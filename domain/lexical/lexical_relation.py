from __future__ import annotations

"""
SanskritAI
==========

Lexical Relation
----------------

Defines an immutable domain-level relationship between a lexical
source lexeme and a target lexeme.

The relation uses stable Lexeme identifiers rather than surface
forms. This keeps semantic relationships independent of script,
orthographic variation, and dictionary representation.

Architecture
------------

Lexeme
  │
  ├── DictionaryEntry
  ├── DictionarySense
  └── LexicalRelation
          │
          └── RelationType

Version
-------

v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.models.enums.relation_type import RelationType


@dataclass(frozen=True, slots=True)
class LexicalRelation(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable semantic or lexical relationship between two lexemes.

    Parameters
    ----------
    relation_id:
        Stable identifier for this relationship.

    source_lexeme_id:
        Identifier of the lexeme from which the relation originates.

    relation_type:
        Canonical RelationType describing the relationship.

    target_lexeme_id:
        Identifier of the related target lexeme.

    notes:
        Optional human-readable notes.
    """

    relation_id: str
    source_lexeme_id: str
    relation_type: RelationType
    target_lexeme_id: str
    notes: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "relation_id",
            self.relation_id.strip(),
        )
        object.__setattr__(
            self,
            "source_lexeme_id",
            self.source_lexeme_id.strip(),
        )
        object.__setattr__(
            self,
            "target_lexeme_id",
            self.target_lexeme_id.strip(),
        )
        object.__setattr__(
            self,
            "notes",
            self.notes.strip(),
        )

    @property
    def display_name(self) -> str:
        return self.relation_type.value

    @property
    def display_text(self) -> str:
        return (
            f"{self.source_lexeme_id} "
            f"{self.relation_type.value} "
            f"{self.target_lexeme_id}"
        )

    @property
    def display_description(self) -> str:
        return self.notes

    @property
    def identity(self) -> tuple[str, RelationType, str]:
        """
        Canonical identity used for indexing and deduplication.
        """
        return (
            self.source_lexeme_id,
            self.relation_type,
            self.target_lexeme_id,
        )

    @property
    def has_notes(self) -> bool:
        return bool(self.notes)

    def to_dict(self) -> dict[str, str]:
        """
        Serialize the relation into a JSON-compatible dictionary.
        """
        return {
            "relation_id": self.relation_id,
            "source_lexeme_id": self.source_lexeme_id,
            "relation_type": self.relation_type.value,
            "target_lexeme_id": self.target_lexeme_id,
            "notes": self.notes,
        }

    def __str__(self) -> str:
        return self.display_text
