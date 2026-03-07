from __future__ import annotations
import re
from pathlib import Path
from typing import Optional, Tuple


def detect_album_artist_title(path: Path) -> Tuple[Optional[str], str, str, Optional[int]]:
    """
    Detect artist, album, title, and track number using neutral rules.
    Returns: (artist, album, title, track_number)
    """

    filename = path.stem
    folder = path.parent.name

    # 1. Track number
    m = re.search(r"\b(\d{1,3})\b", filename)
    track_number = int(m.group(1)) if m else None

    # 2. Base title cleanup
    base = re.sub(r"\b\d{1,3}\b", "", filename)
    base = re.sub(r"[_\-]+", " ", base).strip()

    # 3. Artist detection (only if filename starts with a name-like pattern)
    artist = None
    m_artist = re.match(r"^([A-Za-z]{2,}(?: [A-Za-z]{2,}){0,3})\s*[-–]\s*", filename)
    if m_artist:
        artist = m_artist.group(1)
        base = filename[m_artist.end():].strip()

    # 4. Album logic
    album = base if base else folder

    # 5. Title logic
    if track_number:
        title = f"{base} {track_number}".strip()
    else:
        title = base

    # 6. Fallbacks
    album = album.strip() or "Unknown Album"
    title = title.strip() or filename

    return artist, album, title, track_number
