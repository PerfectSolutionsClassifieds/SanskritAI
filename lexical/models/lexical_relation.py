from __future__ import annotations

"""
SanskritAI
==========

Lexical Relation

Represents a relationship between two lexical entities.

Examples
--------

Lexeme
    राम
        ── synonym ──► नारायण

DictionarySense
    Sense A
        ── antonym ──► Sense B

DictionaryEntry
    MW Entry
        ── related ──► Amarakośa Entry

LexicalRelation intentionally stores only identifiers.
Repositories or services resolve them into objects.

Version
-------
v0.3.0
"""

from SanskritAI.lexical.models.base_lexical_node import (
    BaseLexicalNode,
)
from SanskritAI.lexical.models.lexical_relation_metadata import (
    LexicalRelationMetadata,
)


class LexicalRelation(
    BaseLexicalNode[
        str,
        LexicalRelationMetadata,
    ]
):
    """
    Represents a lexical relationship between two entities.
    """

    def __init__(
        self,
        identifier: str,
        metadata: LexicalRelationMetadata,
    ) -> None:
        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Relation
    # ---------------------------------------------------------

    @property
    def relation_type(self):
        """
        Type of lexical relationship.
        """
        return self.metadata.relation_type

    @property
    def source_identifier(self) -> str:
        """
        Identifier of the source lexical entity.
        """
        return self.metadata.source_identifier

    @property
    def target_identifier(self) -> str:
        """
        Identifier of the target lexical entity.
        """
        return self.metadata.target_identifier

    @property
    def directed(self) -> bool:
        """
        Indicates whether the relationship is directed.
        """
        return self.metadata.directed

    @property
    def weight(self) -> float:
        """
        Relative importance of the relationship.
        """
        return self.metadata.weight

    @property
    def confidence(self) -> float:
        """
        Confidence score assigned to the relationship.
        """
        return self.metadata.confidence

    @property
    def source_dictionary(self) -> str:
        """
        Dictionary or lexical resource from which the relation
        originated.
        """
        return self.metadata.source_dictionary
