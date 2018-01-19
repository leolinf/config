# -*- coding: utf-8 -*-

import base64
import datetime
import hashlib
import json
import time
from decimal import Decimal
from urllib.parse import quote, parse_qs

import pyDes
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Hash import SHA, MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from flask import jsonify
from flask.json import JSONEncoder

from app.config import Config
from app.core.logger import project_logger
from ..constants import Code


def get_params(data):
    """合并参数"""

    data.update({"account": Config.CCX_ACCOUNT})
    lst = []
    for i in data:
        if i == "sign":
            continue
        lst.append(i + data[i])
    s = "".join(sorted(lst)) + Config.CCX_KEY
    project_logger.info("[sign|%s]" % s)
    sign = hashlib.md5(s.encode()).hexdigest().upper()
    project_logger.info("[sign|%s]" % sign)
    data.update({"sign": sign})
    return data


def datetime2timestamp(sometime):
    """转换datetime为timestamp"""

    if not sometime:
        return

    return time.mktime(sometime.timetuple()) * 1000


def exception_handler(request, exception):
    """grequests 错误捕获"""

    raise exception


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):

        if isinstance(obj, datetime.datetime):
            return datetime2timestamp(obj)

        if isinstance(obj, Decimal):
            return int(obj)

        return JSONEncoder.default(self, obj)


def make_response(data=None, status=Code.SUCCESS, msg=""):

    if not msg:
        msg = Code.MSG.get(status)

    return jsonify({
        'data': data,
        'code': status,
        'msg': msg,
    })


def check_whether_cache_from_response(resp):
    """从response判断要不要加入缓存"""

    result = json.loads(resp.data.decode())

    if isinstance(result, dict) and result.get('code') in [1200, 1230]:
        return True

    return False


def get_rsa_encrypt_param(params):
    """获取RSA加密数据"""
    num = "1111111111"
    params.update({
        "userId": Config.WESCORE_USERID,
        "userPwd": Config.WESCORE_PWD,
        "secretKey": num
    })
    for i in params:
        if i == "userId":
            continue
        else:
            params[i] = zhima_encrypt_data(params[i], Config.WESCORE_PUBKEY)
    return params


def get_encrypt_param(params):
    """对参数进行加密封装"""
    _salt = b"\xA9\x9B\xC8\x32\x56\x35\xE3\x03"
    _iterations = 2
    data = []
    for i in params:
        data.append("{}={}".format(i, params[i]))
    str_param = "&".join(data)

    hasher = MD5.new()
    hasher.update(Config.DATATANG_KEY.encode())
    hasher.update(_salt)
    result = hasher.digest()
    for i in range(1, _iterations):
        hasher = MD5.new()
        hasher.update(result)
        result = hasher.digest()

    despy = pyDes.des(result[:8], pyDes.CBC, padmode=pyDes.PAD_PKCS5, IV=result[8:16])
    encrypt_data = despy.encrypt(str_param.encode())
    encryptParam = base64.b64encode(encrypt_data)
    res = {
        "apikey": Config.DATATANG_KEY,
        "encryptParam": encryptParam.decode()
    }
    return res


def zhima_encrypt_data(params, public_key):
    """
    芝麻信用rsa分段加密
    params参数形式为：name=zhishu&addr=chengdushi,即需urlencode
    """
    def zhima_rsa_encrypt(params, public_key):
        """使用芝麻rsa公钥进行加密"""
        rsakey = RSA.importKey(base64.b64decode(public_key))
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = cipher.encrypt(params.encode())
        return text

    maxlength = 117
    params_lst = b""
    while (params):
        _input = params[:maxlength]
        params = params[maxlength:]
        params_lst += zhima_rsa_encrypt(_input, public_key)
    return base64.b64encode(params_lst)


def zhima_decrypt_data(param, private_key):
    """使用私钥对参数进行分段解密"""

    def decrypt_data(param, private_key):
        """私钥解密"""
        rsakey = RSA.importKey(base64.b64decode(private_key))
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        dsize = SHA.digest_size
        sentinel = Random.new().read(15 + dsize)
        text = cipher.decrypt(param, sentinel)
        return text

    maxlength = 128
    param = base64.b64decode(param)
    params_lst = b""
    while (param):
        _input = param[:maxlength]
        param = param[maxlength:]
        params_lst += decrypt_data(_input, private_key)
    return params_lst


def zhima_encrypt_sign(params, private_key):
    """使用私钥签名"""

    rsakey = RSA.importKey(base64.b64decode(private_key))
    signer = Signature_pkcs1_v1_5.new(rsakey)
    if isinstance(params, bytes):
        digest = SHA.new(params)
    else:
        digest = SHA.new(params.encode())
    sign = signer.sign(digest)
    return base64.b64encode(sign)


def zhima_decrypt_sign(param, sign, public_key):
    """使用公钥对参数进行验签"""

    rsakey = RSA.importKey(base64.b64decode(public_key))
    sign = base64.b64decode(sign)
    h = SHA.new(param)
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    return verifier.verify(h, sign)


def buildQueryWithEncode(params):
    '''
    将params组合成key1=value1&key2=value2字符串
    :param params:字典
    :param needEncode:value是否需要encode
    :return string
    '''
    def checkEmpty(value):
        '''
        校验值非空
        :return bool: 非空则为true
        '''
        try:
            if bool(value.strip()):
                return True
            return False
        except:
            return False

    needEncode = True
    if not type(params) == dict:
        return False

    params_data = ''
    for (key, value) in params.items():
        if checkEmpty(value):
            value = bool(needEncode) and quote(value) or value
            params_data = params_data + key + '=' + value + '&'
    params_data = params_data[:-1]
    return params_data


def urlparse_change(data):
    """
    a=1&b=2&c=3
    转换成字典
    """

    result = {}
    for k, v in parse_qs(data.decode()).items():
        result[k] = v[0]
    return result


def get_md5_params(cover_string, appSecret):
    """俊聿Md5编码"""

    param = cover_string + appSecret
    return hashlib.md5(param.encode()).hexdigest()


def kaola_des_encrypt(params):
    """考拉DES加密"""

    data = json.dumps(params)
    key = Config.KAOLA_DESKEY
    iv = Random.new().read(8)
    des = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5, IV=iv)
    encrypt_data = des.encrypt(data.encode())
    return base64.b64encode(encrypt_data)


def kaola_des_decrypt(data):
    """考拉des解密"""

    data = base64.b64decode(data)
    key = Config.KAOLA_DESKEY
    iv = Random.new().read(8)
    des = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5, IV=iv)
    decrypt_data = des.decrypt(data)
    return decrypt_data
