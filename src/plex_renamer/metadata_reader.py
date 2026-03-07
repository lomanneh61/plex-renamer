# metadata_reader.py
#
# Universal metadata extraction using Mutagen.
# Supports MP3, FLAC, WAV, M4A, OGG, OPUS, WMA, AIFF, and more.

from __future__ import annotations
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

from mutagen import File as MutagenFile


def safe_get(tag_dict: Dict[str, Any], keys: list[str]) -> Optional[str]:
    """
    Try multiple tag keys safely.
    Returns the first non-empty value.
    """
    for key in keys:
        if key in tag_dict:
            value = tag_dict[key]
            if isinstance(value, list):
                value = value[0]
            if value:
                return str(value).strip()
    return None


def read_metadata(path: Path) -> Tuple[
    Optional[str],  # artist
    Optional[str],  # album
    Optional[str],  # title
    Optional[int],  # track number
    Optional[int],  # disc number
]:
    """
    Read metadata from any audio file Mutagen supports.
    Returns (artist, album, title, track_number, disc_number).
    Missing fields return None.
    """

    try:
        audio = MutagenFile(path)
    except Exception:
        return None, None, None, None, None

    if not audio or not audio.tags:
        return None, None, None, None, None

    tags = audio.tags

    # Artist
    artist = safe_get(tags, ["artist", "ARTIST", "Author", "TPE1"])

    # Album
    album = safe_get(tags, ["album", "ALBUM", "TALB"])

    # Title
    title = safe_get(tags, ["title", "TITLE", "TIT2"])

    # Track number
    track_raw = safe_get(tags, ["tracknumber", "TRACKNUMBER", "TRCK"])
    track_number = None
    if track_raw:
        try:
            track_number = int(str(track_raw).split("/")[0])
        except Exception:
            pass

    # Disc number
    disc_raw = safe_get(tags, ["discnumber", "DISCNUMBER", "TPOS"])
    disc_number = None
    if disc_raw:
        try:
            disc_number = int(str(disc_raw).split("/")[0])
        except Exception:
            pass

    return artist, album, title, track_number, disc_number
