# title_normalizer.py

from __future__ import annotations
import re
from typing import Optional


def normalize_title(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None

    s = raw

    # Remove brackets
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"\[[^]]*\]", "", s)

    # Remove stray numbers left behind
    s = re.sub(r"\b\d{1,4}\b", "", s)

    # Replace separators
    s = s.replace("_", " ")
    s = re.sub(r"[-+]+", " ", s)

    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()

    # Title-case safely
    s = " ".join(w.capitalize() for w in s.split())

    return s or None
