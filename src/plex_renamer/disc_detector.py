# disc_detector.py
#
# Disc detection from folder names and filenames.
# Neutral, universal, and safe for any library.

from __future__ import annotations
from pathlib import Path
from typing import Optional
import re


DISC_PATTERNS = [
    r"[Dd]isc[_\s-]*(\d{1,2})",
    r"[Cc][Dd][_\s-]*(\d{1,2})",
    r"[Vv]ol[_\s-]*(\d{1,2})",
    r"[Vv]olume[_\s-]*(\d{1,2})",
]


def detect_disc_from_filename(name: str) -> Optional[int]:
    """
    Detect disc number from filename.
    """
    for pattern in DISC_PATTERNS:
        m = re.search(pattern, name)
        if m:
            try:
                return int(m.group(1))
            except Exception:
                pass
    return None


def detect_disc_from_folder(path: Path) -> Optional[int]:
    """
    Detect disc number from parent folder.
    """
    folder = path.parent.name
    for pattern in DISC_PATTERNS:
        m = re.search(pattern, folder)
        if m:
            try:
                return int(m.group(1))
            except Exception:
                pass
    return None
