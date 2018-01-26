# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import functools

from core.utils import decrypt_token
# from settings import LOG_CONF
from flask import g, request, jsonify, current_app as app
import const
# from config import config
# LOG_CONF = config['LOG_CONF']

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
                res = jsonify({'code': const.PERMISSION_DENIED,
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


# logging.config.dictConfig(LOG_CONF)
# # create logger
# logger = logging.getLogger('app')
#
#
# def class_logger(cls):
#     cls.logger = logger.getChild(cls.__name__)
#     return cls
#
#
# def trace_view(level='INFO'):
#     def wrapper(func):
#         level_num = logging.getLevelName(level)
#
#         @functools.wraps(func)
#         def _(self, *args, **kwargs):
#             class_name, method = self.__class__.__name__, request.method
#             data = request.values
#             user = request.remote_user
#             logger.log(
#                 level_num,
#                 u'[view|%s][method|%s][user|%s] [request|%r]',
#                 class_name, method, user, data
#             )
#
#             resp = func(self, *args, **kwargs)
#             logger.log(
#                 level_num,
#                 u'[view|%s][method|%s][user|%s] [response|%r]',
#                 class_name, method, user, resp.response
#             )
#             return resp
#         return _
#     if isinstance(level, str):
#         return wrapper
#     else:
#         assert callable(level)
#         func, level = level, 'INFO'
#         return wrapper(func)
