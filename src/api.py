from flask import Flask, request, Response

from src.node import NodeManager

app = Flask(__name__)

# node_manager = NodeManager()


@app.route('/ping', methods=['GET'])
def ping():
    return Response(b'{"content": "pong"}', status=200, mimetype='application/json')


@app.route('/node', methods=['POST'])
def create_node():
    body = request.get_json()
    name = body['name']
    node_id = NodeManager().create(name)
    return Response(f'{{"node_id": {node_id}}}'.encode(), status=201, mimetype='application/json')


@app.route('/node/<node_id>', methods=['GET'])
def get_node(node_id):
    node = NodeManager().get(node_id=node_id)
    return Response(f'{{"node": {node}}}'.encode(), status=200, mimetype='application/json')

@app.route('/node/<node_id>', methods=['DELETE'])
def delete_node(node_id):
    node = NodeManager().delete(node_id=node_id)
    return Response(b'', status=200, mimetype='application/json')


@app.route('/node', methods=['GET'])
def list_nodes():
    nodes = NodeManager().search()
    return Response(
        f'{{"nodes": {nodes}}}'.encode(), status=200, mimetype='application/json'
    )
