# -*- coding: utf-8 -*-

from flask import Blueprint

from .views import TestView


test = Blueprint('test', __name__)

test.add_url_rule('/test', view_func=TestView.as_view('test'))
