# -*- coding: utf-8 -*-
import logging
from logging import DEBUG, INFO, WARN, ERROR, FATAL, NOTSET

LEVEL_COLOR = {
    DEBUG: '\33[2;39m',
    INFO: '\33[0;36m',
    WARN: '\33[0;33m',
    ERROR: '\33[0;35m',
    FATAL: '\33[1;31m',
    NOTSET: ''
}


class ScreenHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            # 设置颜色
            fs = LEVEL_COLOR[record.levelno] + "%s" + '\33[0m'
            stream.write(fs % msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


logging.ScreenHandler = ScreenHandler

logger = logging.getLogger()
handler = logging.ScreenHandler()
formatter = logging.Formatter('%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
