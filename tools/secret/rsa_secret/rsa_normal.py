# -*- coding: utf-8 -*-

import base64

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5


def encrypt_data(params, public_key):
    """ 公钥加密"""

    def rsa_encrypt(params, public_key):
        """rsa公钥进行加密"""
        rsakey = RSA.importKey(base64.b64decode(public_key))
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = cipher.encrypt(params.encode())
        return text

    maxlength = 117
    params_lst = b""
    while (params):
        _input = params[:maxlength]
        params = params[maxlength:]
        params_lst += rsa_encrypt(_input, public_key)
    return base64.b64encode(params_lst)


def decrypt_data(param, private_key):
    """私钥对参数进行分段解密"""

    def rsa_decrypt(param, private_key):
        """私钥解密"""
        rsakey = RSA.importKey(base64.b64decode(private_key))
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        dsize = SHA.digest_size
        sentinel = Random.new().read(15 + dsize)
        return cipher.decrypt(param, sentinel)

    maxlength = 128
    param = base64.b64decode(param)
    params_lst = b""
    while (param):
        _input = param[:maxlength]
        param = param[maxlength:]
        params_lst += rsa_decrypt(_input, private_key)
    return params_lst


def encrypt_sign(params, private_key):
    """使用私钥签名"""

    rsakey = RSA.importKey(base64.b64decode(private_key))
    signer = Signature_pkcs1_v1_5.new(rsakey)
    if isinstance(params, bytes):
        digest = SHA.new(params)
    else:
        digest = SHA.new(params.encode())
    sign = signer.sign(digest)
    return base64.b64encode(sign)


def decrypt_sign(param, sign, public_key):
    """使用公钥对参数进行验签"""

    rsakey = RSA.importKey(base64.b64decode(public_key))
    sign = base64.b64decode(sign)
    h = SHA.new(param)
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    return verifier.verify(h, sign)


if __name__ == '__main__':

    private_key = """
    MIIBOwIBAAJBAL5qsSGZUHkc+Eobye2mvVSdsgpzyuxdBHrFKqHgND/L0XR9LLyR
    InfVTtW9HOFaY5aZtSGMgjkHDD3WbLaqELsCAwEAAQJASYO7ezNLxFaQ7VupLB1R
    v1dao3ps/7AxyIxSl0iOI4qL33JYNnRteZMBFA8ca9zpdLyG/07dPhB6kBry5Q4r
    AQIhAPEtm5HbYenPgtnDFXi93Q69fqjPkGFeFW/lyPjPner7AiEAyh53+pXxMzbQ
    5xbnA5mhqUEOTWtxTo7XN5r/KATnhUECIQCJtd4Hqbm91LRFfUQMXnUTzpW89E/f
    mOYqr41SrNHh8wIhAMnR4ru1PUOGWNJnbAWMQoBfFYj44AsxVnWPr3imbQgBAiAN
    zEdqi1PHp/xSKUf0GiEE5N1BFZfKEOYaV7aac4eRSw==
    """
    public_key = """
    MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL5qsSGZUHkc+Eobye2mvVSdsgpzyuxd
    BHrFKqHgND/L0XR9LLyRInfVTtW9HOFaY5aZtSGMgjkHDD3WbLaqELsCAwEAAQ==
    """
    params = '1234567890'
    result = encrypt_data(params, public_key)
    print(result)
    print(decrypt_data(result, private_key))
    sign = encrypt_sign(params, private_key)
    print(sign)
    print(decrypt_sign(params, sign, public_key))
