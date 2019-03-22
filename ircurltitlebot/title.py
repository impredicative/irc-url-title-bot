import logging
import re
from typing import cast, Dict

import urltitle

from . import config

log = logging.getLogger(__name__)


class URLTitleReader:

    def __init__(self) -> None:
        self._url_title_reader = urltitle.URLTitleReader(verify_ssl=False)

    def title(self, url: str) -> str:
        netloc = self._url_title_reader.netloc(url)
        overrides = config.NETLOC_OVERRIDES.get(netloc, {})
        overrides = cast(Dict, overrides)
        title = self._url_title_reader.title(url)

        # Substitute title
        for condition_dict, title_format in overrides.get('title_subs', []):
            format_params = {'url': url, 'title': title}
            for condition_key, condition_val in condition_dict.items():
                match = re.search(condition_val, format_params[condition_key])
                if not match:
                    break
                format_params.update(match.groupdict())
            else:
                title = title_format.format(**format_params)
                if title != format_params['title']:
                    log.info('Substituted title "%s" with "%s".', format_params['title'], title)

        # Handle blacklisted title
        if title in overrides.get('title_blacklist', set()):
            log.info('Replaced blacklisted title "%s" for %s with an empty title.', title, netloc)
            title = ''

        return title


url_title_reader = URLTitleReader()
