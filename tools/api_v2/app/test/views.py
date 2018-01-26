# -*- coding: utf-8 -*-

import requests

from flask.views import MethodView
from flask_zipkin import Zipkin

from ..core.functions import make_response
from ..core.decorators import authenticate_required
from ..extensions import zipkin


class TestView(MethodView):

    def get(self):

        headers = {}

        headers.update(zipkin.create_http_headers_for_new_span())

        backend_response = requests.post(
            url='http://localhost:9001/api',
            json={"a": 1, "b": 2},
            headers=headers,
        )
        return make_response()
