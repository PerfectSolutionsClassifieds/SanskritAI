from __future__ import annotations

"""
SanskritAI
==========

Canonical Knowledge Repository

Purpose
-------
Public façade over the Canonical Sanskrit Knowledge Repository.

This repository is the single public entry point for all
lexical, grammatical, semantic, and contextual knowledge.

Architecture
------------

                Acquisition Pipelines
                        │
                        ▼
              CanonicalLexicalRepository
                        │
                        ▼
                 CanonicalKnowledgeRepository
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
 Lexical Registry   Lemma Registry   Source Registry
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                 Lookup Engine
                        │
                        ▼
                   Reader UI

Responsibilities
----------------

• Owns all canonical registries
• Owns all lookup indexes
• Provides immutable public API
• Hides internal implementation
• Acts as the central knowledge façade

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.registries.lexical_registry import (
    LexicalRegistry,
)

from SanskritAI.acquisition.knowledge.registries.lemma_registry import (
    LemmaRegistry,
)

from SanskritAI.acquisition.knowledge.registries.source_registry import (
    SourceRegistry,
)


@dataclass(slots=True)
class CanonicalKnowledgeRepository:
    """
    Public façade over the Canonical Sanskrit Knowledge Repository.
    """

    lexical_registry: LexicalRegistry = field(
        default_factory=LexicalRegistry,
    )

    lemma_registry: LemmaRegistry = field(
        default_factory=LemmaRegistry,
    )

    source_registry: SourceRegistry = field(
        default_factory=SourceRegistry,
    )

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register_lexicon(
        self,
        lexicon,
    ) -> None:
        """
        Registers one canonical lexicon.
        """

        self.lexical_registry.register(
            lexicon,
        )

    def register_source(
        self,
        source,
    ) -> None:
        """
        Registers one canonical source.
        """

        self.source_registry.register(
            source,
        )

    def register_lemma(
        self,
        lemma,
    ) -> None:
        """
        Registers one canonical lemma.
        """

        self.lemma_registry.register(
            lemma,
        )

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def lookup_entry(
        self,
        headword: str,
    ):
        """
        Returns one canonical dictionary entry.
        """

        return self.lexical_registry.lookup_entry(
            headword,
        )

    def lookup_lemma(
        self,
        lemma: str,
    ):
        """
        Returns one canonical lemma.
        """

        return self.lemma_registry.lookup(
            lemma,
        )

    def lookup_source(
        self,
        source_name: str,
    ):
        """
        Returns one canonical source.
        """

        return self.source_registry.lookup(
            source_name,
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def lexicon_count(
        self,
    ) -> int:

        return len(
            self.lexical_registry,
        )

    @property
    def lemma_count(
        self,
    ) -> int:

        return len(
            self.lemma_registry,
        )

    @property
    def source_count(
        self,
    ) -> int:

        return len(
            self.source_registry,
        )

    def statistics(
        self,
    ) -> dict:

        return {

            "lexicons": self.lexicon_count,

            "lemmas": self.lemma_count,

            "sources": self.source_count,

        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "repository": "CanonicalKnowledgeRepository",

            "statistics": self.statistics(),

        }

    def __str__(
        self,
    ) -> str:

        return (

            "CanonicalKnowledgeRepository("

            f"{self.lexicon_count} lexicons, "

            f"{self.lemma_count} lemmas, "

            f"{self.source_count} sources)"

        )
