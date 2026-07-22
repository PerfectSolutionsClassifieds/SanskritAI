from __future__ import annotations

"""
SanskritAI
==========

Identifiable Interface

Defines the contract for objects possessing a stable,
unique identifier.

Every major domain object within SanskritAI should
implement this interface.

Examples
--------

Corpus
Document
Section
Verse
Paragraph
Line
Token

Lexeme
DictionaryEntry
Dhatu

Version
-------
v0.3.0
"""

from abc import ABC, abstractmethod
from typing import Generic

from SanskritAI.core.typing import TIdentifier


class Identifiable(
    Generic[TIdentifier],
    ABC,
):
    """
    Contract for uniquely identifiable objects.
    """

    # ---------------------------------------------------------

    @property
    @abstractmethod
    def id(
        self,
    ) -> TIdentifier:
        """
        Returns the unique identifier.
        """
        ...

    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> TIdentifier:
        """
        Alias for ``id``.

        Improves readability in contexts where ``id`` may
        be confused with Python's built-in function.
        """

        return self.id

    # ---------------------------------------------------------

    def has_identifier(
        self,
    ) -> bool:
        """
        Returns True if a valid identifier exists.
        """

        return self.id is not None
