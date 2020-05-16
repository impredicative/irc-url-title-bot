"""Print title for URL using CLI provided instance config."""
# pylint: disable=import-error,invalid-name
import logging

from ircurltitlebot.__main__ import load_config
from ircurltitlebot.title import url_title_reader

URL = "https://www.aliexpress.com/item/33043594353.html"  # Customize

log = logging.getLogger(__name__)
load_config()

title = url_title_reader.title(URL, "")
log.info(f"Title for {URL} is: {title}")
