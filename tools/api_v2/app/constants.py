# -*- coding: utf-8 -*-


class Code:
    """错误码"""

    SUCCESS = 1200
    SUCCESS_NOT_DATA = 1230
    MISSPARAM = 1002
    DATAERROR = 1005
    ICREDITEMPTY = 1006
    TSEPIRE = 1201
    TIMEOUTERROR = 1202
    TIMEOUT_ERROR = 1202
    INTERERROR = 1203
    INTER_ERROR = 1203
    VERIFYDENIED = 2000
    OVER_TEST = 2001
    SEARCH_ERROR = 2002
    KEYWORD_ERROR = 2003
    OTHER_ERROR = 2004
    UPDATE_ERROR = 2005
    SERVERS_ERROR = 2006
    PERMISSIONDENIED = 1301
    TIMEFORMATERROR = 1302
    TIMEFORMAT_ERROR = 1302
    INVALID_TEL = 1303
    MISSSIGN = 1304
    MISSAPPKEY = 1305
    IPERROR = 1306
    ERRORTIMESTAMP = 1307
    ERRORGET = 1308
    PERMISSIONTEST = 1309
    SUCCESS_RECORED = 1
    FAIL_PECORED = 0
    SIGN_FAILUER = 1310
    PARAM_ERROR = 1311
    FILE_IS_BIG = 1400
    UNQUALIFIED_PHOTO = 1402
    DECRYPT_FAILD = 1403
    SEARCH_LATER = 1404

    MSG = {
        SUCCESS: u'成功',
        SUCCESS_NOT_DATA: u'请求成功但是没有数据',
        MISSPARAM: u'没有传递必填参数',
        DATAERROR: u'数据库处理数据错误',
        VERIFYDENIED: u'验证失败',
        ICREDITEMPTY: u'该企业不存在',
        TIMEOUTERROR: u'内部接口请求超时',
        TIMEOUT_ERROR: u'内部接口请求超时',
        INTERERROR: u'内部接口请求错误',
        INTER_ERROR: u'内部接口请求错误',
        TSEPIRE: u'时间过期',
        PERMISSIONDENIED: u'没有权限',
        TIMEFORMATERROR: u'时间格式错误',
        TIMEFORMAT_ERROR: u'时间格式错误',
        INVALID_TEL: u'无效的手机号密文',
        MISSSIGN: u'没有签名',
        MISSAPPKEY: u'没有app_key',
        IPERROR: u'ip 无效',
        ERRORTIMESTAMP: u'时间戳格式不对',
        ERRORGET: u'请求方式不对',
        OVER_TEST: u'超过测试条数',
        PERMISSIONTEST: u'没有测试或者正式权限',
        SERVERS_ERROR: u'服务器出错',
        SEARCH_ERROR: u'查询失败',
        KEYWORD_ERROR: u'请求参数包含违禁词',
        OTHER_ERROR: u'其他错误',
        UPDATE_ERROR: u'接口升级维护',
        SIGN_FAILUER: "验签失败",
        PARAM_ERROR: "参数错误",
        FILE_IS_BIG: "文件过大",
        UNQUALIFIED_PHOTO: "照片不合格",
        DECRYPT_FAILD: "解码照片失败",
        SEARCH_LATER: "操作有风险，稍后再试"
    }


class ZmCode:
    """芝麻信用专用错误码"""

    PRODUCT_ERROR = 5001
    AUTHENTICATION_FAIL = 5002
    TRANSACTION_ID = 5003
    INVALID_ARRANGEMENT = 5004
    OPENID_INVALID = 5005
    PAEAMETER_INVALID = 5006
    PRODUCT_NULL = 5007
    SYSTEM_ERROR = 5008
    TRANSACTION_CLOSE = 5009
    TRANSACTION_EXPIRED = 5010
    TRANSACTION_REPEAT = 5011

    MSG = {
        PRODUCT_ERROR: "输入的产品码不正确",
        AUTHENTICATION_FAIL: "鉴权失败",
        TRANSACTION_ID: "业务流水号不正确",
        INVALID_ARRANGEMENT: "无有效合约",
        OPENID_INVALID: "open_id参数错误",
        PAEAMETER_INVALID: "参数错误",
        PRODUCT_NULL: "产品码为空",
        SYSTEM_ERROR: "系统错误",
        TRANSACTION_CLOSE: "交易已关闭",
        TRANSACTION_EXPIRED: "业务流水号已过期",
        TRANSACTION_REPEAT: "相同业务流水号但业务参数不一致，请求被拒绝",
        }
    zm_code = {
        "ZMCREDIT.api_product_not_match": 5001,
        "ZMCREDIT.authentication_fail": 5002,
        "ZMCREDIT.invalid_transaction_id": 5003,
        "ZMCREDIT.no_valid_arrangement": 5004,
        "ZMCREDIT.openid_parameter_invalid": 5005,
        "ZMCREDIT.parameter_invalid": 5006,
        "ZMCREDIT.product_code_is_null": 5007,
        "ZMCREDIT.system_error": 5008,
        "ZMCREDIT.transaction_close": 5009,
        "ZMCREDIT.transaction_id_expired": 5010,
        "ZMCREDIT.transaction_id_repeat": 5011
    }
