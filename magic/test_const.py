# -*- coding: utf-8 -*-


class MsgMeta(type):

    def __new__(cls, a, b, c):
        c['msg'] = {}
        for k, v in c.items():
            if isinstance(v, tuple):
                code, msg = v
                c[k] = code
                c["msg"][code] = msg
        return type.__new__(cls, a, b, c)


class Msg(object):
    __metaclass__ = MsgMeta

    SUCCESS = '000000', '成功'
    LOGIN = '1232313', '哈哈'


if __name__ == '__main__':
    a = Msg()
    c = a.SUCCESS, a.msg[a.SUCCESS]
    print(c)
