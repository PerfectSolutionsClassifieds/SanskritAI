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

Version
-------
v3.2.0
"""

from dataclasses import dataclass, field

from SanskritAI.acquisition.knowledge.knowledge_service_registry import (
    KnowledgeServiceRegistry,
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

    The resulting dependencies are exposed through
    KnowledgeServiceRegistry.
    """

    # =====================================================
    # Repositories
    # =====================================================

    lexical_repository: DefaultLexicalRepository = field(
        default_factory=DefaultLexicalRepository,
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

    def __post_init__(self) -> None:

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
    def lexical(self):
        return self.registry.lexical

    @property
    def dhatu(self):
        return self.registry.dhatu

    @property
    def morphology(self):
        return self.registry.morphology

    @property
    def sandhi(self):
        return self.registry.sandhi

    @property
    def samasa(self):
        return self.registry.samasa

    @property
    def semantic(self):
        return self.registry.semantic

    # =====================================================
    # Statistics
    # =====================================================

    @property
    def repository_count(self) -> int:
        return self.registry.repository_count

    @property
    def service_count(self) -> int:
        return self.registry.service_count

    @property
    def component_count(self) -> int:
        return self.registry.component_count

    # =====================================================

    def __len__(self) -> int:
        return self.component_count
