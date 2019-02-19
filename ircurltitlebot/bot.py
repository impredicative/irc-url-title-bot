import logging
import threading
from typing import List, Tuple

import miniirc

from . import config

log = logging.getLogger(__name__)


class Bot:
    def __init__(self) -> None:
        instance = config.INSTANCE
        miniirc.IRC(ip=instance['host'],
                    port=instance['ssl_port'],
                    nick=instance['nick'],
                    channels=instance['channels'],
                    ssl=True,
                    debug=False,
                    ns_identity=f"{instance['nick']} {instance['nick_password']}",
                    quit_message='',
                    )


@miniirc.Handler('PRIVMSG')
def _handler(irc: miniirc.IRC, hostmask: Tuple[str, str, str], args: List[str]) -> None:
    log.debug('Handling incoming message: num_threads=%s, hostmask=%s, args=%s',
              threading.active_count(), hostmask, args)
    user, _ident, _hostname = hostmask
    address = args[0]
    msg = args[-1]
    assert msg.startswith(':')
    msg = msg[1:]

    if address not in config.INSTANCE['channels']:
        assert address == config.INSTANCE['nick']
        log.info('Ignoring incoming private message from %s: %s.', user, msg)
        return

    irc.msg(address, f'{config.TITLE_PREFIX} {msg}')
