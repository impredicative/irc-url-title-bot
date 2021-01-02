"""Customized URL title reader."""
import logging
import re
from typing import Optional

import urltitle

from . import config

log = logging.getLogger(__name__)


class URLTitleReader:
    """Customized URL title reader."""

    def __init__(self) -> None:
        self._url_title_reader = urltitle.URLTitleReader(verify_ssl=False)

    def title(self, url: str, channel: str) -> Optional[str]:
        """Return an optional page title of the given URL."""
        site = self._url_title_reader.netloc(url)
        site_config = config.INSTANCE.get("sites", {}).get(site, {})

        # Skip blacklisted channel for site
        if channel.casefold() in (c.casefold() for c in site_config.get("blacklist", {}).get("channels", [])):
            log.info("Skipping blacklisted channel %s for site %s.", channel, site)
            return None

        title = self._url_title_reader.title(url)

        # Skip blacklisted title for site
        blacklist = site_config.get("blacklist", {})
        if title == blacklist.get("title") or ((bl_re := blacklist.get("title_re")) and re.search(bl_re, title)):  # pylint: disable=used-before-assignment
            log.info("Skipping blacklisted title %s for site %s.", repr(title), site)
            return None

        # Substitute title for site
        for format_config in site_config.get("format", []):
            format_params = {"url": url, "title": title}
            for key, pattern in format_config.get("re", {}).items():
                match = re.search(pattern, format_params[key])
                if not match:
                    break
                format_params.update(match.groupdict())
            else:
                updated_title = format_config.get("str", {}).get("title", "{title}").format_map(format_params)
                if title != updated_title:
                    log.info("Substituting title %s with %s.", repr(title), repr(updated_title))
                    title = updated_title
                break

        return title


url_title_reader = URLTitleReader()  # pylint: disable=invalid-name
