from __future__ import annotations

"""
SanskritAI
==========

Identifiable Contract

Defines the architectural contract for objects possessing a
stable immutable identifier.

This contract specifies *what* an identifiable object must
provide, without prescribing the underlying identifier
implementation.

Typical implementations include:

- Lexeme
- Synset
- DictionaryEntry
- Corpus
- Chapter
- Verse
- KnowledgeNode

Architecture
------------

Contract
      │
      ▼
Identifiable

Version
-------
v0.6.0
"""

from abc import abstractmethod
from typing import TYPE_CHECKING

from SanskritAI.core.contracts.contract import Contract

if TYPE_CHECKING:
    from SanskritAI.core.identities.identifier import Identifier


class Identifiable(Contract):
    """
    Architectural contract for identifiable objects.
    """

    @property
    @abstractmethod
    def identifier(self) -> "Identifier":
        """
        Returns the immutable identifier associated with
        this object.
        """
        raise NotImplementedError

    @property
    def has_identifier(self) -> bool:
        """
        Indicates that this object possesses an identifier.
        """
        return True

    def same_identity_as(
        self,
        other: object,
    ) -> bool:
        """
        Returns True if two identifiable objects possess
        identical identifiers.
        """
        if not isinstance(other, Identifiable):
            return False

        return self.identifier == other.identifier
