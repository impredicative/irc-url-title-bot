import logging
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
    def handler(irc, hostmask, args):
        # irc:      An 'IRC' object.
        # hostmask: A 'hostmask' object.
        # args:     A list containing the arguments sent to the command.
        #             Everything following the first `:` in the command
        #             is put into one item (args[-1]).
        log.debug('Handler activated: irc=%s, hostmask=%s, args=%s', repr(irc), repr(hostmask), repr(args))
