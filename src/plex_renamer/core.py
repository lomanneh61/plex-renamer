from __future__ import annotations
import os
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from mutagen import File as MutagenFile

from .patterns import compile_patterns
from .guesser import smart_guess
from .config import Config

def _clean(s: str | None) -> str:
    if not s:
        return ""
    import re
    s = s.replace("+", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return "".join(c for c in s if c not in '/\\:*?"<>|')

def _title_case(s: str) -> str:
    return s.title()

def _extract_tags(path: Path) -> dict | None:
    audio = MutagenFile(path, easy=True)
    if not audio:
        return None

    artist = audio.get("artist", [None])[0]
    album = audio.get("album", [None])[0]
    title = audio.get("title", [None])[0]
    track = audio.get("tracknumber", [None])[0]
    disc = audio.get("discnumber", ["1"])[0]

    if not all([artist, album, title, track]):
        return None

    track = str(track).split("/")[0].zfill(2)
    disc = str(disc).split("/")[0].zfill(2)

    return {
        "artist": _clean(artist),
        "album": _clean(album),
        "title": _clean(title),
        "track": track,
        "disc": disc,
    }

def _parse_filename(filename: str, patterns: Iterable) -> dict | None:
    for pattern in patterns:
        m = pattern.match(filename)
        if m:
            data = m.groupdict()
            data.setdefault("track", "00")
            data.setdefault("title", "Unknown Title")
            data.setdefault("disc", "01")
            data["track"] = str(data["track"]).zfill(2)
            return {k: _clean(v) for k, v in data.items()}
    return None

_track_counters: dict[str, int] = defaultdict(int)

def _next_track(folder_key: str) -> str:
    _track_counters[folder_key] += 1
    return f"{_track_counters[folder_key]:02d}"

def rename_path(root: Path, cfg: Config, log_file) -> None:
    patterns = compile_patterns(cfg.patterns)
    for dirpath, _, files in os.walk(root):
        dirpath = Path(dirpath)
        if cfg.behavior.alphabetical_order:
            files = sorted(files, key=str.lower)
        for name in files:
            _process_file(dirpath / name, cfg, patterns, log_file)

def _process_file(path: Path, cfg: Config, patterns, log_file) -> None:
    filename = path.name
    ext = path.suffix
    parent = _clean(path.parent.name)

    meta = _extract_tags(path)
    if not meta:
        parsed = _parse_filename(filename, patterns)
        if parsed:
            meta = parsed
            if meta["track"] in ("00", "0", "") and cfg.behavior.sequential_numbering:
                meta["track"] = _next_track(parent)
            meta.setdefault("artist", parent)
            meta.setdefault("album", parent)
        else:
            guess = smart_guess(filename, parent, cfg.guesser)
            meta = {
                "artist": _clean(guess.artist or parent),
                "album": _clean(guess.album or parent),
                "title": _clean(filename),
                "track": _next_track(parent) if cfg.behavior.sequential_numbering else "00",
                "disc": "01",
            }

    meta["title"] = _title_case(meta["title"])

    album_folder = meta["album"]
    if meta.get("disc") and meta["disc"] != "01":
        album_folder = f"{meta['album']} (Disc {meta['disc']})"

    dest_dir = cfg.paths.dest / meta["artist"] / album_folder
    dest_dir.mkdir(parents=True, exist_ok=True)

    new_name = f"{meta['track']} - {meta['title']}{ext}"
    dest_path = dest_dir / new_name

    log_file.write(f"{path} -> {dest_path}\n")

    if cfg.behavior.dry_run:
        return

    if cfg.behavior.move:
        shutil.move(path, dest_path)
    else:
        shutil.copy2(path, dest_path)
