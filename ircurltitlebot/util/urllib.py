"""urllib utilities."""

from urllib.parse import urlparse

_LOCALHOST_NAMES = {"127.0.0.1", "localhost", "ip6-localhost", "ip6-loopback", "ip6-allnodes", "ip6-allrouters"}


def validate_parsed_url(url: str) -> bool:
    """Return whether a URL is valid after parsing it."""
    parsed = urlparse(url.casefold())
    return not ((parsed.scheme not in ("http", "https", "")) or (parsed.netloc in _LOCALHOST_NAMES) or ((parsed.netloc == "") and (parsed.path in _LOCALHOST_NAMES)))
