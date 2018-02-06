# -*- coding: utf-8 -*-

import json
import os
import traceback
import const

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from werkzeug.wrappers import Request, Response

from core.models import User, ApiList
from core.auth import (Sign, auth_before_request,
                handler_interface, ret_auth_dec)
from settings import DEBUG, SENTRY_UEL, SENTRY_STATUS
from raven import Client

if SENTRY_STATUS:
    client = Client(SENTRY_UEL)


class AuthMiddleware(DispatcherMiddleware):

    def __init__(self, app, mounts=None):

        super(AuthMiddleware, self).__init__(app, mounts)

    def __call__(self, environ, start_response):

        # 不能用super了，因为要用app
        script = environ.get('PATH_INFO', '')
        path_all = script
        path_info = ''
        while '/' in script:
            if script in self.mounts:
                app = self.mounts[script]
                break
            script, last_item = script.rsplit('/', 1)
            path_info = '/%s%s' % (last_item, path_info)
        else:
            app = self.mounts.get(script, self.app)
        original_script_name = environ.get('SCRIPT_NAME', '')
        environ['SCRIPT_NAME'] = original_script_name + script
        environ['PATH_INFO'] = path_info
        if app.name == 'Not Found':
            return app(environ, start_response)
        if handler_interface(path_all) in ['operator_callback', 'operator_tbCallback']:
            return app(environ, start_response)
        req = Request(environ, shallow=False)
        req_method = req.method
        req_data = req.args
        if req_method == 'POST':
            from werkzeug import LimitedStream
            from StringIO import StringIO
            length = int(environ.get('CONTENT_LENGTH', 0) or 0)
            request_data = req.get_data()
            req_data = req.form
            output = StringIO(request_data)
            stream = LimitedStream(output, length)
            environ['wsgi.input'] = stream

        if DEBUG is False:
            sign = req_data.get('sign', '')
            app_key = req_data.get('app_key', '')
            # 验证有没有app_key
            if not app_key:
                resp = Response(json.dumps({
                    'code': const.MISSAPPKEY,
                    'data': None,
                    'msg': const.MSG[const.MISSAPPKEY],
                }))
                return resp(environ, start_response)
            # 验证有没有签名
            if not sign:
                resp = Response(json.dumps({
                    'code': const.MISSSIGN,
                    'data': None,
                    'msg': const.MSG[const.MISSSIGN],
                }))
                return resp(environ, start_response)
            # 验证是不是有效的用户
            user = User.objects(app_key=app_key).first()
            if not Sign.check_user(user):
                resp = Response(json.dumps({
                    'code': const.VERIFYDENIED,
                    'data': None,
                    'msg': const.MSG[const.VERIFYDENIED],
                }))
                return resp(environ, start_response)
            # 验证ip白名单
            ip = req.remote_addr
            if not Sign.check_ip(user, ip):
                resp = Response(json.dumps({
                    'code': const.IPERROR,
                    'data': None,
                    'msg': const.MSG[const.IPERROR],
                }))
                return resp(environ, start_response)
            # 验证时间
            try:
                t = float(req_data.get('t', ''))
            except:
                resp = Response(json.dumps({
                    'code': const.ERRORTIMESTAMP,
                    'data': None,
                    'msg': const.MSG[const.ERRORTIMESTAMP],
                }))
                return resp(environ, start_response)
            if not Sign.check_time(t):
                resp = Response(json.dumps({
                    'code': const.TSEPIRE,
                    'data': None,
                    'msg': const.MSG[const.TSEPIRE],
                }))
                return resp(environ, start_response)
            # 验证权限
            prefix = path_all
            if not Sign.check_permission(user, prefix):
                resp = Response(json.dumps({
                    'code': const.PERMISSIONDENIED,
                    'data': None,
                    'msg': const.MSG[const.PERMISSIONDENIED],
                }))
                return resp(environ, start_response)
            # 验证secret
            secret = Sign.check_secret(user, req_data)
            if not secret:
                resp = Response(json.dumps({
                    'code': const.VERIFYDENIED,
                    'data': None,
                    'msg': const.MSG[const.VERIFYDENIED],
                }))
                return resp(environ, start_response)

        app.config['secret'] = secret
        app.config['app_key'] = app_key
        api_type = handler_interface(path_all)

        # 测试次数控制
        api = ApiList.objects(api_type=api_type).first()
        res = auth_before_request(app_key, api_type, api)
        if not isinstance(res['code'], dict):
            resp = Response(json.dumps({
                'code': res['code'],
                'data': None,
                'msg': const.MSG[res['code']],
            }))
            return resp(environ, start_response)
        # 从子项目获取数据
        try:
            resp_data = iter(app(environ, start_response)).next()
            resp_json_data = json.loads(resp_data)
        except:
            Sign.hander_result(req_data, path_all, api_type, resp_data)
            if SENTRY_STATUS:
                client.captureException()
            return resp_data

        # 对返回字段进行控制, data 表示要控制的js的起始key
        t = ret_auth_dec(user, resp_json_data, api_type, data='data')
        auth_before_request(app_key, api_type, api, result=t)
        # 记录
        Sign.hander_result(req_data, path_all, api_type, t, cache=app.config.get("cache", "") or "")
        resp = Response(json.dumps(t))
        return resp(environ, start_response)


def do(subdir):
    try:
        module = __import__('submodule.{0}'.format(subdir), globals(), locals(), ["app"])
        dispatch.update({
            '/{0}'.format(subdir): module.app.app
        })
    except Exception:
        traceback.print_exc()


subdirs = os.walk(os.getcwd() + '/submodule').next()[1]
dispatch = {}

map(do, subdirs)

app = AuthMiddleware(
    NotFound(),
    dispatch,
)
import newrelic.agent

app = newrelic.agent.WSGIApplicationWrapper(app)
