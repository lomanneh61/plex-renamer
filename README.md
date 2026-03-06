plex-renamer
A modular, extensible audio renaming toolkit designed for messy real‑world libraries. It combines metadata extraction, multi‑pattern filename parsing, folder‑based inference, alphabetical ordering, and sequential numbering to produce clean, Plex‑friendly music libraries. The package is structured as a proper Python module with optional components for a web UI and a Proxmox LXC watcher.

Features
Hybrid metadata + filename parsing

Multi‑pattern detection for chaotic filenames

Folder‑based artist/album inference

Alphabetical ordering for deterministic output

Sequential numbering for files missing track numbers

Multi‑disc detection

YAML configuration

Smart guesser for missing metadata

Dry‑run mode

Move or copy behavior

Optional Flask web UI

Optional Proxmox LXC watcher

Fully modular Python package layout

Installation
Install in editable mode during development:

bash
pip install -e .
This exposes the plex-renamer command globally.

Basic Usage
Direct CLI usage
bash
plex-renamer D:\\input D:\\output --dry-run
Using a YAML config file
bash
plex-renamer --config config.yaml
Move instead of copy
bash
plex-renamer D:\\input D:\\output --move
Configuration
The renamer can be fully controlled through a YAML file.
Example: config.example.yaml

yaml
paths:
src: "D:/music/input"
dest: "D:/music/output"
review: "D:/music/review"

behavior:
dry\_run: false
move: false
sequential\_numbering: true
alphabetical\_order: true

guesser:
enable: true
default\_album: "Unsorted Lectures"
default\_artist: "Unknown Speaker"
keywords:
- "lecture"
- "sermon"
- "khutba"
keyword\_album: "Lectures"
How It Works
Metadata extraction
If a file contains valid ID3/FLAC metadata (artist, album, title, track), the renamer uses it.

Multi‑pattern filename parsing
If metadata is missing, the renamer tries multiple filename patterns to extract track numbers and titles.

Folder‑based inference
If artist/album are missing, the parent folder name becomes both.

Alphabetical ordering
Files are processed alphabetically to ensure deterministic sequential numbering.

Sequential numbering
Files without track numbers receive 01, 02, 03, etc., based on alphabetical order.

Smart guesser
If patterns fail, the guesser attempts to infer artist/album from keywords or names in the filename.

Project Structure
Code
plex-renamer/
pyproject.toml
README.md
config.example.yaml
src/
plex\_renamer/
**init**.py
config.py
patterns.py
core.py
guesser.py
cli.py
webapp.py
watcher.py
Module overview
core.py — main renaming engine

config.py — YAML loader and validation

patterns.py — regex patterns for filename parsing

guesser.py — heuristic metadata inference

cli.py — command‑line interface

webapp.py — optional Flask web UI

watcher.py — optional Proxmox LXC folder watcher

Web UI (optional)
A lightweight Flask app provides:

drag‑and‑drop uploads

rename previews

batch renaming

log viewing

Run it:

bash
python -m plex\_renamer.webapp
Then open:

Code
http://localhost:5000
Proxmox LXC Watcher (optional)
A watcher script monitors a folder and triggers renaming automatically using inotifywait.

Example systemd service:

Code
\[Unit]
Description=Plex Renamer Watcher

\[Service]
ExecStart=/usr/bin/python3 -m plex\_renamer.watcher /opt/plex-renamer/config.yaml
Restart=always

\[Install]
WantedBy=multi-user.target
Contributing
Fork the repository

Create a feature branch

Commit your changes

Submit a pull request

Contributions are welcome for:

new filename patterns

improved smart guessing

web UI enhancements

watcher improvements

documentation

License
MIT License. See LICENSE for details.

