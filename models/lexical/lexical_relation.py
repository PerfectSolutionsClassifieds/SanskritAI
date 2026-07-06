"""
SanskritAI
==========

Module:
    models.lexical.lexical_relation

Description:
    Represents a semantic relationship between two Lexeme objects.

Version:
    v0.3.0 Final
"""

from __future__ import annotations

from dataclasses import dataclass

from models.enums.relation_type import RelationType


@dataclass(slots=True)
class LexicalRelation:
    """
    Semantic relationship between two Lexeme objects.

    Relationships are stored using Lexeme IDs rather than
    textual forms, ensuring stability across scripts,
    dictionaries, and orthographic variants.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    relation_id: str

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------

    relation_type: RelationType

    target_lexeme_id: str

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    notes: str = ""

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Validate and normalize the object.
        """

        self.relation_id = self.relation_id.strip()
        self.target_lexeme_id = self.target_lexeme_id.strip()
        self.notes = self.notes.strip()

        if not self.relation_id:
            raise ValueError("relation_id cannot be empty.")

        if not self.target_lexeme_id:
            raise ValueError("target_lexeme_id cannot be empty.")

    # ---------------------------------------------------------
    # Computed Properties
    # ---------------------------------------------------------

    @property
    def identity(self) -> tuple[RelationType, str]:
        """
        Canonical identity for indexing and deduplication.
        """

        return (
            self.relation_type,
            self.target_lexeme_id,
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialize to a JSON-compatible dictionary.
        """

        return {
            "relation_id": self.relation_id,
            "relation_type": self.relation_type.value,
            "target_lexeme_id": self.target_lexeme_id,
            "notes": self.notes,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"{self.relation_type.value}"
            f" → {self.target_lexeme_id}"
        )

    def __repr__(self) -> str:
        return (
            "LexicalRelation("
            f"id='{self.relation_id}', "
            f"type='{self.relation_type.name}', "
            f"target='{self.target_lexeme_id}')"
        )
