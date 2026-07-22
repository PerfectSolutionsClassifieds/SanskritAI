from __future__ import annotations

"""
SanskritAI
==========

Lexical Relation Builder

Version
-------
v0.3.0
"""

from SanskritAI.lexical.builders.base_lexical_builder import (
    BaseLexicalBuilder,
)
from SanskritAI.lexical.enums.relation_type import (
    RelationType,
)
from SanskritAI.lexical.models.lexical_relation import (
    LexicalRelation,
)
from SanskritAI.lexical.models.lexical_relation_metadata import (
    LexicalRelationMetadata,
)


class LexicalRelationBuilder(
    BaseLexicalBuilder[LexicalRelation],
):
    """
    Fluent builder for LexicalRelation.
    """

    def __init__(self) -> None:
        super().__init__()

        self._identifier = ""
        self._metadata = LexicalRelationMetadata()

    # ---------------------------------------------------------

    def with_identifier(
        self,
        identifier: str,
    ) -> "LexicalRelationBuilder":

        self._identifier = identifier
        return self

    # ---------------------------------------------------------

    def with_relation_type(
        self,
        relation_type: RelationType,
    ) -> "LexicalRelationBuilder":

        self._metadata.relation_type = relation_type
        return self

    # ---------------------------------------------------------

    def between(
        self,
        source_identifier: str,
        target_identifier: str,
    ) -> "LexicalRelationBuilder":

        self._metadata.source_identifier = source_identifier
        self._metadata.target_identifier = target_identifier
        return self

    # ---------------------------------------------------------

    def directed(
        self,
        directed: bool = True,
    ) -> "LexicalRelationBuilder":

        self._metadata.directed = directed
        return self

    # ---------------------------------------------------------

    def with_weight(
        self,
        weight: float,
    ) -> "LexicalRelationBuilder":

        self._metadata.weight = weight
        return self

    # ---------------------------------------------------------

    def with_confidence(
        self,
        confidence: float,
    ) -> "LexicalRelationBuilder":

        self._metadata.confidence = confidence
        return self

    # ---------------------------------------------------------

    def build(self) -> LexicalRelation:

        return LexicalRelation(
            identifier=self._identifier,
            metadata=self._metadata,
        )
