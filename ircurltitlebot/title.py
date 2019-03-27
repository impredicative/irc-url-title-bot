import logging
import re
from typing import Optional

import urltitle

from . import config

log = logging.getLogger(__name__)


class URLTitleReader:

    def __init__(self) -> None:
        self._url_title_reader = urltitle.URLTitleReader(verify_ssl=False)

    def title(self, url: str) -> Optional[str]:
        netloc = self._url_title_reader.netloc(url)
        netloc_config = config.INSTANCE.get('sites', {}).get(netloc, {})
        netloc_config_py = config.NETLOC_OVERRIDES.get(netloc, {})
        title = self._url_title_reader.title(url)

        # Skip blacklisted title
        if title == netloc_config.get('blacklist', {}).get('title'):
            log.info('Skipping blacklisted title %s for site %s.', repr(title), netloc)
            return None

        # Substitute title
        for condition_dict, title_format in netloc_config_py.get('title_subs', []):
            format_params = {'url': url, 'title': title}
            for condition_key, condition_val in condition_dict.items():
                match = re.search(condition_val, format_params[condition_key])
                if not match:
                    break
                format_params.update(match.groupdict())
            else:
                title = title_format.format(**format_params)
                if title != format_params['title']:
                    log.info('Substituted title %s with %s.', repr(format_params['title']), repr(title))

        return title


url_title_reader = URLTitleReader()
