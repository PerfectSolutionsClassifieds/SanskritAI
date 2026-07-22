
from __future__ import annotations

"""
SanskritAI
==========

Unicode Normalizer

Provides Unicode normalization for acquired corpus resources.

Responsibilities
----------------
* Normalize Unicode (NFC/NFKC/NFD/NFKD)
* Normalize line separator characters
* Remove Unicode BOM
* Remove unwanted control characters
* Normalize non-breaking spaces
* Preserve valid Sanskrit Unicode

This normalizer intentionally does NOT perform:

* OCR correction
* Sandhi normalization
* Transliteration
* Linguistic normalization

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from enum import Enum
import unicodedata

from SanskritAI.acquisition.normalizers.base_normalizer import BaseNormalizer


class UnicodeNormalizationForm(Enum):
    """
    Supported Unicode normalization forms.
    """

    NFC = "NFC"
    NFD = "NFD"
    NFKC = "NFKC"
    NFKD = "NFKD"


class UnicodeNormalizer(BaseNormalizer):
    """
    Normalizes Unicode text into a canonical form.
    """

    #
    # Characters that should simply disappear.
    #
    _REMOVE_CHARACTERS = {
        "\ufeff",   # BOM
        "\u200b",   # Zero-width space
        "\u200c",   # Zero-width non-joiner
        "\u200d",   # Zero-width joiner
        "\u2060",   # Word joiner
    }

    #
    # Characters replaced by ordinary ASCII space.
    #
    _SPACE_REPLACEMENTS = {
        "\u00a0",   # NBSP
        "\u2000",
        "\u2001",
        "\u2002",
        "\u2003",
        "\u2004",
        "\u2005",
        "\u2006",
        "\u2007",
        "\u2008",
        "\u2009",
        "\u200a",
        "\u202f",
        "\u205f",
        "\u3000",
    }

    #
    # Unicode line separators.
    #
    _LINE_SEPARATORS = {
        "\u2028",
        "\u2029",
        "\u0085",
    }

    def __init__(
        self,
        normalization_form: UnicodeNormalizationForm = UnicodeNormalizationForm.NFC,
    ) -> None:
        super().__init__()

        self._form = normalization_form

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def normalization_form(self) -> UnicodeNormalizationForm:
        return self._form

    # ------------------------------------------------------------------
    # BaseNormalizer API
    # ------------------------------------------------------------------

    def normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize Unicode text.
        """

        text = self.ensure_text(text)

        if not text:
            return text

        #
        # Canonical Unicode normalization.
        #
        text = unicodedata.normalize(
            self._form.value,
            text,
        )

        #
        # Remove BOM and invisible characters.
        #
        text = self._remove_characters(text)

        #
        # Normalize Unicode spaces.
        #
        text = self._normalize_spaces(text)

        #
        # Normalize Unicode line separators.
        #
        text = self._normalize_line_separators(text)

        #
        # Remove unwanted control characters.
        #
        text = self._remove_control_characters(text)

        return text

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _remove_characters(
        self,
        text: str,
    ) -> str:

        for ch in self._REMOVE_CHARACTERS:
            text = text.replace(ch, "")

        return text

    def _normalize_spaces(
        self,
        text: str,
    ) -> str:

        for ch in self._SPACE_REPLACEMENTS:
            text = text.replace(ch, " ")

        return text

    def _normalize_line_separators(
        self,
        text: str,
    ) -> str:

        for ch in self._LINE_SEPARATORS:
            text = text.replace(ch, "\n")

        return text

    def _remove_control_characters(
        self,
        text: str,
    ) -> str:

        cleaned = []

        for ch in text:

            #
            # Preserve standard whitespace.
            #
            if ch in ("\n", "\r", "\t"):
                cleaned.append(ch)
                continue

            category = unicodedata.category(ch)

            #
            # Remove remaining control characters.
            #
            if category.startswith("C"):
                continue

            cleaned.append(ch)

        return "".join(cleaned)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @staticmethod
    def is_normalized(
        text: str,
        form: UnicodeNormalizationForm = UnicodeNormalizationForm.NFC,
    ) -> bool:
        """
        Returns True if the text is already normalized.
        """
        return (
            unicodedata.normalize(form.value, text)
            == text
        )

    @staticmethod
    def normalize_string(
        text: str,
        form: UnicodeNormalizationForm = UnicodeNormalizationForm.NFC,
    ) -> str:
        """
        Convenience static API.
        """
        return UnicodeNormalizer(form).normalize(text)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            "UnicodeNormalizer("
            f"form={self._form.value})"
        )
