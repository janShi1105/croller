"""Config File"""

import os

BASE_DIR = path.realpath(path.dirname(__file__))
LOG_DIR = path.join(BASE_DIR,'logs')

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING_CONFIG = {
    'version': 1,

    'disable_existing_loggers': True,

    'formatters': {
        'default': {
            '()': 'colorlog.ColoredFormatter',
            'format': '\t'.join([
                "%(log_color)s[%(levelname)s]",
                "asctime:%(asctime)s",
                "process:%(process)d",
                "thread:%(thread)d",
                "module:%(module)s",
                "%(oathname)s:%(lineno)d",
                "message:%(message)s"
            ]),
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors':{
                'DEBUG': 'bold_black',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red'
            },
        },
        'simple': {
            '()': 'colorlog.ColoredFormatter',
            'format': '\t'.join([
                "%(log_colors)s[%(levelname)s]",
                "%(asctime)s",
                "%(message)s"
                ]),
                'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors':{
                'DEBUG': 'bold_black',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red'
            },
        },
        'query': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(cyan)s[SQL] %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.RotatingFileHandler',
            'filename': path.join(LOG_DIR, 'crawler.log'),
            'formatter': 'default',
            'backupCount': 3,
            'maxBytes': 1024 * 1024 * 2
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'console_simple': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'query': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'query'
        },
    },
    'root': {
        'handlers': ['file', 'console_simple'],
        'level': 'DEBUG'
    },

    'loggers': {
        'celery': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False
        },
        'my_project': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagete': False
        }
    }
}