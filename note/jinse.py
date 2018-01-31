# -*- coding: utf-8 -*-
import logging
import traceback
import requests
import datetime
import coloredlogs

import pymysql.cursors
from logging.config import dictConfig
from logging import DEBUG, INFO, WARN, ERROR, FATAL, NOTSET

logging_config = dict(
    version = 1,
    formatters = {
        'f': {
                'format':'%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
            }
        },
    handlers = {
        'h': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': logging.DEBUG
            }
        },
    root = {
        'handlers': ['h'],
        'level': logging.DEBUG,
        },
)

#dictConfig(logging_config)
#logger = logging.getLogger()

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG')


logger.critical("critical")
logger.error("error")
logger.warn("warn")
logger.warning('warning')
logger.info('info')
logger.debug("debug")


url = 'http://xxx.com'
host = '127.0.0.1'
port = '3306'
user = 'root'
password = '123456'
database = 'weibit'
now = datetime.datetime.now()

def request():
    try:
        result = requests.get(url, timeout=2).json()
        return result
    except Exception as e:
        traceback.print_exc()
        logger.critical("Error %s", str(e))
        return {}

def data_insert(data):
    try:
        with conn.cursor() as cursor:
            sql = '''INSERT INTO `jinse_sort` (name, symbol, rank, market_capital,
                                               price, available, volume_24h, percent_change_24h,
                                               total, api_updated, created_at, updated_at, insert_time)
                                               VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
            cursor.execute(sql, data)
    except Exception as e:
        traceback.print_exc()
        logger.critical("Error %s", str(e))
        raise

def main():
    global conn
    conn = pymysql.connect(host=host, user=user, password=password, db=database, cursorclass=pymysql.cursors.DictCursor, charset="utf8")
    try:
        resp = request()
        for i in resp.get("data", {}).get("listData", {}).get("list", []):
            data = (i.get("name"), i.get("symbol"),
                    i.get("rank"), i.get("market_capital"), i.get("price"),
                    i.get("available"), i.get("volume_24h"), i.get("percent_change_24h"),
                    i.get("total"), i.get("api_updated"), i.get("created_at"),
                    i.get("updated_at"), now)
            data_insert(data)
        conn.commit()
    except Exception as e:
        traceback.print_exc()
        logger.critical("Error %s", str(e))
        conn.rollback()
        logger.critical("insert fail ...")
        return
    finally:
        conn.close()
    logger.debug("insert success ...")


if __name__ == '__main__':
    main()

# 创建表语句
"""
CREATE TABLE `jinse_sort` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `name`  VARCHAR(255) NOT NULL COMMENT '名称',
    `symbol` VARCHAR(255) NOT NULL COMMENT '标志',
    `rank` SMALLINT(6) COMMENT '金色财经平台排名',
    `market_capital` VARCHAR(255) NOT NULL COMMENT '市值(亿)',
    `price` VARCHAR(255) NOT NULL COMMENT '价格',
    `available` VARCHAR(255) NOT NULL COMMENT '流通数量',
    `volume_24h` VARCHAR(255) NOT NULL COMMENT '24小时成交额',
    `percent_change_24h` VARCHAR(255) NOT NULL COMMENT '24小时涨幅',
    `total` VARCHAR(255) NOT NULL COMMENT '发行总量',
    `api_updated` VARCHAR(255) NOT NULL COMMENT '金色财经接口更新时间',
    `created_at` VARCHAR(255) NOT NULL COMMENT '金色财经接口创建时间',
    `updated_at` VARCHAR(255) NOT NULL COMMENT '刷新页面时间',
    `insert_time` DATETIME NOT NULL COMMENT '更新插入时间',
    PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='测试用的 表';
"""
