#!/usr/bin/env python
"""
OPA is expected to be running on default port 8181
"""

import json
import logging

from flask import Flask, request
from flask_opa import OPA, OPAException


def parse_input():
    return {
        "input": {
            "method": request.method,
            "path": request.path.rstrip('/').strip().split("/")[1:],
            "user": request.headers.get("Authorization", ""),
        }
    }


app = Flask(__name__)
app.config.from_pyfile('app.cfg')

app.opa = OPA(app, input_function=parse_input)
app.logger.setLevel(logging.DEBUG)

data = {
    'alice': {
        "fullname": "Alice B.",
        "age": 27,
        "salary": "6000",
        "position": "Developer"
    },
    'bob': {
        "fullname": "Bob C.",
        "age": 31,
        "salary": "5000",
        "position": "System Admin"
    },
    'charlie': {
        "fullname": "Charlie S.",
        "age": 54,
        "salary": "15000",
        "position": "CEO"
    }
}


@app.route("/")
def welcome_page():
    return "Hello. This is some welcome page accessible to anyone!"


@app.route("/employees", methods=['GET'])
def people_list():
    return json.dumps(list(data.keys()))


@app.route("/employees/<name>", methods=['GET'])
def show_data_of(name):
    if name in data:        
        return json.dumps(data[name])
    else:
        return json.dumps({
            "message": "%s was not found in our system" % name
        }), 404


@app.route("/employees/<name>", methods=['POST'])
def set_data_of(name):
    data[name] = json.loads(request.data)    
    return json.dumps(data[name])


@app.route("/employees/<name>", methods=['DELETE'])
def delete(name):
    if name not in data:
        return json.dumps({
            "message": "%s was not found in our system" % name
        }), 404
    del data[name]    
    return json.dumps(None), 204


@app.errorhandler(OPAException)
def handle_opa_exception(e):
    return json.dumps({"message": str(e)}), 403


if __name__ == '__main__':
    app.run(debug=True)
