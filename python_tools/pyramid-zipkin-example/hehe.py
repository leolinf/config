# -*- coding: utf-8 -*-
# backend.py
import datetime

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from transport import http_transport


@view_config(route_name='print_date', renderer='json')
def print_date(request):
    if request.method == "POST":
        print(request.json)
        return {"code": 10000, "msg": "success"}
    else:
        return Response(str(datetime.datetime.now()))

def main():
    settings = {}
    settings['service_name'] = 'hehe'
    settings['zipkin.transport_handler'] = http_transport

    config = Configurator(settings=settings)
    config.include('pyramid_zipkin')
    config.add_route('print_date', '/api')
    config.scan()

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 9001, app)
    server.serve_forever()

if __name__ == '__main__':
    main()
