from flask import Flask, jsonify, request
from flask_expects_json import expects_json
from jsonpatch import JsonPatch
from data.teams_data_store import teams
from models.team import Team

app = Flask(__name__)

@app.route("/teams", methods=['GET'])
def get_teams():
    return jsonify([t.__dict__ for t in teams])

@app.route("/teams/<int:id>", methods=['GET'])
def get_team(id):
    for t in teams:
        if t.id == id:
            return jsonify(t.__dict__)
          
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

    max_id = 0
    if teams:
        max_id = max([t.id for t in teams])
    
    newTeam = Team(max_id + 1, team_to_create.get("name", None), team_to_create.get("parent", None))
    teams.append(newTeam)
    return jsonify(newTeam.__dict__), 201

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
    replacement = request.get_json()
    
    for t in teams:
        if t.id == replacement.get("id", None):
            t.name = replacement.get("name", None)
            t.parent = replacement.get("parent", None)
            return jsonify({}), 204
          
    return jsonify({"message": "Bad request"}), 400

@app.route("/teams/<int:id>", methods=['PATCH'])
def update_team(id):
    patch = JsonPatch.from_string(request.get_data(True,True,False))
    
    for t in teams:
        if t.id == id:
            patched_dict = patch.apply(t.__dict__)
            t.rebuild(patched_dict)
            return jsonify({}), 204
          
    return jsonify({"message": "Bad request"}), 400    

@app.route("/teams/<int:id>", methods=['DELETE'])
def delete_team(id):
    for t in teams:
        if t.id == id:
            teams.remove(t)
            return jsonify({}), 204
          
    return jsonify({"message": "Team not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)
