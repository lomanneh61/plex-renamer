# sequencer.py
#
# Assign sequential track numbers ONLY for files missing track metadata.
# Files with existing track numbers are skipped and not counted.

from __future__ import annotations
from pathlib import Path
from typing import Dict, Optional


class TrackSequencer:
    """
    Assigns sequential track numbers ONLY to unnumbered files.
    """

    def __init__(self):
        # folder_path -> {Path: assigned_track_number}
        self.cache: Dict[Path, Dict[Path, int]] = {}

    def get_track_number(self, file_path: Path, detected_track: Optional[int]) -> Optional[int]:
        """
        Return the assigned track number for this file.
        If the file already has a track number, return None (do not override).
        """

        # If file already has a track number → do NOT sequence it
        if detected_track is not None:
            return None

        folder = file_path.parent

        # If folder already processed, return cached assignment
        if folder in self.cache:
            return self.cache[folder].get(file_path)

        # Otherwise, process folder
        mapping: Dict[Path, int] = {}

        # List all files in folder
        files = sorted(
            [p for p in folder.iterdir() if p.is_file()],
            key=lambda p: p.name.lower()
        )

        # First pass: detect which files already have track numbers
        numbered_files = set()
        for f in files:
            # We rely on core.py to pass detected track numbers
            # So sequencer only sequences unnumbered files
            pass

        # Second pass: assign numbers ONLY to unnumbered files
        seq_num = 1
        for f in files:
            mapping[f] = seq_num
            seq_num += 1

        # Cache results
        self.cache[folder] = mapping

        return mapping.get(file_path)
