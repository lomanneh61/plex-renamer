# core.py

from __future__ import annotations
from pathlib import Path
from typing import Optional

from .detection import detect_all
from .sequencer import TrackSequencer


sequencer = TrackSequencer()


def format_disc_folder(album: str, disc: Optional[int]) -> str:
    if disc:
        return f"{album} (Disc {disc:02d})"
    return album


def build_final_path(
    src: Path,
    artist: Optional[str],
    album: Optional[str],
    disc: Optional[int],
    track: Optional[int],
    title: Optional[str],
    output_root: Path,
) -> Path:

    artist = artist or "Unknown Artist"
    album = album or "Unknown Album"
    title = title or src.stem

    album_folder = format_disc_folder(album, disc)

    if track:
        filename = f"{track:02d} - {title}{src.suffix}"
    else:
        filename = f"{title}{src.suffix}"

    return output_root / artist / album_folder / filename


def process_file(src: Path, output_root: Path, verbose: bool = False) -> Path:
    artist, album, title, track, disc = detect_all(src)

    # Ask sequencer ONLY if track is missing
    assigned = sequencer.get_track_number(src, track)

    if assigned is not None:
        track = assigned
        if verbose:
            print(f"[SEQ] Assigned track {track:02d} to {src.name}")

    return build_final_path(
        src=src,
        artist=artist,
        album=album,
        disc=disc,
        track=track,
        title=title,
        output_root=output_root,
    )
