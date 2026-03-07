# core.py — Final Universal Version

from __future__ import annotations
from pathlib import Path
from typing import Optional

from .title_normalizer import normalize_title
from .disc_detector import detect_disc, format_disc_folder
from .detection import detect_album_artist_title


def build_final_path(
    src: Path,
    artist: Optional[str],
    album: Optional[str],
    disc: Optional[str],
    track_number: Optional[int],
    title: Optional[str],
    output_root: Path,
) -> Path:
    """
    Build the final destination path:
    Artist / Album (Disc 01) / 01 - Cleaned Title.ext
    """

    # Fallbacks
    artist = artist or "Unknown Artist"
    album = album or "Unknown Album"
    title = title or src.stem

    # Disc folder (Album or Album (Disc 01))
    album_folder = format_disc_folder(album, disc)

    # Track prefix (01 - Title.ext)
    if track_number:
        track_str = f"{track_number:02d}"
        filename = f"{track_str} - {title}{src.suffix}"
    else:
        filename = f"{title}{src.suffix}"

    return output_root / artist / album_folder / filename

def process_file(src: Path, output_root: Path) -> Path:
    """
    Main renaming pipeline using universal detection rules.
    """

    # ---------------------------------------
    # 1. Detect metadata (artist, album, title, track)
    # ---------------------------------------
    artist, album, title, track_number = detect_album_artist_title(src)

    # ---------------------------------------
    # 2. Normalize album + title
    # ---------------------------------------
    album_clean = normalize_title(album) or album
    title_clean = normalize_title(title) or title

    # ---------------------------------------
    # 3. Disc detection
    # ---------------------------------------
    disc = detect_disc(src)

    # ---------------------------------------
    # 4. Build final path
    # ---------------------------------------
    final_path = build_final_path(
        src=src,
        artist=artist,
        album=album_clean,
        disc=disc,
        track_number=track_number,
        title=title_clean,
        output_root=output_root,
    )

    return final_path
