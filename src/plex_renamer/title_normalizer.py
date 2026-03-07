from __future__ import annotations
import re
from typing import Optional

def _clean_spaces(s: str) -> str:
    # Replaces all whitespace (tabs, newlines, multiple spaces) with a single space
    return re.sub(r"\s+", " ", s).strip()

def _remove_brackets(s: str) -> str:
    # Fixed the syntax error here
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"\[[^]]*\]", "", s)
    return s

def _remove_numbers(s: str) -> str:
    # Removes standalone numbers and Roman numeral 'I's
    s = re.sub(r"\b\d+\b", "", s)
    s = re.sub(r"\b[iI]+\b", "", s)
    return s

def _remove_disc_track_hints(s: str) -> str:
    # Removes "CD 1", "Disc 2", and leading track numbers like "01 - "
    s = re.sub(r"(cd|disc|vol|volume)\s*\d+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^\d{1,2}[-_. ]+", "", s)
    return s

def _remove_separators(s: str) -> str:
    s = s.replace("_", " ")
    s = re.sub(r"[-+]+", " ", s)
    return s

def _collapse_repeated_words(s: str) -> str:
    words = s.split()
    cleaned = []
    for w in words:
        if not cleaned or cleaned[-1].lower() != w.lower():
            cleaned.append(w)
    return " ".join(cleaned)

def _title_case(s: str) -> str:
    # .title() turns "don't" into "Don'T". 
    # Using a regex or capitalize() on words is safer for titles.
    return " ".join(w.capitalize() for w in s.split())

def normalize_title(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None

    s = raw

    # 1. Remove brackets (Fixed syntax error and combined for efficiency)
    s = re.sub(r"\[[^\]]*\]|\([^)]*\)", "", s)

    # 2. Remove separators
    s = s.replace("_", " ")
    s = re.sub(r"[-+]+", " ", s)

    # 3. Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()

    # 4. Collapse repeated words
    words = s.split()
    cleaned = []
    for w in words:
        if not cleaned or cleaned[-1].lower() != w.lower():
            cleaned.append(w)
    s = " ".join(cleaned)

    # 5. Title-case safely (preserves numbers, avoids "Don'T" issues)
    s = " ".join(w.capitalize() for w in s.split())

    # Returns the string, or None if the cleaning left it empty
    return s if s else None
    return _title_case(s)