"""urllib utilities."""

from urllib.parse import urlparse

_LOCALHOST_NAMES = {"127.0.0.1", "localhost", "ip6-localhost", "ip6-loopback", "ip6-allnodes", "ip6-allrouters"}


def validate_parsed_url(url: str) -> bool:
    """Return whether a URL is valid after parsing it."""
    parsed = urlparse(url.casefold())
    is_scheme_valid = parsed.scheme in ("http", "https", "")
    is_netloc_valid = parsed.netloc not in _LOCALHOST_NAMES
    is_path_valid = (parsed.path not in _LOCALHOST_NAMES) if (parsed.netloc == "") else True
    return is_scheme_valid and is_netloc_valid and is_path_valid
