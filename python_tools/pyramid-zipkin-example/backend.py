# -*- coding: utf-8 -*-
# backend.py
import datetime
import requests

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from transport import http_transport
from py_zipkin.zipkin import create_http_headers_for_new_span


@view_config(route_name='print_date')
def print_date(request):
    print(request.method)

    headers = {}
    headers.update(create_http_headers_for_new_span())
    backend_response = requests.get(
        url='http://localhost:9001/api?aa=1&cc=2',
        headers=headers,
    )

    return Response(backend_response.text)

def main():
    settings = {}
    settings['service_name'] = 'backend'
    settings['zipkin.transport_handler'] = http_transport

    config = Configurator(settings=settings)
    config.include('pyramid_zipkin')
    config.add_route('print_date', '/api')
    config.scan()

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 9000, app)
    server.serve_forever()

if __name__ == '__main__':
    main()
