"""Text normalization for search (future Android parity)."""

from __future__ import annotations

import unicodedata


def normalize_for_search(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.strip().casefold())
    without_marks = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    collapsed = " ".join(without_marks.split())
    return collapsed
