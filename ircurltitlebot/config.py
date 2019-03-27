import logging.config
from pathlib import Path
from typing import Dict


def configure_logging() -> None:
    logging.config.dictConfig(LOGGING)
    log = logging.getLogger(__name__)
    log.debug('Logging is configured.')


INSTANCE: Dict = {}  # Set from YAML config file.
PACKAGE_NAME = Path(__file__).parent.stem

ALERTS_CHANNEL_FORMAT_DEFAULT = '##{nick}-alerts'
MAX_WORKERS_PER_CHANNEL = 3
TITLE_PREFIX = '⤷'
TITLE_TIMEOUT = 60

LOGGING = {  # Ref: https://docs.python.org/3/howto/logging.html#configuring-logging
    'version': 1,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(levelname)s %(threadName)s:%(name)s:%(lineno)d:%(funcName)s: %(message)s',
        },  # Note: Use %(thread)x- if needed for thread ID.
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

NETLOC_OVERRIDES = {  # Site-specific overrides (w/o www prefix) as condition-action tuples. Sites must be in lowercase.
    'arxiv.org': {'title_subs': [({'url': r'/pdf/(?P<url_id>.+?)(?:\.pdf)*$'},
                                  '{title} | https://arxiv.org/abs/{url_id}'),
                                 ({'url': r'/abs/(?P<url_id>.+?)$'},
                                  '{title} | https://arxiv.org/pdf/{url_id}')]},
}

configure_logging()
