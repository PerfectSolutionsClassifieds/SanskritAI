from __future__ import annotations

import re


DEVANAGARI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")


def normalize_text(text: str) -> str:
    """Normalize spacing, danda punctuation, and Devanagari digits."""
    text = text.strip().translate(DEVANAGARI_DIGITS)
    text = text.replace("॥", " ॥ ").replace("।", " । ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()
