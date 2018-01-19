# -*- coding: utf-8 -*-

import datetime
import requests
import traceback

from flask_login import current_user

from ..constants import MonitorStatus, CreditStatus, ApproveStatus
from ..models import SingleSearch, MonitorSearch as Monitor
from ..core.functions import timestamp2datetime, period2datetime
from ..config import Config
from .logger import project_logger


def somedate2timestamp(year, month, day):
    """年月日转换为时间戳"""

    return int(datetime.datetime(year, month, day).strftime('%s')) * 1000


def get_monitor_cumulate(*args):
    """获取贷中监控累计统计"""

    match = {
        'company_id': current_user.company_id,
        'status': {'$ne': MonitorStatus.DOING},
    }

    monitors = Monitor.objects(__raw__=match).all()
    total_monitor = monitors.count()
    total_break = monitors.filter(break_num__gt=0).count()

    return total_monitor, total_break


def get_credit_cumulate(*args):
    """获取累积进件"""

    match = {
        'company_id': current_user.company_id,
        'status': {'$ne': CreditStatus.NO},
    }

    if args[0] and args[1]:
        match.update({
            'create_time': {
                '$gte': timestamp2datetime(args[0]),
                '$lt': timestamp2datetime(args[1]),
            }
        })
    elif args[2] and args[2] != 'all':
        start_time, end_time = period2datetime(args[2])
        match.update({
            'create_time': {
                '$gte': start_time,
                '$lt': end_time,
            }
        })

    searches = SingleSearch.objects(__raw__=match).all()

    total_search = searches.count()
    total_break = searches.filter(is_break_rule=1).count()

    return total_search, total_break


def get_review_cumulate(*args):
    """获取累积审批"""

    match = {
        'company_id': current_user.company_id,
        'status': {'$ne': CreditStatus.NO},
    }

    if args[0] and args[1]:
        match.update({
            'create_time': {
                '$gte': timestamp2datetime(args[0]),
                '$lt': timestamp2datetime(args[1]),
            }
        })
    elif args[2] and args[2] != 'all':
        start_time, end_time = period2datetime(args[2])
        match.update({
            'create_time': {
                '$gte': start_time,
                '$lt': end_time,
            }
        })

    searches = SingleSearch.objects(__raw__=match).all()

    total_into = searches.count()
    total_approve = searches.filter(approve_status=ApproveStatus.PASS).count()

    return total_into, total_approve


def modify_phone(phone):
    """根据手机号格式不同修改成统一格式"""

    phone = str(phone)
    l = phone.split('.')
    if len(l) == 2:
        return l[0]
    return phone


def get_args(args, index, default):

    if len(args) > index and args[index] != '':
        return args[index]
    else:
        return default


def send_tz(apikey, content, mobile, send_tz_uri='/v1/sms/sendtz', sms_host='api.dingdongcloud.com'):
    """
    发送通知
    """

    req_dict = {
        "apikey": apikey,
        "mobile": mobile,
        "content": content,
    }
    r = requests.post(
        'https://' + sms_host + send_tz_uri,
        data=req_dict
    )

    return r.json()


def short_url(url):
    params = {
        'source': '3538199806',
        'url_long': url,
    }
    r = requests.get('http://api.t.sina.com.cn/short_url/shorten.json', params=params).json()
    return r[0]['url_short']


def send_yzm(apikey, content, mobile, send_tz_uri='/v1/sms/sendyzm', sms_host='api.dingdongcloud.com'):
    """
    发送验证码
    """

    req_dict = {
        "apikey": apikey,
        "mobile": mobile,
        "content": content,
    }
    r = requests.post(
        'https://' + sms_host + send_tz_uri,
        data=req_dict
    )

    return r.json()


def query_location(address, apikey=Config.GD_KEY):
    """获取高德地图地址的坐标"""

    url = 'http://restapi.amap.com/v3/geocode/geo'
    params =  {
        'address': address,
        'key': apikey,
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        r_json = r.json()
        project_logger.info('location got: {0}'.format(r_json))
    except:
        traceback.print_exc()
        return ''
    if r_json.get('geocodes', []):
        return r_json['geocodes'][0]['location']
    else:
        return ''
