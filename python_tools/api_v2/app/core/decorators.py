# -*- coding: utf-8 -*-

import json
import urllib.parse
from functools import wraps

from flask import request, jsonify, g
from flask.views import View

from ..constants import Code
from .functions import make_response
from .logger import project_logger
from ..models import User, ApiList
from .managers import (Sign, auth_before_request,
                       handler_interface, ret_auth_dec)
from ..extensions import cache
from ..config import Config


def authenticate_required(func):
    """
    鉴权装饰器, 装饰view的具体方法
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        req_method = request.method
        req_path = request.path
        req_data = request.args
        if req_method == 'POST':
            req_data = request.form

        sign = req_data.get('sign', '')
        app_key = req_data.get('app_key', '')

        # 验证有没有app_key
        if not app_key:
            return make_response(status=Code.MISSAPPKEY)

        # 验证有没有签名
        if not sign:
            return make_response(status=Code.MISSSIGN)

        # 验证是不是有效的用户
        user = User.objects(app_key=app_key).first()
        if not Sign.check_user(user):
            return make_response(status=Code.VERIFYDENIED)

        # 验证ip白名单
        ip = request.remote_addr
        if not Sign.check_ip(user, ip):
            return make_response(status=Code.IPERROR)

        # 验证时间
        try:
            t = float(req_data.get('t', ''))
        except:
            return make_response(status=Code.ERRORTIMESTAMP)
        if not Sign.check_time(t):
            return make_response(status=Code.TSEPIRE)

        # 验证权限
        if not Sign.check_permission(user, req_path):
            return make_response(status=Code.PERMISSIONDENIED)

        # 验证secret
        secret = Sign.check_secret(user, req_data)
        if not secret:
            return make_response(status=Code.VERIFYDENIED)

        # 测试次数控制
        api_type = handler_interface(req_path)
        api = ApiList.objects(api_type=api_type).first()
        res = auth_before_request(app_key, api_type, api)
        if not isinstance(res['code'], dict):
            return jsonify({
                'code': res['code'],
                'data': None,
                'msg': Code.MSG[res['code']],
            })

        # 请求view 里面的数据
        resp = func(*args, **kwargs)

        resp_json_data = json.loads(resp.get_data().decode("utf-8"))
        # 对返回字段进行控制, data 表示要控制的js的起始key
        t = ret_auth_dec(user, resp_json_data, api_type, data='data')
        auth_before_request(app_key, api_type, api, result=t)
        # 记录
        _cache = getattr(g, "cache_data", "")
        Sign.hander_result(req_data, req_path, api_type, t, cache_data=_cache)
        return jsonify(resp_json_data)

    return wrapper


def custom_memoize(**kw):
    """
    封装了memoize的缓存装饰器，可以装饰具体view的get方法
    :param **kw: 与memoize的参数一致
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # 表示装饰的是view的get方法
            if args and isinstance(args[0], View):
                if request.method == 'GET':
                    request_parmams = request.args.copy()
                else:
                    request_parmams = request.form.copy()

                if 'sign' in request_parmams:
                    request_parmams.pop('sign')
                if 't' in request_parmams:
                    request_parmams.pop('t')
                if 'app_key' in request_parmams:
                    request_parmams.pop('app_key')

                def _fuck(params):
                    string = sorted(params.items(), key=lambda param: param[0])
                    return urllib.parse.urlencode(string)

                request_parmams = _fuck(request_parmams)

                @cache.memoize(**kw)
                def ciao(view, request_parmams):
                    """
                    :param view: 作用是让缓存区别不同的view
                    """

                    project_logger.info('本次查询没有取缓存的数据')
                    g.cache_data = "cache"
                    return func(*args, **kwargs)

                return ciao(args[0].__class__, request_parmams)

            # 表示装饰的是view的其他方法
            # if args and isinstance(args[0], View) and request.method != 'GET':
            #     raise Exception('目前不支持GET以外方法的缓存')

            # 表示装饰一般的方法
            resp = cache.memoize(**kw)(func)(*args, **kwargs)

            return resp
        return wrapper
    return decorator


def modify_output(func):
    """
    装饰第三方接口的方法
    :param is_testing: 是否是测试，为True时直接返回假数据，不实际请求第三方接口
    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        if not Config.IS_TESTING:
            return func(*args, **kwargs)

        return {}

    return wrapper
