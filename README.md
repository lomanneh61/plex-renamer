\# plex-renamer



Hybrid Plex music renamer with:



\- metadata + multi-pattern filename parsing  

\- folder-based artist/album inference  

\- alphabetical ordering + sequential numbering  

\- YAML config, dry-run, move/copy, smart guesser stubs  

\- optional web UI and Proxmox watcher stubs  



\## Install (editable)



```bash

pip install -e .


## Usage

plex-renamer D:\input D:\output --dry-run


Or with config:

plex-renamer --config config.yaml



