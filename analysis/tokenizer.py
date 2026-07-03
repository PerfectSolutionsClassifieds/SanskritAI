from __future__ import annotations

import re


TOKEN_PATTERN = re.compile(r"[\u0900-\u097F]+|[a-zA-Zāīūṛṝḷṅñṭḍṇśṣṃḥ]+|[।॥]")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text)
