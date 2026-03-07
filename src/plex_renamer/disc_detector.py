# disc_detector.py

from __future__ import annotations
import re
from pathlib import Path
from typing import Optional


# Patterns that indicate disc numbers
DISC_PATTERNS = [
    r"cd\s*(?P<disc>\d+)",          # cd2, cd 2
    r"disc\s*(?P<disc>\d+)",        # disc3, disc 3
    r"vol\s*(?P<disc>\d+)",         # vol1, vol 1
    r"volume\s*(?P<disc>\d+)",      # volume 2
    r"(?P<disc>\d+)-\d+",           # 2-03
    r"cd\s*(?P<disc>\d+)\s*track",  # cd2-track21
]


def _clean(s: str | None) -> Optional[str]:
    if not s:
        return None
    s = re.sub(r"\s+", " ", s).strip()
    return s


def detect_disc_from_filename(filename: str) -> Optional[str]:
    for pat in DISC_PATTERNS:
        m = re.search(pat, filename, flags=re.IGNORECASE)
        if m:
            return str(m.group("disc")).zfill(2)
    return None


def detect_disc_from_folder(folder: str) -> Optional[str]:
    for pat in DISC_PATTERNS:
        m = re.search(pat, folder, flags=re.IGNORECASE)
        if m:
            return str(m.group("disc")).zfill(2)
    return None


def detect_disc(path: Path) -> Optional[str]:
    """
    Detect disc number using:
    1. Filename
    2. Parent folder
    """
    filename = path.stem
    folder = path.parent.name

    disc = detect_disc_from_filename(filename)
    if disc:
        return disc

    disc = detect_disc_from_folder(folder)
    if disc:
        return disc

    return None


def format_disc_folder(album: str, disc: Optional[str]) -> str:
    """
    Build the final album folder name:
    - If disc is None → return album
    - If disc exists → "Album (Disc 01)"
    """
    if not disc:
        return album
    return f"{album} (Disc {disc})"
