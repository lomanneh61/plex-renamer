import subprocess
from .config import load_config
from .core import rename_path

def watch(config_path: str):
    cfg = load_config(config_path, {})
    src = cfg.paths.src

    while True:
        subprocess.run(["inotifywait", "-e", "close_write,create,move", "-r", str(src)])
        with open("watcher.log", "a", encoding="utf-8") as log:
            rename_path(src, cfg, log)