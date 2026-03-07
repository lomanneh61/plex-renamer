# detection.py

from __future__ import annotations
import re
from pathlib import Path
from typing import Optional, Tuple

from .title_normalizer import normalize_title


# Track prefix patterns (real track numbers)
TRACK_PREFIX_PATTERNS = [
    r"^[\s\-_]*(\d{1,3})[\s\-_]+",   # 01 - Title, 01_ Title, 01 Title
    r"[Tt]rack[\s\-_]*(\d{1,3})",    # Track 01
    r"\((\d{1,3})\)",                # (01)
    r"\[(\d{1,3})\]",                # [01]
]


def extract_track_prefix(name: str) -> Optional[int]:
    """Extract real track prefix patterns."""
    for pat in TRACK_PREFIX_PATTERNS:
        m = re.search(pat, name)
        if m:
            return int(m.group(1))
    return None


def extract_last_number(name: str) -> Optional[int]:
    """Extract the last number in the filename (e.g., 010 → 10)."""
    nums = re.findall(r"(\d{1,4})", name)
    if not nums:
        return None
    return int(nums[-1])


def strip_number_from_title(name: str, number: int) -> str:
    """Remove the extracted number from the title."""
    # Remove standalone number or number inside words
    cleaned = re.sub(rf"\b{number}\b", "", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def detect_all(path: Path) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[int], Optional[int]]:
    """
    Detect artist, album, title, track, disc.
    """

    # Metadata reader (if you have one)
    artist = None
    album = None
    title = None
    track = None
    disc = None

    # --- 1. Try metadata first ---
    # (Your metadata reader goes here if implemented)

    # --- 2. Try filename track prefix ---
    stem = path.stem
    prefix_track = extract_track_prefix(stem)
    if prefix_track is not None:
        track = prefix_track
        # Remove prefix from title
        title = re.sub(r"^[\s\-_]*\d{1,3}[\s\-_]+", "", stem)

    # --- 3. If still no track, extract last number ---
    if track is None:
        last_num = extract_last_number(stem)
        if last_num is not None:
            track = last_num
            title = strip_number_from_title(stem, last_num)

    # --- 4. If still no title, fallback to stem ---
    if not title:
        title = stem

    # --- 5. Normalize title ---
    title = normalize_title(title)

    return artist, album, title, track, disc
