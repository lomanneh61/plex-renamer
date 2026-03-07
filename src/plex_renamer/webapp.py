import argparse
from pathlib import Path

from .config import load_config
from .core import rename_path


def main():
    parser = argparse.ArgumentParser(description="Plex Music Renamer")
    parser.add_argument("src", nargs="?", help="Source folder")
    parser.add_argument("dest", nargs="?", help="Destination folder")
    parser.add_argument("--review", help="Review folder")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--move", action="store_true")
    parser.add_argument("--config", help="YAML config file")
    parser.add_argument("--log", default="renamer.log")

    args = parser.parse_args()

    cli_args = {
        "src": args.src,
        "dest": args.dest,
        "review": args.review,
        "dry_run": args.dry_run,
        "move": args.move,
    }

    cfg = load_config(args.config, cli_args)

    cfg.paths.dest.mkdir(parents=True, exist_ok=True)
    cfg.paths.review.mkdir(parents=True, exist_ok=True)

    with open(args.log, "w", encoding="utf-8") as log:
        rename_path(cfg.paths.src, cfg, log)
