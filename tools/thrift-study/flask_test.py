# -*- coding:utf-8 -*-

from flask import Flask, request
from simple_client import client_call


app = Flask(__name__)


@app.route('/', methods=['GET'])
def upload_file():
    data = request.args
    return client_call(data['test'])


if __name__ == '__main__':
    app.run(debug=True)
