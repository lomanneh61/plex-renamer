from pathlib import Path
import argparse

from .config import load_config
from .core import rename_path


def main():
    parser = argparse.ArgumentParser(description="Plex Renamer Tool")
    parser.add_argument("input", type=str, help="Input folder")
    parser.add_argument("--config", type=str, required=True, help="Path to config.yaml")
    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    input_path = Path(args.input)

    with open("rename.log", "w", encoding="utf-8") as log_file:
        rename_path(input_path, cfg, log_file)


if __name__ == "__main__":
    main()
