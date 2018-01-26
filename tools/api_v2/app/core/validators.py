# -*- coding: utf-8 -*-

import re
import datetime

from flask_restful import inputs


phone = inputs.regex('^1\d{10}$')
name = inputs.regex('^.{0,10}$')
banknum = inputs.regex('^.{5,30}$')
address = inputs.regex('^.{5,30}$')
cmcc_number = ["134", "135", "136", "137", "138", "139", "150", "151", "152",
               "157", "158", "159", "182", "183", "184", "187", "188", "147",
               "178", "1705", "1703", "1706"]
telecom_number = ["133", "153", "180", "181", "189", "177", "179", "149",
                  "1700", "1701", "1702"]
unicom_number = ["130", "131", "132", "155", "156", "145", "185", "186", "176",
                 "175", "1707", "1708", "1709"]


def idnum(form, field):
    value = field.data
    message = 'The input field idnum is illegal.'

    pattern = re.compile('^\d{17}[0-9X]$')
    if not pattern.match(value):
        raise ValueError(message)

    if value[6:8] not in ["19", "20"]:
        raise ValueError(message)

    birth = value[6:14]
    try:
        datetime.datetime.strptime(birth, '%Y%m%d')
    except ValueError:
        raise ValueError(message)

    def _relation(value):
        factor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        last = {
            0: '1',
            1: '0',
            2: 'X',
            3: '9',
            4: '8',
            5: '7',
            6: '6',
            7: '5',
            8: '4',
            9: '3',
            10: '2',
        }
        summary = sum([int(value[i]) * factor[i] for i in range(17)])
        return last[summary % 11] == value[-1]

    if not _relation(value):
        raise ValueError(message)

    return value


def typenum(form, field):
    value = field.data
    message = "illegal type number "

    try:
        if value in ["1", "2", "3"]:
            pass
    except:
        raise ValueError(message)
    return value


def month_num(form, field):
    value = field.data
    message = "illegal month number, please input 3, 6 or 12."

    try:
        if value in ["3", "6", "12"]:
            pass
    except:
        raise ValueError(message)
    return value


def type(form, field):
    value = field.data
    message = "illegal type, please input 1, 2, 3, 4, 5, 6"

    try:
        if value in ["1", "2", "3", "4", "5", "6"]:
            pass
    except:
        raise ValueError(message)
    return value


def identity_type(form, field):
    value = field.data
    message = "illegal type, please input 1, 2, 3, 4, 5, 6"

    try:
        if value in ["1", "2"]:
            pass
        else:
            raise ValueError(message)
    except:
        raise ValueError(message)
    return value
