from flask import Flask, request, Response

from src.node import NodeManager
from src.environments import Env

app = Flask(__name__)

Env._init_envs_(env_file_path='.env')
# node_manager = NodeManager()


@app.route('/ping', methods=['GET'])
def ping():
    return Response(b'{"content": "pong"}', status=200, mimetype='application/json')


@app.route('/node', methods=['POST'])
def create_node():
    body = request.get_json()
    name = body['name']
    description = body.get("description", "")
    node_id = NodeManager(db=Env.DB_NAME, table_name=Env.NODE_TABLE_NAME).create(name=name, description=description)
    return Response(f'{{"node_id": {node_id}}}'.encode(), status=201, mimetype='application/json')


@app.route('/node/<token>', methods=['GET'])
def get_node(token):
    node = NodeManager(db=Env.DB_NAME, table_name=Env.NODE_TABLE_NAME).get(token=token)
    return Response(f'{{"node": {node}}}'.encode(), status=200, mimetype='application/json')

@app.route('/node/<node_id>', methods=['DELETE'])
def delete_node(node_id):
    node = NodeManager(db=Env.DB_NAME, table_name=Env.NODE_TABLE_NAME).delete(node_id=node_id)
    return Response(b'', status=200, mimetype='application/json')


@app.route('/node', methods=['GET'])
def list_nodes():
    nodes = NodeManager(db=Env.DB_NAME, table_name=Env.NODE_TABLE_NAME).search()
    return Response(
        f'{{"nodes": {nodes}}}'.encode(), status=200, mimetype='application/json'
    )
