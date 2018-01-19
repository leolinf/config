# -*- coding: utf-8 -*-

import json
import logging
import redis
import datetime

from app import celery
from app.models import RequestRecord, RequestRecordIn
from app.config import Config
from app.constants import Code
from .record_in_type import record_success


r = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,
                      password=Config.REDIS_PASSWORD)
redis_server = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,
                                 password=Config.REDIS_PASSWORD, db=9)


def get_data(params):
    """每天去重"""

    if 't' in params:
        params.pop("t")
    if 'sign' in params:
        params.pop("sign")
    sorted(params, key=lambda x: x[0])
    params_string = json.dumps(params)
    status = r.sadd("today", params_string)
    return status


def get_validation(response, api_type):
    """验证类接口"""

    if api_type in ["validation_idcardnameverify"]:
        code = response.get("data", {}).get("resCode")
        if code == 1 or code == -1 or code == 3:
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED
    elif api_type in ["validation_netloanblacklist"]:
        return Code.SUCCESS_RECORED
    elif api_type in ["validation_drivinglicensestatus", "validation_licenseidcheck",
                      "validation_firsthavelicense", "validation_candrivecar",
                      "validation_drivinglicenseauth"]:
        code = response.get("data", {}).get("status")
        if code == "1":
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED
    return Code.SUCCESS_RECORED


def get_obtain(response, api_type):
    """获取信息类接口"""
    if api_type in ["obtain_riskinfocheck"]:
        code = int(response.get("data").get("resCode"))
        if code in [0, 1, 2]:
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED
    if api_type in ["obtain_funddetail", "obtain_securitydetail",
                    "obtain_securityreport", "obtain_fundreport",
                    "obtain_peoplebankreport"]:
        if response.get("data"):
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED
    if api_type in ["obtain_housevalue"]:
        if response.get("data", {}).get("resCode") == -1:
            return Code.FAIL_PECORED
        else:
            return Code.SUCCESS_RECORED
    if api_type == "obtain_idcardpic":
        if response.get("data", {}).get("resCode") in [-1, 1]:
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED

    return Code.SUCCESS_RECORED


def get_operator(response, api_type):
    """运营商类接口"""

    if api_type in ["operator_phoneonlinetime", "operator_cmcconlinetime", "operator_unicomonlinetime",
                    "operator_telecomonlinetime"]:
        code = int(response.get("data").get("resCode"))
        if code in [0, 1, 2, 3, 4, 5, 6]:
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED

    elif api_type in ["operator_cmccby3ele"]:
        code = int(response.get("data").get("resCode"))
        if code in [1, -1]:
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED

    elif api_type in ["operator_unicomby3ele", "operator_telecomby3ele", "bank_bankcardby3ele",
                      "operator_operatorby3ele"]:
        code = int(response.get("data").get("resCode"))
        if code in [1, -1, 0]:
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED

    elif api_type in ["operator_phonetime"]:
        code = int(response.get("data").get("resCode"))
        if code in [0, 1, 2, 3, -1]:
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED
    elif api_type in ["operator_cmcctime", "operator_unicomtime", "operator_telecomtime"]:
        # 对外返回Z，表示无数据
        if response.get("data", {}).get("resCode") == "Z":
            return Code.FAIL_PECORED
        else:
            return Code.SUCCESS_RECORED
    elif api_type in ["operator_cmccstatus", "operator_unicomstatus", "operator_telecomstatus"]:
        # 对外返回9, 表示无数据
        if response.get("data", {}).get("resCode") == "9":
            return Code.FAIL_PECORED
        else:
            return Code.SUCCESS_RECORED
    else:
        return Code.SUCCESS_RECORED


def get_bank(response, api_type):
    """银行类接口"""

    if api_type in ["bank_bankcardby3ele", "bank_bankcardby4ele"]:
        code = int(response.get("data").get("resCode"))
        if code in [1, -1, 0]:
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED


def get_image(response, api_type):
    """图片类接口"""

    if api_type in ["image_idnamefacecheck"]:
        code = int(response.get("data").get("resCode"))
        if code in [1, 2, 3, 4]:
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED


def get_zhima_credit(response, api_type):
    """芝麻信用接口"""

    if api_type in ["zhima_credit_fraudscore", "zhima_credit_verifyfraudmsg",
                    "zhima_credit_fraudrisklist", "zhima_credit_score",
                    "zhima_credit_watchlist"]:
        if response.get("data").get("success"):
            return Code.SUCCESS_RECORED
        else:
            return Code.FAIL_PECORED
    if api_type in ["zhima_credit_auth"]:
        return Code.SUCCESS_RECORED


@celery.task
def record(req_data, path, api_type, response, cache_data=""):
    """ 记录 """

    params = req_data
    appkey = params.get('app_key')
    if api_type == 'tel_basics':
        params = (dict(params))
        params.update({"repeat": "repeat"})
    # 记录请求成功，匹配成功，重复
    success, match, repeat = Code.FAIL_PECORED, Code.FAIL_PECORED, Code.FAIL_PECORED
    try:
        if response.get("code") == Code.SUCCESS:
            # 请求为1200 请求成功，匹配成功
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
            if api_type.startswith("validation"):
                match = get_validation(response, api_type)

            elif api_type.startswith("obtain"):
                match = get_obtain(response, api_type)

            elif api_type.startswith("operator"):
                match = get_operator(response, api_type)

            elif api_type.startswith("bank"):
                match = get_bank(response, api_type)

            elif api_type.startswith("image"):
                match = get_image(response, api_type)

            elif api_type.startswith("zhima_credit"):
                match = get_zhima_credit(response, api_type)

        if response.get("code") == 1230:
            # 请求成功，但是不匹配

            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED
            if api_type in ["obtain_education"]:
                success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED

    except AttributeError:
        pass

    _cache = 0
    if not cache_data:
        _cache = 1
    logging.warn("%s %s %s %s %s", api_type, success, match, repeat, _cache)
    now = datetime.datetime.now()
    RequestRecord(
        app_key=appkey,
        create_time=now,
        interface=path,
        params=params,
        match=match,
        success=success,
        repeat=repeat,
        result=response,
        api_type=api_type,
        cache=_cache
    ).save()


@celery.task
def delete_today():
    """清除redis"""
    logging.warn('#############')
    r.delete("today")


@celery.task
def request_record_in(in_type, api_type, params, path, result, _time):
    """第三方请求记录"""

    appkey = params.get('app_key')
    # 记录请求成功，匹配成功，重复
    try:
        success, match = record_success(in_type, result)
    except Exception as e:
        logging.warn(str(e))
        success, match = Code.FAIL_PECORED, Code.FAIL_PECORED
    logging.warn("%s %s %s %s", appkey, in_type, success, match)
    now = datetime.datetime.now()
    RequestRecordIn(
        app_key=appkey,
        create_time=now,
        interface=path,
        params=params,
        match=match,
        success=success,
        repeat=0,
        result=result,
        api_type=api_type,
        in_type=in_type,
        timeout=_time
    ).save()


@celery.task
def update_token():
    """更新token"""

    from app.obtain.util import get_token
    logging.warn('update token start')
    token = get_token()
    logging.warn("token {}".format(token))
    status = redis_server.set("update_token", token)
    if not status:
        token = get_token()
        status = redis_server.set("update_token", token)
    logging.warn('update token success %s', status)
