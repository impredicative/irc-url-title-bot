import logging
import threading
from typing import List, NoReturn, Tuple

import miniirc
from urlextract import URLExtract

from . import config

log = logging.getLogger(__name__)
url_extractor = URLExtract()


class Bot:
    def __init__(self) -> NoReturn:  # type: ignore
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
    channel = args[0]
    msg = args[-1]
    assert msg.startswith(':')
    msg = msg[1:]

    if channel not in config.INSTANCE['channels']:
        assert channel == config.INSTANCE['nick']
        log.info('Ignoring incoming private message from %s: %s.', user, msg)
        return

    try:
        urls = url_extractor.find_urls(msg, only_unique=True)
    except Exception as exc:
        log.error('Error extracting URLs in message from %s in %s having content "%s". The error is: %s',
                  user, channel, msg, exc)
        return

    irc.msg(channel, f'{config.TITLE_PREFIX} {msg}')
