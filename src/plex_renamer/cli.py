from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import logging

from .core import process_file

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Neutral audio file renamer")
    parser.add_argument("source", type=Path, help="Source folder with audio files")
    parser.add_argument("output", type=Path, help="Destination root folder")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Show what would happen, but do not move/copy")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()
    setup_logging(args.verbose)

    src_root: Path = args.source
    out_root: Path = args.output

    if not src_root.exists():
        logger.error("Source folder does not exist: %s", src_root)
        raise SystemExit(1)

    files = [p for p in src_root.rglob("*") if p.is_file()]
    if not files:
        logger.info("No files found in %s", src_root)
        return

    for src in files:
        dest = process_file(src, out_root)
        logger.info("→ %s", dest)

        if not args.dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)


if __name__ == "__main__":
    main()
