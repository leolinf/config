# -*- coding: utf-8 -*-

import datetime
from mongoengine import connect, DynamicDocument, StringField, ListField, \
    DateTimeField, DictField, DynamicField, IntField, ReferenceField, \
    BooleanField, ObjectIdField


class User(DynamicDocument):
    """
    user表是公司信息
    """
    app_key = StringField(unique=True)

    app_secret = StringField()

    permissions = ListField()

    ip_list = ListField()

    ''' 以下account、password、user_type不会再使用
    　　而是在Account表中。
    '''
    account = StringField()
    password = StringField()
    user_type = IntField(default=0)

    # 用户文档权限
    param_limit = ListField(DictField())
    ''' 公司名'''
    companyname = StringField(unique=True)
    # 默认的api名字的顺序
    api_type_sort = ListField()

    # 注册时间，接入时间
    no_get_api_time = DateTimeField(default=datetime.datetime.now())
    # 包含了该公司所有的包月接口,
    monthly = ListField(default=[])


class ApiList(DynamicDocument):
    """接口表"""
    # 接口的名字, 中文表示, 给前端展示
    api_name = StringField(required=True)
    # icon 地址
    icon_link = StringField()
    # icon 对应的应用接口说明
    icon_des = StringField()
    # 接口类型,用来和 数据聚合的表 对接
    # 接口大类
    interface = StringField()
    # 接口小类
    api_type = StringField()
    # 应用接口图例
    img = StringField()
    # 管理端需要增加部分字段
    # 测试状态 {app_key1: 1, app_key2: 0}
    measure_status = DictField()
    # 测试数量
    measure_count = DictField()
    # 正式状态
    offical_status = DictField()
    # 接口是否已经使用， 接口本身的状态，不关乎用户
    # 当 is_open 为 0 的时候， 表示 接口还在开发中，此时measure_status 表示是否对用户显示。
    # 当is_open为１时，表示是否可测试状态
    is_open = IntField()
    meta = {
        "collection": "apilist"
    }
    # 所有需要进行权限控制的字段进行保存，而不是放进配置文件中
    # 每一个元素目前都是一个字典
    '''{'description': u'是否结婚',
            'name': u'isMarried'
            xxx}
    '''
    all_auth_field = ListField()

    # api babel 接口标签
    label = ListField()

    # 后面迭代版本如果需要增加新的字段， 推荐使用ext_property开头，以表示扩展属性
    # 扩展属性， 表示是否 使用到模块中
    ext_property_used = BooleanField(default=False)

    # 用来设置事务
    pendingTransactions = ListField(default=[])

    # 这个是一个默认的时间, 每次不同的用户会进行覆盖
    ext_property_default_time = DateTimeField(
        default=datetime.datetime.now(), required=True)
    # 存储每个用户的时间
    # {'user1': '2016-08-09 08:00:00'}
    ext_property_user_time = DictField()
    # 渠道
    channel = StringField()
    # 计费方式
    billing = StringField()
    # 备注
    remark = StringField()
    # 第三方权限
    '''
    {
      'method': 'tianxing_idcard',
      'channel': u'天行',
      "weight": 0.1
    }
    '''
    three_auth = ListField()


class RequestRecord(DynamicDocument):

    app_key = StringField()

    create_time = DateTimeField()

    interface = StringField()

    params = DictField()

    result = DynamicField()

    match = IntField()

    success = IntField()

    api_type = StringField()

    repeat = IntField()

    cache = IntField()

    meta = {
        'collection': 'request_record',
        'indexes': [
            [('api_type', 1)],
            [('app_key', 1)],
            [('create_time', 1)],
            [('success', 1)],
            [('match', 1)]
        ]
    }


class OperatorRecord(DynamicDocument):

    # 创建时间
    create_time = IntField()
    # 手机号
    phone = StringField()
    # token
    uuid = StringField()
    # operator data
    operator_data = DynamicField()
    # operator_detail_data
    operator_detail = DynamicField()
    # 运营商
    operator = StringField()
    # name
    name = StringField()
    #idcard
    idcard = StringField()
    # callback
    callback = StringField()
    # 授权状态
    auth_status = IntField()

    meta = {
        "collections": 'operator_record',
        'indexes': [
            "uuid",
            "create_time",
            "phone"
        ],
        "index_background": True,
    }


class RequestRecordIn(DynamicDocument):
    """接入接口的记录"""

    app_key = StringField()

    create_time = DateTimeField()
    # api 大的分类
    # 接口大类
    interface = StringField()

    params = DictField()

    result = DynamicField()
    # 1 是成功
    success = IntField()
    # 匹配
    match = IntField()
    # 接口小的分类
    # 接口小分类, 统一以下划线来分开
    api_type = StringField()
    repeat = IntField()

    # 第三方类型
    in_type = StringField()
    # 记录查询时间
    timeout = DynamicField()

    meta = {
        'collection': 'request_record_in',
        'indexes': [
            [('api_type', 1)],
            [('app_key', 1)],
            [('create_time', 1)],
            [('success', 1)],
            [('match', 1)],
            [('in_type', 1)],
        ]
    }


class ApiListIn(DynamicDocument):
    """接入接口表"""
    # 接口的名字, 中文表示, 给前端展示
    api_name = StringField(unique=True)
    # 接口类型,用来和 数据聚合的表 对接
    # 接口大类
    interface = StringField(default="interface")
    # 接口小类
    api_type = StringField()
    # 接入接口小类
    in_type = StringField(unique=True)
    # 渠道
    channel = StringField()
    icon_link = StringField()

    meta = {
        "collection": "apilistin"
    }
