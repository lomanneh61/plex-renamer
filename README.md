\# plex-renamer



A flexible, metadata-aware audio file renamer for mixed libraries (music, lectures, podcasts, anything).



\- Neutral: no cultural or religious assumptions

\- Modular: auto-detect, guessing, title normalization, disc detection

\- Safe: folder-based fallbacks and confidence scoring



\## Features



\- Extracts artist, album, title, track, disc from filenames when possible

\- Falls back to folder names and neutral guessing

\- Normalizes titles (removes junk, numbers, separators)

\- Handles multi-disc albums (`Album (Disc 01)`)

\- Produces Plex/Jellyfin-friendly structure:



```text

Artist/

&nbsp; Album (Disc 01)/

&nbsp;   01 - Cleaned Title.ext

Install

bash

pip install .

(or use a virtualenv and pip install -e . for development)



Usage

From the repo root after install:



bash

plex-renamer /path/to/source /path/to/output

source: folder containing your audio files



output: destination root where the organized structure will be created



Example

bash

plex-renamer "D:/Audio Raw" "D:/Audio Library"

Project Structure

text

src/

&nbsp; plex\_renamer/

&nbsp;   \_\_init\_\_.py

&nbsp;   core.py

&nbsp;   auto\_detect.py

&nbsp;   title\_normalizer.py

&nbsp;   disc\_detector.py

&nbsp;   guesser.py

&nbsp;   cli.py

tests/

&nbsp; test\_core.py

pyproject.toml

README.md

Development

Run tests:



bash

pytest

License

MIT



Code



---



\### 2. `pyproject.toml`



Create `pyproject.toml` in the repo root:



```toml

\[build-system]

requires = \["setuptools>=61.0"]

build-backend = "setuptools.build\_meta"



\[project]

name = "plex-renamer"

version = "0.1.0"

description = "Neutral, metadata-aware audio file renamer"

readme = "README.md"

requires-python = ">=3.9"

license = { text = "MIT" }

authors = \[

&nbsp; { name = "LANDING" }

]

dependencies = \[]



\[project.scripts]

plex-renamer = "plex\_renamer.cli:main"



\[tool.setuptools]

package-dir = {"" = "src"}



\[tool.setuptools.packages.find]

where = \["src"]

