# guesser.py (Fully Neutral Version)

from __future__ import annotations
import re
from pathlib import Path
from typing import Optional


def guess_artist(filename: str, folder: str) -> tuple[Optional[str], float]:
    """
    Neutral artist guesser:
    - No speaker titles
    - No cultural assumptions
    - Only generic name detection + folder fallback
    """

    # 1. Generic 2–4 word capitalized name (universal)
    m = re.search(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}", filename)
    if m:
        return m.group(0).strip(), 0.70

    # 2. Folder fallback
    if folder and not folder.isnumeric():
        return folder, 0.50

    return None, 0.0


def guess_album(filename: str, folder: str) -> tuple[Optional[str], float]:
    """
    Neutral album guesser:
    - No topic hints
    - No cultural hints
    - Only folder fallback
    """

    if folder and not folder.isnumeric():
        return folder, 0.50

    return None, 0.0


def guess_title(filename: str) -> tuple[Optional[str], float]:
    """
    Neutral title guesser:
    - Removes track numbers
    - Removes disc hints
    - Cleans separators
    """

    # Remove leading track numbers
    s = re.sub(r"^\d{1,2}[-_. ]+", "", filename)

    # Remove disc hints
    s = re.sub(r"(cd|disc|vol)\s*\d+", "", s, flags=re.IGNORECASE)

    # Clean separators
    s = re.sub(r"[-+_]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()

    if not s:
        return None, 0.0

    return s, 0.60


def guess_metadata(path: Path) -> dict:
    """
    Returns:
    {
        "artist": str | None,
        "album": str | None,
        "title": str | None,
        "confidence": float
    }
    """

    filename = path.stem
    folder = path.parent.name

    artist, a_conf = guess_artist(filename, folder)
    album, b_conf = guess_album(filename, folder)
    title, t_conf = guess_title(filename)

    # Weighted confidence
    confidence = (a_conf + b_conf + t_conf) / 3

    return {
        "artist": artist,
        "album": album,
        "title": title,
        "confidence": confidence,
    }
