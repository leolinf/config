# -*- coding: utf-8 -*-

import hashlib
import hmac
import time
import base64
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = key

    def encrypet(self, raw):
        raw = self._pad(raw.encode('UTF-8'))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('UTF-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s)- 1:])]

a = 'l1'
b='2'
user_id='123'
account_id='4'
reg_time='l2'
expire= str(time.time())

key = hmac.new(a + b, '|'.join([user_id, reg_time, account_id]), hashlib.sha1).hexdigest()[:32]
enc_msg = AESCipher(key).encrypet('|'.join([user_id, account_id, expire]))
print(enc_msg)
dec_msg = AESCipher(key).decrypt(enc_msg)
print(dec_msg)
