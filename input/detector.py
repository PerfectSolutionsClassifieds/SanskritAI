from __future__ import annotations


def detect_script(text: str) -> str:
    if any("\u0900" <= char <= "\u097F" for char in text):
        return "devanagari"
    return "roman"
