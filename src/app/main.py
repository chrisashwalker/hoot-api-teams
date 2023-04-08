from flask import Flask, jsonify, request
from data.greetings import say_hello_to

app = Flask(__name__)

@app.route("/")
def index() -> str:
    return jsonify({"message": "Success"})
    
@app.route("/hello", methods=['POST'])
def hello() -> str:
    greetee = request.json.get("greetee", None)
    response = {"message": say_hello_to(greetee)}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
