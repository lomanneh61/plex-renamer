🎵 plex-renamer

A universal, media‑server‑friendly audio renamer that produces clean, predictable folder structures for Plex, Jellyfin, Emby, Navidrome, and any other music server.



🚀 Example Usage

bash

plex-renamer "D:/Audio Raw" "D:/Audio Library"

This scans your input folder, detects metadata, normalizes titles, detects discs and track numbers, and outputs a clean structure like:



Code

Artist/

&nbsp;   Album (Disc 01)/

&nbsp;       01 - Cleaned Title.ext

Explore more:



folder structure rules



track numbering



disc detection



📁 Project Structure

Code

src/

&nbsp; plex\_renamer/

&nbsp;   \_\_init\_\_.py

&nbsp;   core.py

&nbsp;   detection.py

&nbsp;   title\_normalizer.py

&nbsp;   disc\_detector.py

&nbsp;   cli.py



tests/

&nbsp; test\_core.py



pyproject.toml

README.md

Explore more:



project structure



🧠 How It Works

1\. Metadata Detection

Extracts album, title, track number, and optional artist



Neutral, language‑agnostic, no cultural assumptions



Works even with messy filenames



2\. Title Normalization

Removes junk characters



Collapses whitespace



Preserves track numbers



Applies safe title‑casing



3\. Disc Detection

Detects disc numbers from folder names or filenames



Formats album folders as:



Code

Album (Disc 01)

4\. Final Path Builder

Outputs:



Code

Artist/

&nbsp;   Album (Disc 01)/

&nbsp;       01 - Title.ext

🛠 Installation

bash

pip install -e .

Explore more:



editable installs



🧪 Development

Run tests:



bash

pytest -v

Explore more:



running tests



🏷️ Versioning

This project follows semantic versioning.



To create a release:



bash

git tag v1.0.0

git push origin v1.0.0

