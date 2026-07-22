
from __future__ import annotations

"""
SanskritAI
==========

Sanskrit Normalizer

Performs Sanskrit-specific textual normalization after Unicode
normalization and before corpus parsing.

Responsibilities
----------------
* Normalize danda characters
* Normalize double danda characters
* Normalize avagraha
* Normalize OCR punctuation variants
* Normalize hyphen variants
* Normalize quotation marks
* Remove duplicated punctuation
* Preserve valid Sanskrit orthography

This normalizer intentionally does NOT perform:

    • sandhi splitting
    • samāsa analysis
    • stemming
    • lemmatization
    • grammatical analysis
    • transliteration

Version
-------
v0.5.0
"""

import re

from SanskritAI.acquisition.normalizers.base_normalizer import BaseNormalizer


class SanskritNormalizer(BaseNormalizer):
    """
    Sanskrit-specific normalization.
    """

    DANDA = "।"
    DOUBLE_DANDA = "॥"
    AVAGRAHA = "ऽ"

    def __init__(
        self,
        *,
        preserve_vedic_accents: bool = True,
        preserve_punctuation: bool = True,
    ) -> None:

        super().__init__()

        self._preserve_vedic_accents = preserve_vedic_accents
        self._preserve_punctuation = preserve_punctuation

    # ---------------------------------------------------------
    # BaseNormalizer API
    # ---------------------------------------------------------

    def normalize(
        self,
        text: str,
    ) -> str:

        text = self.ensure_text(text)

        if not text:
            return text

        text = self._normalize_dandas(text)
        text = self._normalize_avagraha(text)
        text = self._normalize_hyphens(text)
        text = self._normalize_quotes(text)
        text = self._remove_duplicate_punctuation(text)

        return text

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------

    def _normalize_dandas(
        self,
        text: str,
    ) -> str:

        #
        # Common OCR variants
        #

        replacements = {
            "।।": "॥",
            "॥॥": "॥",
            "||": "॥",
            "|": "।",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def _normalize_avagraha(
        self,
        text: str,
    ) -> str:

        replacements = {
            "ʼ": self.AVAGRAHA,
            "ʻ": self.AVAGRAHA,
            "ʹ": self.AVAGRAHA,
            "′": self.AVAGRAHA,
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def _normalize_hyphens(
        self,
        text: str,
    ) -> str:

        for ch in (
            "‐",
            "-",
            "–",
            "—",
            "−",
        ):
            text = text.replace(ch, "-")

        return text

    def _normalize_quotes(
        self,
        text: str,
    ) -> str:

        replacements = {
            "“": '"',
            "”": '"',
            "„": '"',
            "‟": '"',
            "‘": "'",
            "’": "'",
            "‚": "'",
            "‛": "'",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def _remove_duplicate_punctuation(
        self,
        text: str,
    ) -> str:

        #
        # Collapse excessive punctuation
        #

        text = re.sub(r"।{3,}", "॥", text)
        text = re.sub(r"॥{2,}", "॥", text)
        text = re.sub(r"-{2,}", "-", text)

        return text

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def preserve_vedic_accents(self) -> bool:
        return self._preserve_vedic_accents

    @property
    def preserve_punctuation(self) -> bool:
        return self._preserve_punctuation

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "SanskritNormalizer("
            f"preserve_vedic_accents="
            f"{self._preserve_vedic_accents}, "
            f"preserve_punctuation="
            f"{self._preserve_punctuation})"
        )
