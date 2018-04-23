# -*- coding:utf-8 -*-

from flask import Flask, request, Response, redirect
from simple_client import client_call


app = Flask(__name__)


@app.route('/test', methods=['GET'])
def upload_file():
    return client_call('test')


if __name__ == '__main__':
    app.run(debug=True)
