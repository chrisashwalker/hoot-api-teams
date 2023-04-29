import atexit, json
from bson import json_util
from flask import Flask, jsonify, request
from flask_expects_json import expects_json
from flask_pymongo import PyMongo
from jsonpatch import JsonPatch
from pika import BlockingConnection, ConnectionParameters
from data.teams_data_store import init_teams
from models.team import Team

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://root:guest@hoot-db-mongo:27017/hoot?authSource=admin"
mongo = PyMongo(app)
teams = mongo.db.get_collection('teams')
if teams.estimated_document_count() < 1:
    teams.insert_many(init_teams())

connection = BlockingConnection(ConnectionParameters('hoot-message-queues'))
channel = connection.channel()
channel.queue_declare(queue='deleted-objects', durable=True)

@app.route("/teams", methods=['GET'])
def get_teams():
    return json.loads(json_util.dumps(teams.find({}, {'_id': False})))

@app.route("/teams/<int:id>", methods=['GET'])
def get_team(id):          
    result = teams.find_one({'id': id}, {'_id': False})
    if result:
        return json.loads(json_util.dumps(result))
    return jsonify({"message": "Team not found"}), 404

create_schema = {
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "parent": { "type": "number" }
  },
  "required": ["name"]
}

@app.route("/teams", methods=['POST'])
@expects_json(create_schema)
def create_team():
    team_to_create = request.get_json()
    max_id = max([Team(**t).id for t in json.loads(json_util.dumps(teams.find({}, {'_id': False})))])
    newTeam = Team(max_id + 1, team_to_create.get("name", None), team_to_create.get("parent", None))
    teams.insert_one(newTeam.__dict__)
    return json.loads(json_util.dumps(newTeam.__dict__)), 201

replace_schema = {
  "type": "object",
  "properties": {
    "id": { "type": "number" },
    "name": { "type": "string" },
    "parent": { "type": "number" }
  },
  "required": ["id", "name"]
}

@app.route("/teams", methods=['PUT'])
@expects_json(replace_schema)
def replace_team():
    try:
        obj = request.get_json()
        replacement = Team(obj.get("id", None), obj.get("name", None), obj.get("parent", None))
        teams.find_one_and_replace({'id': replacement.id}, replacement.__dict__)
        return jsonify({}), 204
    except:
        return jsonify({"message": "Bad request"}), 400

@app.route("/teams/<int:id>", methods=['PATCH'])
def update_team(id):
    try:
        patch = JsonPatch.from_string(request.get_data(True,True,False))
        t = teams.find_one({'id': id}, {'_id': False})
        obj = json.loads(json_util.dumps(t))
        patched_dict = patch.apply(obj)
        cast = Team(obj.get("id", None), obj.get("name", None), obj.get("parent", None))
        cast.rebuild(patched_dict)
        teams.update_one(t, {"$set": cast.__dict__})
        return jsonify({}), 204
    except:
        return jsonify({"message": "Bad request"}), 400    

@app.route("/teams/<int:id>", methods=['DELETE'])
def delete_team(id):
    t = teams.find_one({'id': id}, {'_id': False})
    if t:
        teams.delete_one(t)
        if channel:
            msg = '{{"type":"team","objId":{0}}}'.format(id)
            channel.basic_publish('', 'deleted-objects', msg)
        return jsonify({}), 204
          
    return jsonify({"message": "Team not found"}), 404

def close_connection():
    if connection:
        connection.close()

if __name__ == '__main__':
    atexit.register(close_connection)
    app.run(host='0.0.0.0', port=8003)
