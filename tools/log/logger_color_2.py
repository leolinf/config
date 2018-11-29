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
            fs = LEVEL_COLOR[record.levelno] + "%s\n" + '\33[0m'
            print(logging._unicode)
            if not logging._unicode:
                stream.write(fs % msg)
            else:
                try:
                    if (isinstance(msg, unicode) and getattr(stream, 'encoding', None)):
                        ufs = fs.decode(stream.encoding)
                        try:
                            stream.write(ufs % msg)
                        except UnicodeEncodeError:
                            stream.write((ufs % msg).encode(stream.encoding))
                    else:
                        stream.write(fs % msg)
                except UnicodeError:
                    stream.write(fs % msg.encode("UTF-8"))
            self.flush()

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


logging.ScreenHandler = ScreenHandler
logger = logging.getLogger()
handler = logging.ScreenHandler()
formatter = logging.Formatter('%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s')
handler.setFormatter(formater)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
