from __future__ import annotations

"""
SanskritAI
==========

Default Derivation Repository

Canonical in-memory derivation repository.

This version includes real derivation blueprints so the
Morphological Derivation Kernel can move beyond simple
bootstrap patterns and toward reusable derivational
templates.

Version
-------
v1.2.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.derivation.derivation_pattern import DerivationPattern
from SanskritAI.domain.derivation.derivation_pattern_collection import (
    DerivationPatternCollection,
)
from SanskritAI.domain.derivation.derivation_repository import (
    DerivationRepository,
)


DEFAULT_DERIVATION_PATTERNS: tuple[DerivationPattern, ...] = (
    DerivationPattern(
        identifier="derivation.bhu_kta",
        name="Bhū + Kta Blueprint",
        template="भू + क्त -> भूत",
        description=(
            "Blueprint for the canonical bhū + kta derivation."
        ),
        category="blueprint",
        priority=1,
    ),
    DerivationPattern(
        identifier="derivation.kri_kta",
        name="Kṛ + Kta Blueprint",
        template="कृ + क्त -> कृत",
        description=(
            "Blueprint for the canonical kṛ + kta derivation."
        ),
        category="blueprint",
        priority=2,
    ),
    DerivationPattern(
        identifier="derivation.gam_lyap",
        name="Gam + Lyap Blueprint",
        template="गम् + ल्यप् -> गत्वा",
        description=(
            "Blueprint for the canonical gam + lyap derivation."
        ),
        category="blueprint",
        priority=3,
    ),
    DerivationPattern(
        identifier="derivation.kri_lyap",
        name="Kṛ + Lyap Blueprint",
        template="कृ + ल्यप् -> कृत्वा",
        description=(
            "Blueprint for the canonical kṛ + lyap derivation."
        ),
        category="blueprint",
        priority=4,
    ),
    DerivationPattern(
        identifier="derivation.direct_concat",
        name="Direct Concatenation",
        template="Dhatu + Pratyaya -> Surface",
        description=(
            "Baseline derivation pattern that combines a dhatu "
            "and a pratyaya directly."
        ),
        category="baseline",
        priority=10,
    ),
    DerivationPattern(
        identifier="derivation.hint_based",
        name="Hint Based Derivation",
        template="Metadata hinted -> Surface",
        description=(
            "Pattern used when the caller provides an explicit "
            "derived surface form hint."
        ),
        category="hinted",
        priority=20,
    ),
)


@dataclass(frozen=True, slots=True)
class DefaultDerivationRepository(
    DerivationRepository,
):
    """
    Canonical in-memory derivation repository.
    """

    patterns: DerivationPatternCollection = field(
        default_factory=lambda: DerivationPatternCollection(
            patterns=DEFAULT_DERIVATION_PATTERNS,
        )
    )

    @property
    def display_name(self) -> str:
        return "Default Derivation Repository"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical in-memory derivation repository."

    def get(self, identifier: str) -> DerivationPattern | None:
        return self.patterns.get_by_identifier(identifier)

    def find_by_category(
        self,
        category: str,
    ) -> DerivationPatternCollection:
        return self.patterns.find_by_category(category)

    def search(self, query: str) -> DerivationPatternCollection:
        return self.patterns.search(query)

    def all(self) -> DerivationPatternCollection:
        return self.patterns

    def contains(self, identifier: str) -> bool:
        return self.get(identifier) is not None

    @property
    def count(self) -> int:
        return self.patterns.count
