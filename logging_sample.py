from logging import (
    getLogger,
    Formatter,
    FileHandler,
    StreamHandler,
    DEBUG,
    ERROR
)

import requests

logger = getLogger(__name__)

default_format = '[%(levelname)s] %(asctime)s %(name)s %(filename)s:%(lineno)d %(message)s'
default_formatter = Formatter(default_format)
funcname_formatter = Formatter(default_format + '(%(funcName)s)')

log_stream_handler = StreamHandler()
log_stream_handler.setFormatter(default_formatter)
log_stream_handler.setLevel(DEBUG)

log_file_handler = FileHandler(filename="crawler.log")
log_file_handler.setFormatter(funcname_formatter)
log_file_handler.setLevel(ERROR)

logger.setLevel(DEBUG)
logger.addHandler(log_stream_handler)
logger.addHandler(log_file_handler)

def logging_example():
    logger.info('Start Crowler')
    logger.warning('Dont crowler because of Outer Site')
    logger.error('Not Found')

    try:
        r = requests.get('#invalid_url', timeout=1)
    except requests.exceptions.RequestException as e:
        logger.exception('Threw Error during requests: %r', e)

if __name__ == '__main__':
    logging_example()
    