from __future__ import annotations

"""
SanskritAI
==========

Public Application Façade

This class is the single public entry point into the
SanskritAI platform.

External applications (CLI, Django, FastAPI, Desktop,
AI/RAG, Testing) should interact only with this façade.

Architecture
------------

                SanskritAI
                     │
                     ▼
      ApplicationServiceRegistry
                     │
      ┌──────────────┼──────────────┐
      │              │              │
 Knowledge       Reader        Resolution
 Registry        Engine         Pipeline

Future

    • AI / RAG

    • Commentary

    • Search

    • Translation

    • Annotation

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.application.application_service_registry import (
    ApplicationServiceRegistry,
)

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_result import (
    ReaderResult,
)

from SanskritAI.corpus.models.corpus import (
    Corpus,
)


@dataclass(slots=True)
class SanskritAI:
    """
    Public façade for the SanskritAI platform.
    """

    registry: ApplicationServiceRegistry

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    @classmethod
    def from_corpus(
        cls,
        corpus: Corpus,
    ) -> "SanskritAI":
        """
        Creates a SanskritAI application from a corpus.
        """

        registry = ApplicationServiceRegistry(
            corpus=corpus,
        )

        return cls(
            registry=registry,
        )

    # ---------------------------------------------------------
    # Reader API
    # ---------------------------------------------------------

    def analyze_position(
        self,
        position: ReaderPosition,
    ) -> ReaderResult:
        """
        Performs complete linguistic analysis for a canonical
        reader position.
        """

        return self.registry.engine.analyze(
            position,
        )

    def analyze_sloka(
        self,
        position: ReaderPosition,
    ) -> ReaderResult:
        """
        Convenience wrapper.

        Future versions may accept canonical identifiers
        directly.
        """

        return self.analyze_position(
            position,
        )

    def analyze_word(
        self,
        position: ReaderPosition,
    ) -> ReaderResult:
        """
        Performs analysis of a single word.
        """

        return self.analyze_position(
            position,
        )

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    @property
    def navigator(self):
        """
        Reader navigator.
        """

        return self.registry.reader.navigator

    # ---------------------------------------------------------
    # Knowledge
    # ---------------------------------------------------------

    @property
    def knowledge(self):
        """
        Canonical linguistic services.
        """

        return self.registry.knowledge

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    @property
    def resolution_pipeline(self):
        """
        Canonical linguistic pipeline.
        """

        return self.registry.pipeline

    # ---------------------------------------------------------
    # Future
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
    ):
        """
        Placeholder for semantic search.
        """

        raise NotImplementedError

    def ask_ai(
        self,
        prompt: str,
    ):
        """
        Placeholder for future AI/RAG integration.
        """

        raise NotImplementedError

    def generate_commentary(
        self,
        position: ReaderPosition,
    ):
        """
        Placeholder for commentary engine.
        """

        raise NotImplementedError
