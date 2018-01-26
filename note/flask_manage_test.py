# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.script import Manager

app = Flask(__name__)

@app.route('/test')
def hello_world():
    return 'Hello, World!'

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
