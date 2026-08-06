from __future__ import annotations

"""
SanskritAI
==========

Canonical Knowledge Repository

Purpose
-------
The immutable root of the Canonical Sanskrit Knowledge
Repository.

The repository owns two major subsystems

    • Registries

    • KnowledgeIndex

Architecture
------------

CanonicalKnowledgeRepository

        │

        ├──────── Registries

        │           ├── LexicalRegistry

        │           ├── LemmaRegistry

        │           └── SourceRegistry

        │

        └──────── KnowledgeIndex

                    ├── HeadwordIndex

                    ├── LemmaIndex

                    ├── ContextIndex

                    ├── SourceIndex

                    └── LexicalLookupEngine

Version
-------
3.0.0
"""

from dataclasses import dataclass

from SanskritAI.acquisition.knowledge.registries.lexical_registry import (
    LexicalRegistry,
)

from SanskritAI.acquisition.knowledge.registries.lemma_registry import (
    LemmaRegistry,
)

from SanskritAI.acquisition.knowledge.registries.source_registry import (
    SourceRegistry,
)

from SanskritAI.acquisition.knowledge.indexes.knowledge_index import (
    KnowledgeIndex,
)


@dataclass(slots=True)
class CanonicalKnowledgeRepository:
    """
    Root object of the Canonical Sanskrit Knowledge Repository.
    """

    lexical_registry: LexicalRegistry

    lemma_registry: LemmaRegistry

    source_registry: SourceRegistry

    knowledge_index: KnowledgeIndex

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def registries(
        self,
    ) -> tuple:

        return (

            self.lexical_registry,

            self.lemma_registry,

            self.source_registry,

        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "lexicons":

                len(self.lexical_registry),

            "lemmas":

                len(self.lemma_registry),

            "sources":

                len(self.source_registry),

            "indexes":

                self.knowledge_index.summary(),

        }

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return (

            "CanonicalKnowledgeRepository("

            f"{self.summary()}"

            ")"

        )
