from __future__ import annotations

"""
SanskritAI
==========

Canonical Knowledge Repository

The Composition Root for the complete SanskritAI
Knowledge Layer.

This object owns every canonical linguistic repository and
their corresponding application services.

Knowledge Domains
-----------------

• Lexical

• Dhatu

• Morphology

• Sandhi

• Samasa

• Semantic

This class intentionally acts as the single entry point into
canonical linguistic knowledge.

No component outside this layer should directly instantiate
individual repositories.

Version
-------
v3.0.0
"""

from dataclasses import dataclass, field

# ---------------------------------------------------------
# Repositories
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# Services
# ---------------------------------------------------------

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


@dataclass(slots=True)
class CanonicalKnowledgeRepository:
    """
    Composition Root for all canonical Sanskrit knowledge.
    """

    # -----------------------------------------------------
    # Repositories
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Services
    # -----------------------------------------------------

    lexical_service: DefaultLexicalService = field(init=False)

    dhatu_service: DefaultDhatuService = field(init=False)

    morphological_service: DefaultMorphologicalService = field(init=False)

    sandhi_service: DefaultSandhiService = field(init=False)

    samasa_service: DefaultSamasaService = field(init=False)

    semantic_service: DefaultSemanticService = field(init=False)

    # -----------------------------------------------------
    # Initialization
    # -----------------------------------------------------

    def __post_init__(self) -> None:

        self.lexical_service = DefaultLexicalService(
            repository=self.lexical_repository,
        )

        self.dhatu_service = DefaultDhatuService(
            repository=self.dhatu_repository,
        )

        self.morphological_service = DefaultMorphologicalService(
            repository=self.morphological_repository,
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

    # -----------------------------------------------------
    # Convenience Accessors
    # -----------------------------------------------------

    @property
    def lexical(self) -> DefaultLexicalService:
        return self.lexical_service

    @property
    def dhatu(self) -> DefaultDhatuService:
        return self.dhatu_service

    @property
    def morphology(self) -> DefaultMorphologicalService:
        return self.morphological_service

    @property
    def sandhi(self) -> DefaultSandhiService:
        return self.sandhi_service

    @property
    def samasa(self) -> DefaultSamasaService:
        return self.samasa_service

    @property
    def semantic(self) -> DefaultSemanticService:
        return self.semantic_service

    # -----------------------------------------------------
    # Statistics
    # -----------------------------------------------------

    @property
    def repository_count(self) -> int:
        return 6

    @property
    def service_count(self) -> int:
        return 6

    @property
    def total_components(self) -> int:
        return (
            self.repository_count
            + self.service_count
        )
