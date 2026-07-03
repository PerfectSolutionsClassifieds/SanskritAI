from __future__ import annotations

from input.normalizer import normalize_text


class NormalizationService:
    def normalize(self, text: str) -> str:
        return normalize_text(text)
