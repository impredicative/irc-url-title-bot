import logging
import threading
from time import monotonic
from typing import List, NoReturn, Tuple

import miniirc
from urltitle import URLTitleReader
from urlextract import URLExtract

from . import config

log = logging.getLogger(__name__)
url_extractor = URLExtract()
url_title_reader = URLTitleReader()


class Bot:
    def serve(self) -> NoReturn:  # type: ignore
        log.debug('Serving bot.')
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
    msg_time = monotonic()
    log.debug('Handling incoming message: num_threads=%s, hostmask=%s, args=%s',
              threading.active_count(), hostmask, args)
    user, _ident, _hostname = hostmask
    channel = args[0]
    msg = args[-1]
    assert msg.startswith(':')
    msg = msg[1:]

    # Log but ignore unsolicited messages
    if channel not in config.INSTANCE['channels']:
        assert channel == config.INSTANCE['nick']
        log.warning('Ignoring incoming private message from %s having content: %s', user, msg)
        return

    # Extract URLs
    try:
        urls = url_extractor.find_urls(msg, only_unique=True)
    except Exception as exc:
        log.error('Error extracting URLs in message from %s in %s having content "%s". The error is: %s',
                  user, channel, msg, exc)
        return
    if urls:
        log.info('Incoming message from %s in %s having content "%s" has %s URLs: %s',
                 user, channel, msg, len(urls), ', '.join(urls))

    # Reply with titles
    for url in urls:
        try:
            title = url_title_reader.title(url)
        except Exception as exc:
            log.error('Error reading title from URL %s in message from %s in %s having content "%s". The error is: %s',
                      url, user, channel, msg, exc)
        else:
            reply = f'{config.TITLE_PREFIX} {title}'
            irc.msg(channel, reply)
            log.info('Sent outgoing message for %s in %s in %.1fs having content "%s" for URL %s in response to '
                     'incoming message: %s',
                     user, channel, monotonic() - msg_time, reply, url, msg)
