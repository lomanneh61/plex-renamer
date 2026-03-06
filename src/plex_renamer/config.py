import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

@dataclass
class PathsConfig:
    src: Path
    dest: Path
    review: Path = Path("review")

@dataclass
class BehaviorConfig:
    dry_run: bool = False
    move: bool = False
    sequential_numbering: bool = True
    alphabetical_order: bool = True

@dataclass
class Config:
    paths: PathsConfig
    behavior: BehaviorConfig = BehaviorConfig()
    patterns: List[str] = field(default_factory=list)
    guesser: dict = field(default_factory=dict)

def load_config(path: str | None, cli_args: dict) -> Config:
    data: dict = {}
    if path:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

    def get(key, default=None):
        return cli_args.get(key, data.get(key, default))

    paths = data.get("paths", {})
    paths_cfg = PathsConfig(
        src=Path(get("src", paths.get("src"))),
        dest=Path(get("dest", paths.get("dest"))),
        review=Path(get("review", paths.get("review", "review"))),
    )

    behavior = data.get("behavior", {})
    beh_cfg = BehaviorConfig(
        dry_run=get("dry_run", behavior.get("dry_run", False)),
        move=get("move", behavior.get("move", False)),
        sequential_numbering=behavior.get("sequential_numbering", True),
        alphabetical_order=behavior.get("alphabetical_order", True),
    )

    patterns = data.get("patterns", [])
    guesser = data.get("guesser", {})

    return Config(paths=paths_cfg, behavior=beh_cfg, patterns=patterns, guesser=guesser)
