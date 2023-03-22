from flask import Flask, jsonify, request, Response

from src.node import NodeManager

app = Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': '200', 'content': 'pong'})


@app.route('/node', methods=['POST'])
def create_node():
    body = request.get_json()
    name = body['name']
    node_id = NodeManager().create(name)
    return Response(f'{{"node_id": {node_id}}}'.encode(), status=201, mimetype='application/json')


@app.route('/node/<node_id>', methods=['GET'])
def get_node(node_id):
    node = NodeManager().get(node_id=node_id)
    print(node)
    return Response(f'{{"node": "{node}"}}'.encode(), status=200, mimetype='application/json')
