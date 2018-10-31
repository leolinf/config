# -*- coding: utf-8 -*-

import base64
import json

import pyDes
from Crypto import Random
from Crypto.Cipher import DES


def kaola_des_encrypt(params):
    """DES加密"""
    data = json.dumps(params)
    key = ''
    iv = Random.new().read(8)
    des = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5, IV=iv)
    encrypt_data = des.encrypt(data.encode())
    return base64.b64encode(encrypt_data)


def kaola_des_decrypt(data):
    """des解密"""

    data = base64.b64decode(data)
    key = ''
    iv = Random.new().read(8)
    des = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5, IV=iv)
    decrypt_data = des.decrypt(data)
    return decrypt_data


def des_encrypt(s):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，base64
    """
    key = ''
    cipherX = DES.new(key[:8], DES.MODE_ECB)
    pad = 8 - len(s) % 8
    padStr = ""
    for i in range(pad):
        padStr = padStr + chr(pad)
    s = s + padStr
    x = cipherX.encrypt(s)
    return base64.b64encode(x)


def des_descrypt(s):
    """
    DES 解密
    :param s: 加密后的字符串，base64
    :return:  解密后的字符串
    """
    key = ''
    str = base64.b64decode(s)
    cipherX = DES.new(key[:8], DES.MODE_CBC)
    y = cipherX.decrypt(str)
    return y[0:ord(y[len(y)-1]) *-1]
