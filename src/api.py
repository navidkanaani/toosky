from flask import Flask, jsonify, request, Response

from src.node import NodeManager

app = Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': '200', 'content': 'pong'})


@app.route('/node', methods=['POST', 'GET'])
def create_node():
    if request.method == 'POST':
        body = request.get_json()
        name = body['name']
        NodeManager().create(name)
        return Response(b'', status=201, mimetype='application/json')
    elif request.method == 'GET':
        ...
