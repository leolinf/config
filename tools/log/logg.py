# -*- coding: utf-8 -*-
import logging
from logging.config import dictConfig


logging_config = dict(
    version=1,
    formatters={
        'f': {
            'format': '%(asctime)s %(process)d,%(threadName)s,%(thread)d,%(filename)s:%(lineno)d [%(levelname)s] %(message)s',
        }
    },
    handlers={
        'h': {
            'class': 'logging.ScreenHandler',
            'formatter': 'f',
            'level': logging.DEBUG
        }
    },
    root={
        'handlers': ['h'],
        'level': logging.DEBUG,
    },
)
# 方式1
dictConfig(logging_config)
logger = logging.getLogger()

# 方式2
# logger = logging.getLogger()
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.DEBUG)


def main():
    logger.critical("critical")
    logger.error("error")
    logger.warn("warn")
    logger.warning('warning')
    logger.info('info')
    logger.debug("debug")

    try:
        return 1 / 0
    except Exception:
        logger.error("Something bad happened", exc_info=True)


if __name__ == '__main__':
    main()
