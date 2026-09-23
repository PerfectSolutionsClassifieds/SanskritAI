from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Metadata

Canonical immutable metadata describing a Paninian rule.

Purpose
-------
Every PaninianRule owns exactly one PaninianRuleMetadata
instance.

The metadata contains descriptive information only.
It contains no grammatical logic.

This object answers questions such as

    • Which sūtra is this?
    • Which chapter does it belong to?
    • What grammatical family is it?
    • How should it behave?
    • What is its execution priority?

The metadata layer is intentionally independent of the
Rule Engine and Pipeline so that it can also be used by

    • Documentation
    • Knowledge Graph
    • Semantic Kernel
    • Educational UI
    • Rule Explorer
    • Diagnostics

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.panini.paninian_rule_category import (
    PaninianRuleCategory,
)
from SanskritAI.domain.panini.paninian_rule_priority import (
    PaninianRulePriority,
)
from SanskritAI.domain.panini.paninian_rule_type import (
    PaninianRuleType,
)


@dataclass(frozen=True, slots=True)
class PaninianRuleMetadata(Displayable):
    """
    Immutable metadata describing one Paninian rule.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    sutra_number: str

    sutra_text: str

    rule_name: str

    # ---------------------------------------------------------
    # Location inside Aṣṭādhyāyī
    # ---------------------------------------------------------

    adhyaya: int

    pada: int

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    category: PaninianRuleCategory

    rule_type: PaninianRuleType

    priority: PaninianRulePriority = (
        PaninianRulePriority.default()
    )

    # ---------------------------------------------------------
    # Documentation
    # ---------------------------------------------------------

    description: str = ""

    commentary: str = ""

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    dependencies: tuple[str, ...] = field(
        default_factory=tuple,
    )

    overrides: tuple[str, ...] = field(
        default_factory=tuple,
    )

    references: tuple[str, ...] = field(
        default_factory=tuple,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.rule_name

    @property
    def display_text(self) -> str:
        return (
            f"{self.sutra_number} "
            f"{self.sutra_text}"
        )

    @property
    def display_description(self) -> str:
        return (
            self.description
            or self.commentary
            or self.display_text
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @property
    def canonical_location(self) -> str:
        """
        Returns canonical Aṣṭādhyāyī location.

        Example

            6.1
        """
        return (
            f"{self.adhyaya}.{self.pada}"
        )

    @property
    def has_dependencies(self) -> bool:
        return bool(self.dependencies)

    @property
    def has_overrides(self) -> bool:
        return bool(self.overrides)

    @property
    def has_references(self) -> bool:
        return bool(self.references)

    @property
    def is_meta_rule(self) -> bool:
        return self.category.is_meta_rule

    @property
    def is_morphological(self) -> bool:
        return self.category.is_morphological

    @property
    def is_phonological(self) -> bool:
        return self.category.is_phonological

    @property
    def is_semantic(self) -> bool:
        return self.category.is_semantic

    @property
    def is_optional(self) -> bool:
        return self.rule_type.is_optional

    @property
    def is_exception(self) -> bool:
        return self.rule_type.is_exception

    @property
    def is_default_rule(self) -> bool:
        return self.rule_type.is_default

    def __str__(self) -> str:
        return (
            f"{self.sutra_number} "
            f"{self.rule_name}"
        )

    def __repr__(self) -> str:
        return (
            f"PaninianRuleMetadata("
            f"sutra='{self.sutra_number}', "
            f"name='{self.rule_name}')"
        )
