from __future__ import annotations

"""
SanskritAI
==========

Paninian Grammar

Canonical Aggregate Root representing the
complete executable Pāṇinian grammar.

Purpose
-------

PaninianGrammar is the single immutable entry
point for every grammatical service provided by
SanskritAI.

All future grammatical knowledge—including
Aṣṭādhyāyī, Dhātupāṭha, Gaṇapāṭha, Uṇādi,
Paribhāṣā, Kāśikā and Siddhānta-Kaumudī—
will eventually become children of this object.

Architecture
------------

PaninianGrammar
        │
        ├── Manifest
        ├── Loader
        ├── Registry
        ├── Index
        ├── Catalog
        ├── Rule Matcher
        ├── Conflict Pipeline
        └── Derivation Engine

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.panini.paninian_sutra_manifest import (
    PaninianSutraManifest,
)

from SanskritAI.domain.panini.paninian_sutra_loader import (
    PaninianSutraLoader,
)

from SanskritAI.domain.panini.paninian_sutra_registry import (
    PaninianSutraRegistry,
)

from SanskritAI.domain.panini.paninian_sutra_catalog import (
    PaninianSutraCatalog,
)

from SanskritAI.domain.panini.default_paninian_rule_matcher import (
    DefaultPaninianRuleMatcher,
)

from SanskritAI.domain.panini.paninian_default_conflict_pipeline import (
    DefaultPaninianConflictPipeline,
)

from SanskritAI.domain.panini.paninian_derivation_engine import (
    PaninianDerivationEngine,
)


@dataclass(frozen=True, slots=True)
class PaninianGrammar:
    """
    Immutable executable Paninian grammar.
    """

    manifest: PaninianSutraManifest = field(
        default_factory=PaninianSutraManifest,
    )

    loader: PaninianSutraLoader = field(
        default_factory=PaninianSutraLoader,
    )

    registry: PaninianSutraRegistry = field(
        default_factory=PaninianSutraRegistry,
    )

    catalog: PaninianSutraCatalog = field(
        default_factory=PaninianSutraCatalog,
    )

    matcher: DefaultPaninianRuleMatcher = field(
        default_factory=DefaultPaninianRuleMatcher,
    )

    conflict_pipeline: DefaultPaninianConflictPipeline = field(
        default_factory=DefaultPaninianConflictPipeline,
    )

    derivation_engine: PaninianDerivationEngine = field(
        default_factory=PaninianDerivationEngine,
    )

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    @property
    def sutra_count(
        self,
    ) -> int:
        return self.catalog.count

    @property
    def implemented_sutras(
        self,
    ):
        return self.manifest.implemented_sutra_numbers

    @property
    def implementation_percentage(
        self,
    ) -> float:
        return self.manifest.implementation_percentage

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        return {

            "sutras":
                self.sutra_count,

            "coverage":
                round(
                    self.implementation_percentage,
                    4,
                ),

            "manifest":
                self.manifest.summary(),

            "catalog":
                self.catalog.summary(),

            "pipeline":
                self.conflict_pipeline.summary(),

            "engine":
                self.derivation_engine.summary(),

        }

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return (
            "PaninianGrammar("
            f"{self.sutra_count} executable sūtras)"
        )
