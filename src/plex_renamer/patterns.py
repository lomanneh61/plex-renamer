import re
from typing import Iterable

DEFAULT_PATTERNS: list[re.Pattern] = [
    re.compile(r"^(?P<track>\d+)\s*[-.]\s*(?P<title>.+)$"),
    re.compile(r"^(?P<track>\d+)[.)]\s*(?P<title>.+)$"),
    re.compile(r"^(?P<track>\d+)\.(?P<title>.+)$"),
    re.compile(r"^(?P<track>\d+)\s*\(?[a-zA-Z]*\)?[- ]+(?P<title>.+)$"),
    re.compile(r"^cd(?P<disc>\d+)[-_ ]*track(?P<track>\d+)$"),
    re.compile(r"^(?P<track>\d+)\+(?P<title>.+)$"),
    re.compile(r"^(?P<track>\d+)\s+(?P<title>.+)$"),
    re.compile(r"^(?P<title>.+)$"),
]


def compile_patterns(pattern_strings: Iterable[str] | None) -> list[re.Pattern]:
    if not pattern_strings:
        return DEFAULT_PATTERNS
    return [re.compile(p) for p in pattern_strings]
