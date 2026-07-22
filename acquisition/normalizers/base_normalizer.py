
from __future__ import annotations

"""
SanskritAI
==========

Base Normalizer

Defines the abstract interface implemented by every acquisition
normalizer.

Concrete implementations include:

    • UnicodeNormalizer
    • SanskritNormalizer
    • LineEndingNormalizer
    • WhitespaceNormalizer

Future implementations may include:

    • MetadataNormalizer
    • OCRNormalizer
    • XMLNormalizer
    • TEINormalizer
    • FilenameNormalizer

A normalizer is responsible ONLY for transforming text into a
canonical representation.

It intentionally does NOT perform:

    • downloading
    • validation
    • parsing
    • linguistic analysis
    • database importing

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseNormalizer(ABC):
    """
    Abstract base class for all acquisition normalizers.

    Implementations should be stateless whenever possible,
    allowing them to be safely reused throughout the acquisition
    pipeline.
    """

    def __init__(self) -> None:
        self._name = self.__class__.__name__

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """
        Returns the human-readable normalizer name.
        """
        return self._name

    # ------------------------------------------------------------------
    # Abstract API
    # ------------------------------------------------------------------

    @abstractmethod
    def normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize text.

        Parameters
        ----------
        text:
            Input text.

        Returns
        -------
        str
            Normalized text.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Convenience Methods
    # ------------------------------------------------------------------

    def normalize_lines(
        self,
        lines: list[str],
    ) -> list[str]:
        """
        Normalize an iterable of text lines.
        """
        return [
            self.normalize(line)
            for line in lines
        ]

    def normalize_file(
        self,
        path: Path,
        *,
        encoding: str = "utf-8",
        newline: str = "\n",
    ) -> None:
        """
        Normalize a text file in-place.

        Parameters
        ----------
        path:
            File to normalize.

        encoding:
            File encoding.

        newline:
            Newline sequence to use when writing.
        """

        text = path.read_text(
            encoding=encoding,
        )

        normalized = self.normalize(text)

        path.write_text(
            normalized,
            encoding=encoding,
            newline=newline,
        )

    # ------------------------------------------------------------------
    # Validation Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def ensure_text(
        text: str,
    ) -> str:
        """
        Ensures the supplied value is a string.

        Raises
        ------
        TypeError
            If the supplied value is not a string.
        """

        if not isinstance(text, str):
            raise TypeError(
                f"Expected 'str', got "
                f"'{type(text).__name__}'."
            )

        return text

    @staticmethod
    def is_empty(
        text: str,
    ) -> bool:
        """
        Returns True if the supplied text is empty or contains
        only whitespace.
        """
        return not text.strip()

    @staticmethod
    def has_content(
        text: str,
    ) -> bool:
        """
        Returns True if the supplied text contains at least one
        non-whitespace character.
        """
        return bool(text.strip())

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            "()"
        )
