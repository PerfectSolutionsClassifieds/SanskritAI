
from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Service

Canonical concrete implementation of MorphologicalService.

This implementation merges the legacy repository/analyzer
facade with the newer Resolution Pipeline contributor model.

Responsibilities
----------------

• expose the canonical MorphologicalRepository
• expose grammatical categories
• expose the canonical MorphologicalRuleSet
• expose the canonical MorphologicalAnalyzer
• provide direct word-form analysis
• provide MorphologicalResolutionKernel resolution
• contribute morphology to ResolutionResult

Architecture
------------

ResolutionPipeline
        │
        ▼
DefaultMorphologicalService
        │
        ├── DefaultMorphologicalRepository
        │       │
        │       ├── MorphologicalRuleSet
        │       └── DefaultMorphologicalAnalyzer
        │
        └── DefaultMorphologicalResolutionKernel
                │
                └── MorphologicalResolutionStrategy
                        │
                        └── MorphologicalAnalyzer

Design Rules
------------

• No grammatical rules belong in this service.
• No repository implementation logic belongs here.
• No CanonicalKnowledgeRepository dependency belongs here.
• No KnowledgeServiceRegistry dependency belongs here.
• Resolution is delegated to the MorphologicalResolutionKernel.
• Direct analysis is delegated to the repository's analyzer.

Version
-------
v3.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.lexical.word_form import WordForm

from SanskritAI.domain.morphology.default_morphological_repository import (
    DefaultMorphologicalRepository,
)

from SanskritAI.domain.morphology.default_morphological_resolution_kernel import (
    DefaultMorphologicalResolutionKernel,
)

from SanskritAI.domain.morphology.grammatical_category_collection import (
    GrammaticalCategoryCollection,
)

from SanskritAI.domain.morphology.morphological_analysis_collection import (
    MorphologicalAnalysisCollection,
)

from SanskritAI.domain.morphology.morphological_repository import (
    MorphologicalRepository,
)

from SanskritAI.domain.morphology.morphological_resolution_context import (
    MorphologicalResolutionContext,
)

from SanskritAI.domain.morphology.morphological_resolution_kernel import (
    MorphologicalResolutionKernel,
)

from SanskritAI.domain.morphology.morphological_resolution_result import (
    MorphologicalResolutionResult,
)

from SanskritAI.domain.morphology.morphological_rule_set import (
    MorphologicalRuleSet,
)

from SanskritAI.domain.morphology.morphological_service import (
    MorphologicalService,
)

from SanskritAI.domain.morphology.lakara import Lakara
from SanskritAI.domain.morphology.linga import Linga
from SanskritAI.domain.morphology.pada import Pada
from SanskritAI.domain.morphology.prayoga import Prayoga
from SanskritAI.domain.morphology.purusha import Purusha
from SanskritAI.domain.morphology.vacana import Vacana
from SanskritAI.domain.morphology.vibhakti import Vibhakti


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultMorphologicalService(
    MorphologicalService,
    Displayable,
):
    """
    Canonical default MorphologicalService.

    The service is immutable and owns no linguistic logic.

    It delegates:

        direct analysis
            → repository.analyzer

        resolution
            → DefaultMorphologicalResolutionKernel

        pipeline contribution
            → MorphologicalService
    """

    repository: MorphologicalRepository = field(
        default_factory=DefaultMorphologicalRepository,
    )

    # =========================================================
    # Display
    # =========================================================

    @property
    def display_name(
        self,
    ) -> str:
        return "Default Morphological Service"

    @property
    def display_text(
        self,
    ) -> str:
        return self.display_name

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Canonical application service over the "
            "Morphology Kernel."
        )

    # =========================================================
    # Repository
    # =========================================================

    @property
    def morphological_repository(
        self,
    ) -> MorphologicalRepository:
        """
        Canonical morphology repository.
        """
        return self.repository

    # =========================================================
    # Resolution Kernel
    # =========================================================

    @property
    def resolution_kernel(
        self,
    ) -> MorphologicalResolutionKernel:
        """
        Construct the canonical resolution kernel using
        this service's repository.

        The kernel is intentionally created at the service
        boundary rather than stored as another mutable field.
        """

        return DefaultMorphologicalResolutionKernel(
            repository=self.repository,
        )

    # =========================================================
    # Direct Analyzer
    # =========================================================

    @property
    def analyzer(self):
        """
        Canonical morphological analyzer.
        """

        return self.repository.morphological_analyzer

    # =========================================================
    # Analysis
    # =========================================================

    def analyze(
        self,
        word_form: WordForm,
    ) -> MorphologicalAnalysisCollection:
        """
        Perform direct morphological analysis.

        This is the low-level convenience API.

        ResolutionPipeline callers should normally use
        resolve() instead.
        """

        return self.analyzer.analyze(
            word_form,
        )

    # =========================================================
    # Resolution
    # =========================================================

    def resolve(
        self,
        context: MorphologicalResolutionContext,
    ) -> MorphologicalResolutionResult:
        """
        Perform canonical morphological resolution.
        """

        return self.resolution_kernel.resolve(
            context,
        )

    # =========================================================
    # Convenience Resolution
    # =========================================================

    def __call__(
        self,
        context: MorphologicalResolutionContext,
    ) -> MorphologicalResolutionResult:
        return self.resolve(
            context,
        )

    # =========================================================
    # Grammatical Categories
    # =========================================================

    @property
    def vibhakti(self) -> Vibhakti:
        return self.repository.vibhakti

    @property
    def vacana(self) -> Vacana:
        return self.repository.vacana

    @property
    def linga(self) -> Linga:
        return self.repository.linga

    @property
    def purusha(self) -> Purusha:
        return self.repository.purusha

    @property
    def lakara(self) -> Lakara:
        return self.repository.lakara

    @property
    def pada(self) -> Pada:
        return self.repository.pada

    @property
    def prayoga(self) -> Prayoga:
        return self.repository.prayoga

    # =========================================================
    # Category Collections
    # =========================================================

    @property
    def nominal_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        return self.repository.nominal_categories

    @property
    def verbal_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        return self.repository.verbal_categories

    @property
    def all_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        return self.repository.all_categories

    # =========================================================
    # Rule Set
    # =========================================================

    @property
    def rule_set(
        self,
    ) -> MorphologicalRuleSet:
        return self.repository.morphological_rule_set

    @property
    def morphological_rule_set(
        self,
    ) -> MorphologicalRuleSet:
        return self.repository.morphological_rule_set

    # =========================================================
    # Statistics
    # =========================================================

    @property
    def count(
        self,
    ) -> int:
        return self.repository.count

    # =========================================================
    # String Representation
    # =========================================================

    def __str__(
        self,
    ) -> str:
        return self.display_text
