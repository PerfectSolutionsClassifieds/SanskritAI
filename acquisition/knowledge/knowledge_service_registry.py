from __future__ import annotations

"""
SanskritAI
==========

Knowledge Service Registry

The canonical registry of all repositories, services,
resolution components and future high-level engines used by
SanskritAI.

Purpose
-------

The registry exists to decouple consumers from the concrete
composition root.

Instead of every component depending directly upon
CanonicalKnowledgeRepository, they depend only upon this
registry.

Architecture
------------

CanonicalKnowledgeRepository
            │
            ▼
KnowledgeServiceRegistry
            │
            ├── Repositories
            ├── Services
            ├── Resolution Components
            ├── Reader Components
            └── Future AI Components

The registry intentionally owns NO business logic.

It is simply a typed dependency registry.

Future
------

Future versions may additionally register

    • ReaderEngine

    • ResolutionPipeline

    • AIReasoner

    • PragmaticsEngine

    • CommentarialEngine

    • TranslationEngine

Version
-------
v3.1.0
"""

from dataclasses import dataclass

# ---------------------------------------------------------
# Repository Interfaces
# ---------------------------------------------------------

from SanskritAI.domain.lexical.lexical_repository import (
    LexicalRepository,
)

from SanskritAI.domain.dhatu.dhatu_repository import (
    DhatuRepository,
)

from SanskritAI.domain.morphology.morphological_repository import (
    MorphologicalRepository,
)

from SanskritAI.domain.sandhi.sandhi_repository import (
    SandhiRepository,
)

from SanskritAI.domain.samasa.samasa_repository import (
    SamasaRepository,
)

from SanskritAI.domain.semantic.semantic_repository import (
    SemanticRepository,
)

# ---------------------------------------------------------
# Services
# ---------------------------------------------------------

from SanskritAI.domain.lexical.lexical_service import (
    LexicalService,
)

from SanskritAI.domain.dhatu.dhatu_service import (
    DhatuService,
)

from SanskritAI.domain.morphology.morphological_service import (
    MorphologicalService,
)

from SanskritAI.domain.sandhi.sandhi_service import (
    SandhiService,
)

from SanskritAI.domain.samasa.samasa_service import (
    SamasaService,
)

from SanskritAI.domain.semantic.semantic_service import (
    SemanticService,
)


@dataclass(
    frozen=True,
    slots=True,
)
class KnowledgeServiceRegistry:
    """
    Canonical registry for all linguistic repositories and
    services.

    The registry intentionally contains no business logic.

    It simply provides one strongly-typed dependency object
    which may be passed throughout SanskritAI.
    """

    # -----------------------------------------------------
    # Repositories
    # -----------------------------------------------------

    lexical_repository: LexicalRepository

    dhatu_repository: DhatuRepository

    morphological_repository: MorphologicalRepository

    sandhi_repository: SandhiRepository

    samasa_repository: SamasaRepository

    semantic_repository: SemanticRepository

    # -----------------------------------------------------
    # Services
    # -----------------------------------------------------

    lexical_service: LexicalService

    dhatu_service: DhatuService

    morphological_service: MorphologicalService

    sandhi_service: SandhiService

    samasa_service: SamasaService

    semantic_service: SemanticService

    # -----------------------------------------------------
    # Repository statistics
    # -----------------------------------------------------

    @property
    def repository_count(
        self,
    ) -> int:
        return 6

    @property
    def service_count(
        self,
    ) -> int:
        return 6

    @property
    def component_count(
        self,
    ) -> int:
        return (
            self.repository_count
            + self.service_count
        )

    # -----------------------------------------------------
    # Convenience aliases
    # -----------------------------------------------------

    @property
    def lexical(
        self,
    ) -> LexicalService:
        return self.lexical_service

    @property
    def dhatu(
        self,
    ) -> DhatuService:
        return self.dhatu_service

    @property
    def morphology(
        self,
    ) -> MorphologicalService:
        return self.morphological_service

    @property
    def sandhi(
        self,
    ) -> SandhiService:
        return self.sandhi_service

    @property
    def samasa(
        self,
    ) -> SamasaService:
        return self.samasa_service

    @property
    def semantic(
        self,
    ) -> SemanticService:
        return self.semantic_service

    # -----------------------------------------------------

    def __len__(
        self,
    ) -> int:
        return self.component_count
