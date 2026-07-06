"""
SanskritAI
==========

Module:
    services.importers.unicode_normalizer

Description
-----------
Provides Unicode normalization utilities for Sanskrit corpus
importers.

Responsibilities
----------------
    • Unicode NFC normalization
    • Remove Byte Order Mark (BOM)
    • Remove zero-width characters
    • Normalize line endings
    • Normalize tabs
    • Collapse excessive whitespace
    • Remove trailing whitespace

This module is intentionally corpus-independent and may be
shared by all future SanskritAI importers.

Version:
    v0.4.0
"""

from __future__ import annotations

import re
import unicodedata


class UnicodeNormalizer:
    """
    Unicode text normalization utilities.

    All methods are stateless and may be safely reused.
    """

    # ---------------------------------------------------------
    # Invisible Unicode Characters
    # ---------------------------------------------------------

    BYTE_ORDER_MARK = "\ufeff"

    ZERO_WIDTH_SPACE = "\u200b"

    ZERO_WIDTH_NON_JOINER = "\u200c"

    ZERO_WIDTH_JOINER = "\u200d"

    WORD_JOINER = "\u2060"

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    @classmethod
    def normalize(
        cls,
        text: str,
    ) -> str:
        """
        Complete normalization pipeline.

        Parameters
        ----------
        text
            Raw UTF-8 text.

        Returns
        -------
        str
            Clean normalized Unicode text.
        """

        text = cls.normalize_unicode(text)

        text = cls.remove_bom(text)

        text = cls.remove_zero_width(text)

        text = cls.normalize_line_endings(text)

        text = cls.normalize_tabs(text)

        text = cls.normalize_spaces(text)

        text = cls.strip_trailing_whitespace(text)

        return text

    # ---------------------------------------------------------
    # Individual Steps
    # ---------------------------------------------------------

    @staticmethod
    def normalize_unicode(
        text: str,
    ) -> str:
        """
        Normalize Unicode to NFC.
        """

        return unicodedata.normalize("NFC", text)

    @classmethod
    def remove_bom(
        cls,
        text: str,
    ) -> str:
        """
        Remove UTF-8 BOM.
        """

        return text.replace(cls.BYTE_ORDER_MARK, "")

    @classmethod
    def remove_zero_width(
        cls,
        text: str,
    ) -> str:
        """
        Remove invisible Unicode formatting characters.
        """

        characters = (

            cls.ZERO_WIDTH_SPACE,

            cls.ZERO_WIDTH_NON_JOINER,

            cls.ZERO_WIDTH_JOINER,

            cls.WORD_JOINER,

        )

        for character in characters:

            text = text.replace(character, "")

        return text

    @staticmethod
    def normalize_line_endings(
        text: str,
    ) -> str:
        """
        Convert CRLF/CR to LF.
        """

        text = text.replace("\r\n", "\n")

        text = text.replace("\r", "\n")

        return text

    @staticmethod
    def normalize_tabs(
        text: str,
    ) -> str:
        """
        Replace tabs with spaces.
        """

        return text.replace("\t", "    ")

    @staticmethod
    def normalize_spaces(
        text: str,
    ) -> str:
        """
        Collapse multiple spaces while preserving line breaks.
        """

        lines = []

        for line in text.split("\n"):

            line = re.sub(
                r"[ ]{2,}",
                " ",
                line,
            )

            lines.append(line)

        return "\n".join(lines)

    @staticmethod
    def strip_trailing_whitespace(
        text: str,
    ) -> str:
        """
        Remove trailing whitespace from every line.
        """

        return "\n".join(

            line.rstrip()

            for line in text.split("\n")

        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @classmethod
    def normalize_lines(
        cls,
        text: str,
        *,
        remove_empty: bool = False,
    ) -> list[str]:
        """
        Normalize and split into lines.

        Parameters
        ----------
        remove_empty
            If True, blank lines are discarded.

        Returns
        -------
        list[str]
        """

        text = cls.normalize(text)

        lines = text.split("\n")

        if remove_empty:

            lines = [

                line

                for line in lines

                if line.strip()

            ]

        return lines

    @staticmethod
    def is_normalized(
        text: str,
    ) -> bool:
        """
        Returns True if text is already NFC normalized.
        """

        return text == unicodedata.normalize(
            "NFC",
            text,
        )

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return "UnicodeNormalizer()"
