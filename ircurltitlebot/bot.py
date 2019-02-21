import concurrent.futures
from itertools import groupby
import logging
import threading
from time import monotonic
# noinspection PyUnresolvedReferences
from queue import SimpleQueue  # type: ignore
from typing import Dict, List, NoReturn, Tuple, Optional

from miniirc import Handler as IRCHandler, IRC
from urltitle import URLTitleReader
from urlextract import URLExtract

from . import config

log = logging.getLogger(__name__)
url_extractor = URLExtract()
url_title_reader = URLTitleReader()


class Bot:
    EXECUTORS: Dict[str, concurrent.futures.ThreadPoolExecutor] = {}
    QUEUES: Dict[str, SimpleQueue] = {}

    def __init__(self):
        log.debug('Initializing bot.')

        # Setup channels
        channels = config.INSTANCE['channels']
        channels_str = ', '.join(channels)
        active_count = threading.active_count
        log.debug('Setting up threads and queues for %s channels (%s) with %s currently active threads.',
                  len(channels), channels_str, active_count())
        for channel in channels:
            log.debug('Setting up threads and queue for %s.', channel)
            self.EXECUTORS[channel] = concurrent.futures.ThreadPoolExecutor(max_workers=config.MAX_WORKERS_PER_CHANNEL,
                                                                            thread_name_prefix=f'URLHandler-{channel}')
            self.QUEUES[channel] = SimpleQueue()
            threading.Thread(target=_handle_titles, name=f'TitlesHandler-{channel}', args=(channel,)).start()
            log.info('Finished setting up threads and queue for %s with %s currently active threads.',
                     channel, active_count())
        log.info('Finished setting up threads and queues for %s channels (%s) with %s currently active threads.',
                 len(channels), channels_str, active_count())

    def serve(self) -> NoReturn:  # type: ignore
        log.debug('Serving bot.')
        instance = config.INSTANCE
        IRC(ip=instance['host'],
            port=instance['ssl_port'],
            nick=instance['nick'],
            channels=instance['channels'],
            ssl=True,
            debug=False,
            ns_identity=f"{instance['nick']} {instance['nick_password']}",
            quit_message='',
            )


def _handle_url(irc: IRC, channel: str, user: str, url: str) -> Optional[Tuple[IRC, str, str, str]]:  # type: ignore
    start_time = monotonic()
    try:
        title = url_title_reader.title(url)
    except Exception as exc:
        log.error('Error reading title from URL %s in message from %s in %s in %.1fs: %s',
                  url, user, channel, monotonic() - start_time, exc)
    else:
        log.debug('Returning title "%s" from URL %s in message from %s in %s in %.1fs.',
                  title, url, user, channel, monotonic() - start_time)
        return irc, user, url, title


def _handle_titles(channel: str) -> NoReturn:
    queue = Bot.QUEUES[channel]
    title_timeout = config.TITLE_TIMEOUT
    title_prefix = config.TITLE_PREFIX
    active_count = threading.active_count
    log.debug('Starting titles handler for %s.', channel)
    while True:
        url_future = queue.get()
        start_time = monotonic()
        try:
            result = url_future.result(timeout=title_timeout)
        except concurrent.futures.TimeoutError:
            log.error('Result timed out after %.1fs given a timeout of %.1fs.', monotonic() - start_time)
        else:
            if result is None:
                continue
            irc, user, url, title = result
            msg = f'{title_prefix} {title}'
            irc.msg(channel, msg)
            log.info('Sent outgoing message for %s in %s in %.1fs having content "%s" for URL %s with %s active '
                     'threads.',
                     user, channel, monotonic() - start_time, msg, url, active_count())


@IRCHandler('PRIVMSG')
def _handle_msg(irc: IRC, hostmask: Tuple[str, str, str], args: List[str]) -> None:
    log.debug('Handling incoming message: hostmask=%s, args=%s', hostmask, args)
    user, _ident, _hostname = hostmask
    channel = args[0]
    msg = args[-1]
    assert msg.startswith(':')
    msg = msg[1:]

    # Ignore ignored users
    if user in config.INSTANCE['ignores']:
        return

    # Ignore and log PMs
    if channel not in config.INSTANCE['channels']:
        assert channel == config.INSTANCE['nick']
        log.warning('Ignoring incoming private message from %s having content: %s', user, msg)
        return

    # Extract URLs
    try:
        urls = url_extractor.find_urls(msg, only_unique=False)  # Assumes returned URLs have same order as in message.
        # Note: Due to a bug in urlextract==0.9, a URL can erroneously be returned twice.
        # Refer to https://github.com/lipoja/URLExtract/issues/32
        urls = [url[0] for url in groupby(urls)]  # Guarantees consecutive uniqueness as a workaround for above bug.
        # urls = list(dict.fromkeys(urls))  # Guarantees uniqueness while preserving ordering.

    except Exception as exc:
        log.error('Error extracting URLs in message from %s in %s having content "%s". The error is: %s',
                  user, channel, msg, exc)
        return
    if urls:
        urls_str = ', '.join(urls)
        log.debug('Incoming message from %s in %s has %s URLs: %s', user, channel, len(urls), urls_str)
    else:
        return

    # Add jobs
    executor = Bot.EXECUTORS[channel]
    queue = Bot.QUEUES[channel]
    for url in urls:
        url_future = executor.submit(_handle_url, irc, channel, user, url)
        queue.put(url_future)
    log.debug('Queued %s URLs for message from %s in %s: %s', len(urls), user, channel, urls_str)
