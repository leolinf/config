# -*- encoding: utf-8 -*-

import re
import grequests

from app.config import Config
from app.core.logger import project_logger
from app.core.functions import exception_handler

import base64
from Crypto.Hash import MD5, SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto import Random


match_phone = re.compile(r"1\d{10}|\d{3,4}-\d{7,8}|\d{3,4}\d{7,8}|\d{7,8}")


def hander_token_request(url, data):
    """处理token请求"""

    try:
        response = grequests.map([grequests.get(url, params=data, verify=False,
            timeout=Config.YOULA_TIMEOUT)], exception_handler=exception_handler)[0]
    except Exception as e:
        project_logger.critical('[ADDRESS_YOULA|TOKEN][ERROR|%s]', str(e))
        return None
    if response.status_code != 200:
        return None
    response.encoding = 'utf-8'
    result = response.json()
    return result


def get_encrypt_data(data):
    """公钥分段加密"""

    maxlength = 117
    params_lst = b""
    while (data):
        _input = data[:maxlength]
        data = data[maxlength:]
        params_lst += encrypt_data(_input)
    return base64.b64encode(params_lst)


def get_decrypt_data(data):
    """私钥分段解密"""

    maxlength = 128
    data = base64.b64decode(data)
    params_lst = b""
    while (data):
        _input = data[:maxlength]
        data = data[maxlength:]
        params_lst += decrypt_data(_input)
    return params_lst


def encrypt_data(params):
    """公钥对数据加密"""
    rsakey = RSA.importKey(base64.b64decode(Config.ZMXY_PUBKEY))
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    text = cipher.encrypt(params.encode())
    return text


def decrypt_data(params):
    """私钥数据解密"""
    rsakey = RSA.importKey(base64.b64decode(Config.ZMXY_PRIVAET))
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    dsize = SHA.digest_size
    sentinel = Random.new().read(15 + dsize)
    text = cipher.decrypt(params, sentinel)
    return text


def sign_data(params):
    """私钥对数据签名"""

    rsakey = RSA.importKey(base64.b64decode(Config.ZMXY_PRIVAET))
    signer = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new(params.encode())
    return base64.b64encode(signer.sign(digest))


def sign_encode(params, sign):
    """私钥验签名"""

    rsakey = RSA.importKey(base64.b64decode(Config.ZMXY_PUBKEY))
    sign = base64.b64decode(sign)
    h = SHA.new(params)
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    return verifier.verify(h, sign)
