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
@app.route('/node', methods=['POST'])
def create_node():
    body = request.get_json()
    name = body['name']
    description = body.get("description", "")
    eid = Manager().create_node(name=name, description=description)
    return Response(f'{{"eid": "{eid}"}}'.encode(), status=201, mimetype='application/json')


@gaurd_edge
@app.route('/node/<eid>', methods=['GET'])
def get_node(eid):
    node = Manager().get_node(eid=eid)
    response = json.dumps({"node": node})
    return Response(response, status=200, mimetype='application/json')

@gaurd_edge
@app.route('/node/<eid>', methods=['DELETE'])
def delete_node(eid):
    node = Manager().delete_node(eid=eid)
    return Response(b'', status=200, mimetype='application/json')


@gaurd_edge
@app.route('/nodes', methods=['GET'])
def list_nodes():
    nodes = Manager().search_node()
    response = json.dumps({"nodes": nodes})
    return Response(
        response, status=200, mimetype='application/json'
    )

@gaurd_edge
@app.route('/node/<eid>', methods=['PUT'])
def update_node(eid):
    body = request.get_json()
    node_name = body.get('name')
    parent_eid = body.get('parent_eid')
    description = body.get('description')
    Manager().update_node(eid=eid, name=node_name, description=description, parent_eid=parent_eid)
    return Response(b'', status=200, mimetype='application/json')
