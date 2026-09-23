
from __future__ import annotations

"""
SanskritAI
=========

Lexical Relation Builder
========================

Fluent builder for constructing the immutable ``LexicalRelation``
domain object.

Architectural flow
------------------

LexicalRelationBuilder
        ↓
LexicalRelation
        ↓
LexicalRelationMetadata

Important
---------

``LexicalRelation`` is a regular immutable domain object and is NOT
a dataclass.

``LexicalRelationMetadata`` is a frozen dataclass.

Therefore:

* ``dataclasses.replace()`` is used only for
  ``LexicalRelationMetadata``.
* ``LexicalRelation`` instances are rebuilt explicitly.
* The canonical ``BaseBuilder`` ``_instance`` lifecycle is retained.

Version
-------

v0.4.3
"""

from dataclasses import replace

from SanskritAI.lexical.builders.base_lexical_builder import (
    BaseLexicalBuilder,
)
from SanskritAI.lexical.models.lexical_relation import (
    LexicalRelation,
)
from SanskritAI.lexical.models.lexical_relation_metadata import (
    LexicalRelationMetadata,
)
from SanskritAI.lexical.models.relation_type import (
    RelationType,
)


class LexicalRelationBuilder(
    BaseLexicalBuilder[LexicalRelation],
):
    """
    Fluent builder for ``LexicalRelation``.

    The builder maintains the current immutable relation through the
    canonical ``BaseBuilder._instance`` lifecycle.

    Metadata changes are performed using ``dataclasses.replace()``
    because ``LexicalRelationMetadata`` is a frozen dataclass.

    The enclosing ``LexicalRelation`` is rebuilt explicitly because
    it is not a dataclass.
    """

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        """
        Initialize the canonical BaseBuilder lifecycle.
        """
        super().__init__()

    # ------------------------------------------------------------------
    # Architectural construction
    # ------------------------------------------------------------------

    def _create_instance(self) -> LexicalRelation:
        """
        Create the default immutable LexicalRelation.

        This method is called by ``BaseBuilder.__init__()`` and
        ``BaseBuilder.reset()``.
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
        Replace selected immutable metadata fields.
        """
        metadata = replace(
            self._instance.metadata,
            **changes,
        )

        self._instance = LexicalRelation(
            identifier=self._instance.identifier,
            metadata=metadata,
        )

        return self

    # ------------------------------------------------------------------
    # Internal relation replacement
    # ------------------------------------------------------------------

    def _replace_relation(
        self,
        *,
        identifier: str | None = None,
        metadata: LexicalRelationMetadata | None = None,
    ) -> "LexicalRelationBuilder":
        """
        Explicitly reconstruct the immutable LexicalRelation.

        ``LexicalRelation`` is not a dataclass, so
        ``dataclasses.replace()`` cannot be used here.
        """
        self._instance = LexicalRelation(
            identifier=(
                self._instance.identifier
                if identifier is None
                else identifier
            ),
            metadata=(
                self._instance.metadata
                if metadata is None
                else metadata
            ),
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
        return self._replace_relation(
            identifier=identifier,
        )

    # ------------------------------------------------------------------
    # Relation type
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

    # ------------------------------------------------------------------
    # Relation endpoints
    # ------------------------------------------------------------------

    def between(
        self,
        source_identifier: str,
        target_identifier: str,
    ) -> "LexicalRelationBuilder":
        """
        Set the source and target lexeme identifiers.
        """
        return self._replace_metadata(
            source_identifier=source_identifier,
            target_identifier=target_identifier,
        )

    # ------------------------------------------------------------------
    # Direction
    # ------------------------------------------------------------------

    def directed(
        self,
        directed: bool,
    ) -> "LexicalRelationBuilder":
        """
        Set whether the relation is directed.
        """
        return self._replace_metadata(
            directed=directed,
        )

    # ------------------------------------------------------------------
    # Weight
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Confidence
    # ------------------------------------------------------------------

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
    # Source dictionary
    # ------------------------------------------------------------------

    def with_source_dictionary(
        self,
        source_dictionary: str,
    ) -> "LexicalRelationBuilder":
        """
        Set the source dictionary.
        """
        return self._replace_metadata(
            source_dictionary=source_dictionary,
        )

    # ------------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------------

    def with_notes(
        self,
        notes: str,
    ) -> "LexicalRelationBuilder":
        """
        Set editorial/source notes.
        """
        return self._replace_metadata(
            notes=notes,
        )

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def build(self) -> LexicalRelation:
        """
        Build the current immutable LexicalRelation.

        The canonical BaseBuilder lifecycle performs validation and
        returns a defensive copy.
        """
        return super().build()
