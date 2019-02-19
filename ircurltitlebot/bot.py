import logging
import threading
from typing import Dict

import miniirc

from . import config

log = logging.getLogger(__name__)


class Bot:
    def __init__(self, user_config: Dict):
        self._user_config = user_config
        self._client = miniirc.IRC(ip=user_config['host'],
                                   port=user_config['ssl_port'],
                                   nick=user_config['nick'],
                                   channels=user_config['channels'],
                                   ssl=True,
                                   debug=True,  # TODO: Eventually set debug=False
                                   ns_identity=f"{user_config['nick']} {user_config['nick_password']}",
                                   quit_message='',
                                   )


@miniirc.Handler('PRIVMSG')
def _handler(irc, hostmask, args):
    log.debug('Handling PRIVMSG: num_threads=%s, hostmask=%s, args=%s', threading.active_count(), hostmask, args)
    user, _ident, _hostname = hostmask
    address = args[0]
    msg = args[-1]
    assert msg.startswith(':')
    msg = msg[1:]
    irc.msg(address, msg * 2)
