import logging.config
from pathlib import Path
from typing import Dict


def configure_logging() -> None:
    logging.config.dictConfig(LOGGING)
    log = logging.getLogger(__name__)
    log.debug('Logging is configured.')


INSTANCE: Dict = {}  # Set from JSON config file.
MAX_WORKERS_PER_CHANNEL = 3
PACKAGE_NAME = Path(__file__).parent.stem
TITLE_PREFIX = '⤷'
TITLE_TIMEOUT = 60

LOGGING = {  # Ref: https://docs.python.org/3/howto/logging.html#configuring-logging
    'version': 1,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(thread)x-%(threadName)s:%(name)s:%(lineno)d:%(funcName)s:%(levelname)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        PACKAGE_NAME: {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'urltitle': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}

configure_logging()
