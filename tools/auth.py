# -*- coding: utf-8 -*-

import functools

from core.utils import decrypt_token
from flask import g, request, jsonify
import const


def clean_cookies(res):
    resp = jsonify(res)
    resp.delete_cookie('login')
    resp.delete_cookie('type')
    return resp


def login_required(auth, req):
    def wrapper(func):
        @functools.wraps(func)
        def decat(self, *args, **kw):
            cookies = request.cookies
            if not cookies:
                res = jsonify({
                    'code': const.PERMISSION_DENIED,
                    'msg': const.MSG[const.PERMISSION_DENIED]})
                res.headers['token'] = None
                return res
            token = request.headers.get('token')
            if token is None:
                res = {'code': const.PERMISSION_DENIED,
                       'msg': const.MSG[const.PERMISSION_DENIED]}
                return clean_cookies(res)

            token_data = decrypt_token(token)
            if not token_data:
                res = {'code': const.PERMISSION_DENIED,
                       'msg': const.MSG[const.PERMISSION_DENIED]}
                return clean_cookies(res)
            else:
                # 判断用户类型
                permisson = [j for i in auth for j in i]
                if token_data['user_type'] not in permisson:
                    res = {'code': const.PERMISSION_DENIED,
                           'msg': const.MSG[const.PERMISSION_DENIED]}
                    return clean_cookies(res)
                g.token_data = token_data
                return func(self, *args, **kw)
        return decat
    return wrapper
