# -*- coding: utf-8 -*-

import urllib.parse
import hashlib
import time

from app.config import Config

from task.tasks import record
from app.constants import Code as const
from app.models.mongos import ApiList
from .logger import project_logger


class Sign(object):

    @classmethod
    def check_user(cls, user):
        """验证用户app_key"""

        if not user:
            return False
        return True

    @classmethod
    def check_ip(cls, user, ip):
        """校验ip白名单"""

        Ip = user.ip_list
        Ip.append("192.168.100.3")
        if ip not in Ip:
            return False
        return True

    @classmethod
    def check_time(cls, t):
        """检验时间是否十分内"""

        now = time.time()
        if abs(now - float(t)) > 600:
            return False
        return True

    @classmethod
    def check_secret(cls, user, data):
        """检验secret并且,验证成功并返回secret"""

        secret = user.app_secret
        l = []
        for k in data:
            if k.startswith('image'):
                continue
            if k in ["sign", "frontPhoto", "backPhoto"]:
                continue
            l.append(k + urllib.parse.quote(data[k], safe=''))

        s = secret + ''.join(sorted(l)) + secret
        sign = hashlib.md5(s.encode()).hexdigest()

        if sign != data.get('sign'):
            project_logger.debug('正确的签名应该是: {0}'.format(sign))
            return False
        return secret

    @classmethod
    def check_permission(cls, user, prefix):
        """权限验证"""

        prefix = handler_interface(prefix)
        if prefix in user.permissions:
            return True
        return False

    @classmethod
    def hander_result(cls, req_data, path_all, api_type, response, cache_data=""):
        """处理请求下来的结果并且记录"""

        # TODO
        record.apply_async(
            args=[
                req_data,
                path_all,
                api_type,
                response
            ],
            kwargs={"cache_data": cache_data},
            queue=Config.RABBITMQ_NAME
        )


def handler_interface(path):
    """处理path接口/enterprise/info/处理成enterpries_info"""
    try:
        uri = path.split("/")[2]
        uri_two = path.split("/")[3]

        url = ["tel", "portray"]
        url_two = ['batch', 'label']
        if uri not in url:
            return uri + "_" + uri_two
        if uri_two not in url_two:
            return uri + "_" + uri_two
        return uri
    except IndexError:
        return None


def Dfs_json(ret, perm):

    if isinstance(ret, list):
        for i in ret:
            Dfs_json(i, perm)

    if isinstance(ret, dict):
        for k in list(ret.keys()):
            if k in perm:
                ret.pop(k)
                continue
            if isinstance(ret[k], dict):
                Dfs_json(ret[k], perm)
            if isinstance(ret[k], list):
                Dfs_json(ret[k], perm)


def ret_auth_dec(user, ret_json_old, api_type, data='data'):
    """
    控制权限返回数据
    """
#    ret_json_old = json.loads(ret_json)
    ret_json = ret_json_old.get(data, '')
    if not ret_json:
        return ret_json_old

    permission_one = Permission.get_permission(api_type, user)
    permission_one = [x['name'] for x in permission_one if not x['enabled']]

    # 过滤不要的数据

    Dfs_json(ret_json, permission_one)

    return {'code': ret_json_old.get("code"), 'data': ret_json, 'msg': const.MSG[const.SUCCESS]}


# 自定义的list来操作列表
class MyList(list):
    def __init__(self, *args, **kw):
        t = super(MyList, self).__init__(*args, **kw)
        if not isinstance(args, tuple):
            return t
        tmp = args[0]
        if not isinstance(tmp, list):
            return t
        for i in tmp:
            if isinstance(i, dict) and len(i.keys()) == 1:
                key = list(i.keys())[0]
                setattr(self, 'shawn_%s' % (key), i[key])
                setattr(self, 'shawn_index_%s' % (key), self.index(i))
        return t

    def append(self, obj):
        t = super(MyList, self).append(obj)
        if not isinstance(obj, dict):
            return t
        key = obj.keys()[0]
        try:
            setattr(self, 'shawn_%s' % (key), self.index(obj))
        except:
            raise ValueError
        return t


class Permission(object):
    """十进制转 二进制"""

    @classmethod
    def NumTranPermission(cls, num):
        try:
            num = int(num)
        except ValueError:
            return '0'
        ret = ''
        while num != 0:
            ret = str(num & 1) + ret
            num = num >> 1
        return ret

    # 该方法默认在permission中存在 该接口的权限
    @classmethod
    def get_permission(cls, api_type, user):
        res = []
        api = ApiList.objects(api_type=api_type).first()
        tmp_param = MyList(user.param_limit)

        u_auth_num = getattr(tmp_param, 'shawn_%s' % (api_type), 0)
        bin_num = cls.NumTranPermission(u_auth_num)

        len_0 = len(api.all_auth_field) - len(bin_num)
        if len_0 > 0:
            bin_num = len_0 * '0' + bin_num

        # 二进制字符串和权限的对应关系
        len_of_auth, k = len(bin_num), 0
        if api.all_auth_field is None:
            return res
        for i in api.all_auth_field:
            if k < len_of_auth:
                res.append({
                    'description': i['description'],
                    'name': i['name'],
                    'enabled': int(bin_num[k])
                })
                k += 1
            else:
                res.append({
                    'description': i['description'],
                    'name': i['name'],
                    'enabled': 0
                })
        return res


def auth_before_request(app_key, api_type, api, result=None):
    """控制测试数量"""

#    api = ApiList.objects(api_type=api_type).first()
    measure_status = api.measure_status.get(app_key)
    # 既不是测试状态也不是正式状态， 不可获取数据
    if not api.measure_status:
        return {'code': const.PERMISSIONTEST}

    if measure_status == 0:
        return {'code': const.PERMISSIONTEST}

    # 有正式权限直接返回
    if api.offical_status and api.offical_status.get(app_key) == 1:
        return {'code': {}}

    # 表示测试状态, 而且当前测试数量大于1
    if measure_status == 1 and api.measure_count.get(app_key) > 0:
        if result:
            if result.get("code") == 1200 or result.get("code") == 1230:
                api.measure_count[app_key] = api.measure_count[app_key] - 1
                api.save()
                return {'code': {}}
        else:
            return {'code': {}}
    # 数量超过测试数量
    else:
        return {"code": const.OVER_TEST}
