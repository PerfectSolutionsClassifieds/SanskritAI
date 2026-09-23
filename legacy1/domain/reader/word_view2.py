from __future__ import annotations

"""
SanskritAI
==========

Word View

Immutable reader representation of one canonical word.

WordView is the bridge between the Reader Domain and the
Resolution Kernel.

Every linguistic analysis begins from this object.

Version
-------
v2.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.reader.reader_view import (
    ReaderView,
)


@dataclass(
    frozen=True,
    slots=True,
)
class WordView(
    ReaderView,
):
    """
    Immutable Reader representation of a single word.
    """

    surface: str = ""

    transliteration: str = ""

    normalized: str = ""

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Word"

    @property
    def display_text(self) -> str:

        if self.surface:
            return self.surface

        return super().display_text

    @property
    def display_description(self) -> str:
        return (
            "Immutable reader word."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_transliteration(self) -> bool:
        return bool(self.transliteration)

    @property
    def has_normalized(self) -> bool:
        return bool(self.normalized)

    @property
    def lexical_key(self) -> str:
        """
        Canonical lexical lookup key.
        """

        if self.normalized:
            return self.normalized

        return self.surface
