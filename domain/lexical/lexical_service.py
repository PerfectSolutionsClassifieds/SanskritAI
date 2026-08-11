from __future__ import annotations

"""
SanskritAI
==========

Lexical Service

Application-facing façade for the Lexical Kernel.

The LexicalService is the first contributor of the canonical
Resolution Pipeline.

Responsibilities
----------------

• Canonical lexical lookup

• Headword retrieval

• Lemma lookup

• Word-form lookup

• Candidate construction

• Contribution to ResolutionResult

Architecture
------------

ResolutionPipeline
        │
        ▼
LexicalService
        │
        ▼
LexicalRepository
        │
        ▼
CanonicalKnowledgeRepository

Version
-------
v3.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.domain.lexical.lexical_repository import (
    LexicalRepository,
)

from SanskritAI.domain.lexical.default_lexical_lookup_engine import (
    DefaultLexicalLookupEngine,
)

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)


@dataclass(
    frozen=True,
    slots=True,
)
class LexicalService(
    ResolutionContributor,
    Displayable,
):
    """
    Domain façade over lexical knowledge.

    This service is also the lexical contributor of the
    canonical Resolution Pipeline.
    """

    repository: LexicalRepository

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Lexical Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Domain façade for canonical lexical retrieval."
        )

    # ---------------------------------------------------------
    # Lookup Engine
    # ---------------------------------------------------------

    @property
    def lookup_engine(
        self,
    ) -> DefaultLexicalLookupEngine:
        """
        Canonical lookup engine.
        """
        return DefaultLexicalLookupEngine(
            repository=self.repository,
        )

    # ---------------------------------------------------------
    # Resolution Pipeline Contribution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: ResolutionContext,
    ) -> LexicalResolutionResult:
        """
        Performs lexical resolution.
        """
        return self.lookup_engine.lookup(
            context,
        )

    def contribute(
        self,
        aggregate: ResolutionResult,
        context: ResolutionContext,
    ) -> ResolutionResult:
        """
        Contributes lexical analysis to the aggregate
        ResolutionResult.
        """
        lexical_result = self.resolve(
            context,
        )

        return aggregate.with_lexical(
            lexical_result,
        )

    # ---------------------------------------------------------
    # Entry Lookup
    # ---------------------------------------------------------

    def get_entry(
        self,
        headword: str,
    ) -> CanonicalDictionaryEntry | None:
        return self.repository.get_entry(
            headword,
        )

    # ---------------------------------------------------------
    # Lemma Lookup
    # ---------------------------------------------------------

    def lookup_lemma(
        self,
        lemma: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        return self.repository.find_entries_by_lemma(
            lemma,
        )

    # ---------------------------------------------------------
    # Word-form Lookup
    # ---------------------------------------------------------

    def lookup_word_form(
        self,
        word_form: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        return self.repository.find_entries_by_word_form(
            word_form,
        )

    # ---------------------------------------------------------
    # Sense Lookup
    # ---------------------------------------------------------

    def lookup_senses(
        self,
        headword: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:
        return self.repository.find_senses(
            headword,
        )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        return self.repository.search(
            query,
        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all_entries(
        self,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        return self.repository.all_entries()

    # ---------------------------------------------------------
    # Repository Statistics
    # ---------------------------------------------------------

    @property
    def count(
        self,
    ) -> int:
        return self.repository.count

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text
