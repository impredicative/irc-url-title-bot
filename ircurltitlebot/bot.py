import logging
from typing import Dict

import miniirc

from . import config

log = logging.getLogger(__name__)


class Bot:
    def __init__(self, user_config: Dict):
        log.debug('Initializing bot.')
        self._user_config = user_config
        self._client = miniirc.IRC(ip=user_config['host'],
                                   port=user_config['ssl_port'],
                                   nick=user_config['nick'],
                                   channels=user_config['channels'],
                                   ssl=True,
                                   debug=True,
                                   ns_identity=f"{user_config['nick']} {user_config['nick_password']}",
                                   quit_message='',
                                   )

    def start(self):
        pass
