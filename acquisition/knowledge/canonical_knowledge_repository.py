
from __future__ import annotations

"""
SanskritAI
==========

Canonical Knowledge Repository

Composition root for the SanskritAI knowledge layer.

This object constructs the canonical repositories and services
and exposes them through KnowledgeServiceRegistry.

Important architectural rule
-----------------------------

The composition root may depend on domain implementations.

Domain services must NOT depend on this composition root.

Canonical lexical state is owned here.

DefaultLexicalRepository is a domain adapter and delegates
lexical operations back to this composition root.

Version
-------
v3.3.0
"""

from dataclasses import dataclass, field
from typing import Iterable

from SanskritAI.acquisition.knowledge.knowledge_service_registry import (
    KnowledgeServiceRegistry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)

# =========================================================
# Default Repositories
# =========================================================

from SanskritAI.domain.lexical.default_lexical_repository import (
    DefaultLexicalRepository,
)

from SanskritAI.domain.dhatu.default_dhatu_repository import (
    DefaultDhatuRepository,
)

from SanskritAI.domain.morphology.default_morphological_repository import (
    DefaultMorphologicalRepository,
)

from SanskritAI.domain.sandhi.default_sandhi_repository import (
    DefaultSandhiRepository,
)

from SanskritAI.domain.samasa.default_samasa_repository import (
    DefaultSamasaRepository,
)

from SanskritAI.domain.semantic.default_semantic_repository import (
    DefaultSemanticRepository,
)

# =========================================================
# Default Services
# =========================================================

from SanskritAI.domain.lexical.default_lexical_service import (
    DefaultLexicalService,
)

from SanskritAI.domain.dhatu.default_dhatu_service import (
    DefaultDhatuService,
)

from SanskritAI.domain.morphology.default_morphological_service import (
    DefaultMorphologicalService,
)

from SanskritAI.domain.sandhi.default_sandhi_service import (
    DefaultSandhiService,
)

from SanskritAI.domain.samasa.default_samasa_service import (
    DefaultSamasaService,
)

from SanskritAI.domain.semantic.default_semantic_service import (
    DefaultSemanticService,
)


@dataclass(
    slots=True,
)
class CanonicalKnowledgeRepository:
    """
    SanskritAI composition root.

    Owns construction of the canonical repositories and
    application services.

    Canonical lexical state is owned by this object.

    DefaultLexicalRepository is a thin domain adapter that
    delegates lexical operations to this composition root.
    """

    # =====================================================
    # Repositories
    # =====================================================

    lexical_repository: DefaultLexicalRepository | None = field(
        default=None,
    )

    dhatu_repository: DefaultDhatuRepository = field(
        default_factory=DefaultDhatuRepository,
    )

    morphological_repository: DefaultMorphologicalRepository = field(
        default_factory=DefaultMorphologicalRepository,
    )

    sandhi_repository: DefaultSandhiRepository = field(
        default_factory=DefaultSandhiRepository,
    )

    samasa_repository: DefaultSamasaRepository = field(
        default_factory=DefaultSamasaRepository,
    )

    semantic_repository: DefaultSemanticRepository = field(
        default_factory=DefaultSemanticRepository,
    )

    # =====================================================
    # Canonical Lexical State
    # =====================================================

    _lexicons: dict[
        str,
        CanonicalLexicon,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # =====================================================
    # Services
    # =====================================================

    lexical_service: DefaultLexicalService = field(
        init=False,
    )

    dhatu_service: DefaultDhatuService = field(
        init=False,
    )

    morphological_service: DefaultMorphologicalService = field(
        init=False,
    )

    sandhi_service: DefaultSandhiService = field(
        init=False,
    )

    samasa_service: DefaultSamasaService = field(
        init=False,
    )

    semantic_service: DefaultSemanticService = field(
        init=False,
    )

    # =====================================================
    # Registry
    # =====================================================

    registry: KnowledgeServiceRegistry = field(
        init=False,
    )

    # =====================================================
    # Construction
    # =====================================================

    def __post_init__(
        self,
    ) -> None:

        # -------------------------------------------------
        # Lexical Repository Adapter
        # -------------------------------------------------

        if self.lexical_repository is None:

            self.lexical_repository = (
                DefaultLexicalRepository(
                    repository=self,
                )
            )

        # -------------------------------------------------
        # Services
        # -------------------------------------------------

        self.lexical_service = DefaultLexicalService(
            repository=self.lexical_repository,
        )

        # IMPORTANT:
        #
        # DhatuService is resolver-oriented.
        # The Dhatu repository remains an independent
        # registered knowledge component.
        #
        self.dhatu_service = DefaultDhatuService()

        self.morphological_service = (
            DefaultMorphologicalService(
                repository=self.morphological_repository,
            )
        )

        self.sandhi_service = DefaultSandhiService(
            repository=self.sandhi_repository,
        )

        self.samasa_service = DefaultSamasaService(
            repository=self.samasa_repository,
        )

        self.semantic_service = DefaultSemanticService(
            repository=self.semantic_repository,
        )

        # -------------------------------------------------
        # Registry
        # -------------------------------------------------

        self.registry = KnowledgeServiceRegistry(

            # repositories

            lexical_repository=self.lexical_repository,

            dhatu_repository=self.dhatu_repository,

            morphological_repository=(
                self.morphological_repository
            ),

            sandhi_repository=self.sandhi_repository,

            samasa_repository=self.samasa_repository,

            semantic_repository=self.semantic_repository,

            # services

            lexical_service=self.lexical_service,

            dhatu_service=self.dhatu_service,

            morphological_service=(
                self.morphological_service
            ),

            sandhi_service=self.sandhi_service,

            samasa_service=self.samasa_service,

            semantic_service=self.semantic_service,
        )

    # =====================================================
    # Canonical Lexicon State
    # =====================================================

    def add_lexicon(
        self,
        lexicon: CanonicalLexicon,
    ) -> None:
        """
        Add or replace one canonical lexicon.

        The composition root remains the authoritative owner
        of canonical lexical state.
        """

        self._lexicons[
            lexicon.identifier
        ] = lexicon

    def register_lexicon(
        self,
        lexicon: CanonicalLexicon,
    ) -> None:
        """
        Explicit registration alias.
        """

        self.add_lexicon(
            lexicon,
        )

    def clear_lexicons(
        self,
    ) -> None:
        """
        Remove all canonical lexicons.
        """

        self._lexicons.clear()

    def all_lexicons(
        self,
    ) -> tuple[
        CanonicalLexicon,
        ...,
    ]:
        """
        Return all registered canonical lexicons.
        """

        return tuple(
            self._lexicons.values(),
        )

    # =====================================================
    # Lexical Entry Operations
    # =====================================================

    def get_entry(
        self,
        headword: str,
    ) -> CanonicalDictionaryEntry | None:
        """
        Find the first canonical dictionary entry matching
        the supplied headword.
        """

        for lexicon in self.all_lexicons():

            entry = lexicon.get(
                headword,
            )

            if entry is not None:
                return entry

        return None

    def all_entries(
        self,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Return all canonical dictionary entries across
        all registered lexicons.
        """

        entries: list[
            CanonicalDictionaryEntry,
        ] = []

        for lexicon in self.all_lexicons():

            entries.extend(
                lexicon.all_entries(),
            )

        return tuple(
            entries,
        )

    @property
    def lexical_entry_count(
        self,
    ) -> int:
        """
        Number of canonical dictionary entries.
        """

        return len(
            self.all_entries(),
        )

    # =====================================================
    # Lemma Lookup
    # =====================================================

    def find_entries_by_lemma(
        self,
        lemma: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Find canonical entries whose lemma text matches
        the supplied lemma.
        """

        matches: list[
            CanonicalDictionaryEntry,
        ] = []

        for entry in self.all_entries():

            entry_lemma = getattr(
                entry,
                "lemma",
                None,
            )

            lemma_text = getattr(
                entry_lemma,
                "lemma",
                entry_lemma,
            )

            if lemma_text == lemma:
                matches.append(
                    entry,
                )

        return tuple(
            matches,
        )

    # =====================================================
    # Word Form Lookup
    # =====================================================

    def find_entries_by_word_form(
        self,
        word_form: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Find entries matching a supplied word form.

        Canonical dictionary entries may expose word-form
        information through their metadata or direct fields.
        """

        matches: list[
            CanonicalDictionaryEntry,
        ] = []

        for entry in self.all_entries():

            if getattr(
                entry,
                "headword",
                None,
            ) == word_form:
                matches.append(
                    entry,
                )
                continue

            forms = getattr(
                entry,
                "word_forms",
                (),
            )

            if word_form in forms:
                matches.append(
                    entry,
                )

        return tuple(
            matches,
        )

    # =====================================================
    # Sense Lookup
    # =====================================================

    def find_senses(
        self,
        headword: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:
        """
        Return all senses belonging to a headword.
        """

        entry = self.get_entry(
            headword,
        )

        if entry is None:
            return ()

        return tuple(
            entry.senses,
        )

    # =====================================================
    # Search
    # =====================================================

    def search(
        self,
        query: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:
        """
        Simple canonical lexical search.

        Exact headword matches are naturally included.
        Search is intentionally deterministic and small;
        specialized indexes remain responsible for indexed
        lookup.
        """

        if not query:
            return ()

        results: list[
            CanonicalDictionaryEntry,
        ] = []

        for entry in self.all_entries():

            headword = getattr(
                entry,
                "headword",
                "",
            )

            transliteration = getattr(
                entry,
                "transliteration",
                None,
            )

            lemma = getattr(
                getattr(
                    entry,
                    "lemma",
                    None,
                ),
                "lemma",
                None,
            )

            if (
                query in headword
                or (
                    transliteration is not None
                    and query.lower()
                    in transliteration.lower()
                )
                or (
                    lemma is not None
                    and query in lemma
                )
            ):
                results.append(
                    entry,
                )

        return tuple(
            results,
        )

    # =====================================================
    # Registry Shortcut
    # =====================================================

    @property
    def services(
        self,
    ) -> KnowledgeServiceRegistry:
        """
        Preferred access point.

        Example:

            repository.services.lexical
            repository.services.dhatu
            repository.services.morphology
        """

        return self.registry

    # =====================================================
    # Legacy Convenience Properties
    # =====================================================

    @property
    def lexical(
        self,
    ):
        return self.registry.lexical

    @property
    def dhatu(
        self,
    ):
        return self.registry.dhatu

    @property
    def morphology(
        self,
    ):
        return self.registry.morphology

    @property
    def sandhi(
        self,
    ):
        return self.registry.sandhi

    @property
    def samasa(
        self,
    ):
        return self.registry.samasa

    @property
    def semantic(
        self,
    ):
        return self.registry.semantic

    # =====================================================
    # Statistics
    # =====================================================

    @property
    def repository_count(
        self,
    ) -> int:
        return self.registry.repository_count

    @property
    def service_count(
        self,
    ) -> int:
        return self.registry.service_count

    @property
    def component_count(
        self,
    ) -> int:
        return self.registry.component_count

    # =====================================================

    def __len__(
        self,
    ) -> int:
        return self.component_count
