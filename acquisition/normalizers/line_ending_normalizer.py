
from __future__ import annotations

"""
SanskritAI
==========

Line Ending Normalizer

Normalizes platform-specific line endings into a single canonical
representation.

Responsibilities
----------------
* Convert Windows CRLF -> LF
* Convert Classic Mac CR -> LF
* Normalize Unicode line separators
* Preserve blank lines
* Preserve line ordering

This normalizer intentionally does NOT perform:

    • Unicode normalization
    • Whitespace normalization
    • OCR correction
    • Sanskrit normalization
    • Parsing

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from SanskritAI.acquisition.normalizers.base_normalizer import (
    BaseNormalizer,
)


class LineEndingNormalizer(BaseNormalizer):
    """
    Normalizes all line endings to a configurable canonical
    newline sequence.

    By default, SanskritAI stores text using Unix line endings
    ('\\n') regardless of the originating platform.
    """

    def __init__(
        self,
        newline: str = "\n",
    ) -> None:
        super().__init__()

        if newline not in ("\n", "\r\n", "\r"):
            raise ValueError(
                "newline must be one of "
                "'\\n', '\\r\\n', or '\\r'."
            )

        self._newline = newline

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def newline(self) -> str:
        """
        Canonical newline sequence.
        """
        return self._newline

    # ---------------------------------------------------------
    # BaseNormalizer API
    # ---------------------------------------------------------

    def normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalizes all supported newline conventions.
        """

        text = self.ensure_text(text)

        if not text:
            return text

        #
        # Unicode line separators
        #

        text = text.replace("\u2028", "\n")
        text = text.replace("\u2029", "\n")
        text = text.replace("\u0085", "\n")

        #
        # Windows
        #

        text = text.replace("\r\n", "\n")

        #
        # Classic Macintosh
        #

        text = text.replace("\r", "\n")

        #
        # Convert to requested output style.
        #

        if self._newline != "\n":
            text = text.replace("\n", self._newline)

        return text

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @staticmethod
    def normalize_string(
        text: str,
        newline: str = "\n",
    ) -> str:
        """
        Convenience static API.
        """
        return LineEndingNormalizer(
            newline=newline,
        ).normalize(text)

    @staticmethod
    def detect_style(
        text: str,
    ) -> str:
        """
        Detects the dominant newline convention.

        Returns
        -------
        str

            "windows"
            "unix"
            "mac"
            "mixed"
            "none"
        """

        crlf = text.count("\r\n")

        #
        # Count standalone CR only.
        #

        cr = text.count("\r") - crlf

        lf = text.count("\n") - crlf

        kinds = sum(
            x > 0
            for x in (
                crlf,
                cr,
                lf,
            )
        )

        if kinds == 0:
            return "none"

        if kinds > 1:
            return "mixed"

        if crlf:
            return "windows"

        if cr:
            return "mac"

        return "unix"

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        escaped = (
            self._newline
            .replace("\r", "\\r")
            .replace("\n", "\\n")
        )

        return (
            "LineEndingNormalizer("
            f"newline='{escaped}')"
        )
