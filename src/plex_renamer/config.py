from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
import yaml


@dataclass
class BehaviorConfig:
    alphabetical_order: bool = True
    sequential_numbering: bool = True
    dry_run: bool = False
    move: bool = False


@dataclass
class PathsConfig:
    dest: Path = Path(".")


@dataclass
class GuesserConfig:
    enable: bool = True
    keywords: list[str] = field(default_factory=list)
    default_album: str | None = None
    default_artist: str | None = None


@dataclass
class Config:
    paths: PathsConfig = field(default_factory=PathsConfig)
    behavior: BehaviorConfig = field(default_factory=BehaviorConfig)
    guesser: GuesserConfig = field(default_factory=GuesserConfig)
    patterns: List[str] = field(default_factory=list)


def load_config(path: Path) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return Config(
        paths=PathsConfig(dest=Path(data["paths"]["dest"])),
        behavior=BehaviorConfig(**data["behavior"]),
        guesser=GuesserConfig(**data["guesser"]),
        patterns=data.get("patterns", []),
    )
