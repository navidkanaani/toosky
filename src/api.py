import json

from flask import Flask, request, Response

from src.node import NodeManager
from src.manager import Manager
from src.environments import Env
from src.utility import gaurd_edge


app = Flask(__name__)

Env._init_envs_(env_file_path='.env')

@gaurd_edge
@app.route('/ping', methods=['GET'])
def ping():
    return Response(b'{"content": "pong"}', status=200, mimetype='application/json')


@gaurd_edge
@app.route('/node/create', methods=['POST'])
def create_node():
    body = request.get_json()
    name = body['name']
    description = body.get("description", "")
    token = Manager().create_node(name=name, description=description)
    return Response(f'{{"token": "{token}"}}'.encode(), status=201, mimetype='application/json')


@gaurd_edge
@app.route('/node/search/<token>', methods=['GET'])
def get_node(token):
    node = Manager().get_node(token=token)
    response = json.dumps({"node": node})
    return Response(response, status=200, mimetype='application/json')

@gaurd_edge
@app.route('/node/delete/<token>', methods=['DELETE'])
def delete_node(token):
    node = Manager().delete_node(token=token)
    return Response(b'', status=200, mimetype='application/json')


@gaurd_edge
@app.route('/node/list', methods=['GET'])
def list_nodes():
    nodes = Manager().search_node()
    response = json.dumps({"nodes": nodes})
    return Response(
        response, status=200, mimetype='application/json'
    )

@gaurd_edge
@app.route('/node/update/<token>', methods=['PUT'])
def update_node(token):
    body = request.get_json()
    node_name = body.get('name')
    parent_token = body.get('parent_token')
    description = body.get('description')
    Manager().update_node(token=token, name=node_name, description=description, parent_token=parent_token)
    return Response(b'', status=200, mimetype='application/json')
