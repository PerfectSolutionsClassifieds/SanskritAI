from __future__ import annotations

"""
SanskritAI
==========

Lexical Relation Builder
========================

Fluent builder for constructing immutable ``LexicalRelation`` objects.

Architectural contract
----------------------

The builder conforms to the ``NodeBuilder`` / ``BaseBuilder`` lifecycle.

Because ``LexicalRelation`` and ``LexicalRelationMetadata`` are
immutable, all fluent setters replace the current immutable instance.

Version
-------
v0.4.1
"""

from dataclasses import replace

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
    Fluent builder for ``LexicalRelation``.
    """

    # ------------------------------------------------------------------
    # Architectural construction
    # ------------------------------------------------------------------

    def _create_instance(self) -> LexicalRelation:
        """
        Create the default immutable relation instance.

        Used by BaseBuilder initialization and reset().
        """

        return LexicalRelation(
            identifier="",
            metadata=LexicalRelationMetadata(),
        )

    # ------------------------------------------------------------------
    # Internal metadata replacement
    # ------------------------------------------------------------------

    def _replace_metadata(
        self,
        **changes,
    ) -> "LexicalRelationBuilder":
        """
        Replace selected immutable relation metadata fields.
        """

        metadata = replace(
            self._instance.metadata,
            **changes,
        )

        self._instance = replace(
            self._instance,
            metadata=metadata,
        )

        return self

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    def with_identifier(
        self,
        identifier: str,
    ) -> "LexicalRelationBuilder":
        """
        Set the relation identifier.
        """

        self._instance = replace(
            self._instance,
            identifier=identifier,
        )

        return self

    # ------------------------------------------------------------------
    # Relation semantics
    # ------------------------------------------------------------------

    def with_relation_type(
        self,
        relation_type: RelationType,
    ) -> "LexicalRelationBuilder":
        """
        Set the relation type.
        """

        return self._replace_metadata(
            relation_type=relation_type,
        )

    def between(
        self,
        source_identifier: str,
        target_identifier: str,
    ) -> "LexicalRelationBuilder":
        """
        Set source and target lexical identifiers.
        """

        return self._replace_metadata(
            source_identifier=source_identifier,
            target_identifier=target_identifier,
        )

    def directed(
        self,
        directed: bool = True,
    ) -> "LexicalRelationBuilder":
        """
        Set whether the relation is directed.
        """

        return self._replace_metadata(
            directed=directed,
        )

    def with_weight(
        self,
        weight: float,
    ) -> "LexicalRelationBuilder":
        """
        Set relation weight.
        """

        return self._replace_metadata(
            weight=weight,
        )

    def with_confidence(
        self,
        confidence: float,
    ) -> "LexicalRelationBuilder":
        """
        Set relation confidence.
        """

        return self._replace_metadata(
            confidence=confidence,
        )

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def build(self) -> LexicalRelation:
        """
        Return the current immutable relation.
        """

        return self._instance
