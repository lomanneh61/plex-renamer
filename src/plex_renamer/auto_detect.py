# auto_detect.py

from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class AutoDetectResult:
    artist: Optional[str]
    album: Optional[str]
    title: Optional[str]
    track: Optional[str]
    disc: Optional[str]


# Common separators in your dataset
SEPARATORS = r"[-+_.]|\s{2,}|--"


# Speaker-like patterns (beginning or end)
SPEAKER_PATTERNS = [
    r"(?P<speaker>(Sheikh|Imam|Ustadh|Ustaaz|Maulana)\s+[A-Za-z]+(?:\s+[A-Za-z]+)*)",
    r"(?P<speaker>[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})",  # Generic 2–4 word names
]

# Album-like patterns
ALBUM_HINTS = [
    r"Mandinka",
    r"Collection",
    r"Topics",
    r"Lecture",
    r"Series",
    r"Guidance",
    r"Faith",
]

# Disc patterns
DISC_PATTERNS = [
    r"cd\s*(?P<disc>\d+)",
    r"disc\s*(?P<disc>\d+)",
    r"vol\s*(?P<disc>\d+)",
    r"(?P<disc>\d+)-\d+",  # 2-03
]


def _clean(s: str | None) -> Optional[str]:
    if not s:
        return None
    s = s.replace("+", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def detect_track(filename: str) -> Optional[str]:
    m = re.match(r"(?P<track>\d{1,2})\s*[-_. ]", filename)
    if m:
        return m.group("track").zfill(2)
    return None


def detect_disc(filename: str) -> Optional[str]:
    for pat in DISC_PATTERNS:
        m = re.search(pat, filename, flags=re.IGNORECASE)
        if m:
            return str(m.group("disc")).zfill(2)
    return None


def detect_speaker(filename: str) -> Optional[str]:
    for pat in SPEAKER_PATTERNS:
        m = re.search(pat, filename, flags=re.IGNORECASE)
        if m:
            return _clean(m.group("speaker"))
    return None


def detect_album(filename: str) -> Optional[str]:
    for hint in ALBUM_HINTS:
        if re.search(hint, filename, flags=re.IGNORECASE):
            return _clean(hint)
    return None


def detect_title(filename: str) -> Optional[str]:
    # Remove track numbers
    s = re.sub(r"^\d{1,2}[-_. ]+", "", filename)

    # Remove disc hints
    s = re.sub(r"(cd|disc|vol)\s*\d+", "", s, flags=re.IGNORECASE)

    # Remove speaker names
    for pat in SPEAKER_PATTERNS:
        s = re.sub(pat, "", s, flags=re.IGNORECASE)

    # Remove leftover separators
    s = re.sub(SEPARATORS, " ", s)

    s = _clean(s)
    return s if s else None


def auto_detect(path: Path) -> AutoDetectResult:
    name = path.stem

    track = detect_track(name)
    disc = detect_disc(name)
    speaker = detect_speaker(name)
    album = detect_album(name)
    title = detect_title(name)

    return AutoDetectResult(
        artist=speaker,
        album=album,
        title=title,
        track=track,
        disc=disc,
    )
