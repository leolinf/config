# -*- coding: utf-8 -*-
"""
可以根据私钥 得到公钥 不能通过公钥获取私钥
注意：跨平台私钥无法得到公钥 mac linux
openssl genrsa -out private_key.pem 1024
openssl rsa -in private_key.pem -pubout -out public_key.pem

特殊的加密解密方式
rsa 私钥加密 公钥解密
"""
import base64
import M2Crypto


def rsa_encrypt(params):
    file_name = 'private_key.pem'
    rsa_pri = M2Crypto.RSA.load_key(file_name)
    # 这里的方法选择加密填充方式，所以在解密的时候 要对应。
    return rsa_pri.private_encrypt(params, M2Crypto.RSA.pkcs1_padding)


def encrypt_data(params):
    '''私钥加密'''

    params_lst = ""
    maxlength = 117
    while (params):
        _input = params[:maxlength]
        params = params[maxlength:]
        params_lst += rsa_encrypt(_input)
    return base64.b64encode(params_lst)


def rsa_decrypt(param):
    file_name = 'public_key.pem'
    rsa_pub = M2Crypto.RSA.load_pub_key(file_name)
    # 解密
    return rsa_pub.public_decrypt(param, M2Crypto.RSA.pkcs1_padding)


def decrypt_data(sign):
    """公钥解密"""

    param = base64.b64decode(sign)
    maxlength = 128
    params_lst = ""
    while (param):
        _input = param[:maxlength]
        param = param[maxlength:]
        params_lst += decrypt_data(_input)
    return params_lst
