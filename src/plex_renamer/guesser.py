import re
from dataclasses import dataclass


@dataclass
class GuessResult:
    artist: str | None = None
    album: str | None = None


def smart_guess(filename: str, folder_name: str, cfg: dict) -> GuessResult:
    keywords = cfg.keywords
    default_album = cfg.default_album or folder_name
    default_artist = cfg.default_artist or folder_name

    name = filename.lower()
    album = default_album
    artist = default_artist

    for kw in keywords:
        if kw.lower() in name:
            album = cfg.get("keyword_album", default_album)
            break

    m = re.search(r"(imam\s+\w+)", filename, re.IGNORECASE)
    if m:
        artist = m.group(1).title()

    return GuessResult(artist=artist, album=album)
