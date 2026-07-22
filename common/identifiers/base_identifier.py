from __future__ import annotations

"""
SanskritAI
==========

Base Identifier

Foundation class for all immutable identifiers used throughout
SanskritAI.

Purpose
-------
Provides a common, immutable identifier implementation for every
domain model.

Examples
--------
CorpusId
DocumentId
SectionId
ChapterId
VerseId
ParagraphId
LineId
TokenId

Characteristics
---------------
* Immutable
* Hashable
* Comparable
* JSON serializable
* UUID-based
* Type-safe
* Lightweight

Version
-------
v0.1.0
"""

from abc import ABC
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class BaseIdentifier(ABC):
    """
    Immutable identifier value object.

    Subclasses should inherit without adding mutable state.
    """

    value: UUID

    # ---------------------------------------------------------
    # Factory Methods
    # ---------------------------------------------------------

    @classmethod
    def generate(cls) -> "BaseIdentifier":
        """
        Generate a new identifier.
        """
        return cls(uuid4())

    @classmethod
    def from_string(
        cls,
        value: str,
    ) -> "BaseIdentifier":
        """
        Construct an identifier from its string representation.
        """
        return cls(UUID(value))

    @classmethod
    def from_uuid(
        cls,
        value: UUID,
    ) -> "BaseIdentifier":
        """
        Construct an identifier from an existing UUID.
        """
        return cls(value)

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_uuid(self) -> UUID:
        """
        Return the underlying UUID.
        """
        return self.value

    def to_string(self) -> str:
        """
        Return the canonical string representation.
        """
        return str(self.value)

    def to_dict(self) -> dict:
        """
        Serialize for JSON or API transport.
        """
        return {
            "id": str(self.value),
            "type": self.__class__.__name__,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"('{self.value}')"
        )
