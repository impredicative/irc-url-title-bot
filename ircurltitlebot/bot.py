import logging
from typing import Dict

from . import config

log = logging.getLogger(__name__)


class Bot:
    def __init__(self, user_config: Dict):
        self._user_config = user_config

    def start(self):
        pass
