"""Package configuration."""
import logging.config
import types
from pathlib import Path
from typing import Dict

import ircstyle


def configure_logging() -> None:
    """Configure logging."""
    logging.config.dictConfig(LOGGING)
    log = logging.getLogger(__name__)
    log.debug("Logging is configured.")


INSTANCE: Dict = {}  # Set from YAML config file.
PACKAGE_NAME = Path(__file__).parent.stem
runtime = types.SimpleNamespace()  # Set at runtime.  # pylint: disable=invalid-name

ALERTS_CHANNEL_FORMAT_DEFAULT = "##{nick}-alerts"
MAX_WORKERS_PER_CHANNEL = 3
TITLE_PREFIX = ircstyle.style("⤷", fg="green", reset=True)
TITLE_TIMEOUT = 60

LOGGING = {  # Ref: https://docs.python.org/3/howto/logging.html#configuring-logging
    "version": 1,
    "formatters": {
        "detailed": {"format": "%(asctime)s %(levelname)s %(threadName)s:%(name)s:%(lineno)d:%(funcName)s: %(message)s"},  # Note: Use %(thread)x- if needed for thread ID.
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "level": "DEBUG", "formatter": "detailed", "stream": "ext://sys.stdout"}},
    "loggers": {
        "__main__": {"level": "INFO", "handlers": ["console"], "propagate": False},
        PACKAGE_NAME: {"level": "INFO", "handlers": ["console"], "propagate": False},
        # "urltitle": {"level": "INFO", "handlers": ["console"], "propagate": False},
        # "": {"level": "DEBUG", "handlers": ["console"]},
    },
}

configure_logging()
