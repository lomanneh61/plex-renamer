# cli.py
#
# Command-line interface for plex-renamer.
# Integrates:
# - hybrid metadata detection
# - auto-assigned track numbers
# - dry-run mode
# - verbose logging

from __future__ import annotations
import argparse
from pathlib import Path

from .core import process_file


def main():
    parser = argparse.ArgumentParser(
        description="Rename audio files using metadata, filename detection, and auto-assigned track numbers."
    )

    parser.add_argument("input", help="Input folder containing audio files.")
    parser.add_argument("output", help="Output folder for renamed files.")

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without renaming or moving files."
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging."
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"ERROR: Input path does not exist: {input_path}")
        return

    # Process all files recursively
    for src in input_path.rglob("*"):
        if not src.is_file():
            continue

        dest = process_file(src, output_path, verbose=args.verbose)

        if args.dry_run:
            print(f"INFO: → {dest}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            src.rename(dest)
            print(f"RENAMED: {src} → {dest}")
