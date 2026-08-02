from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule

Canonical abstract base class for every executable
Paninian grammatical rule.

Purpose
-------
PaninianRule represents one executable grammatical rule of the
Aṣṭādhyāyī.

Unlike previous versions, descriptive information is no longer
stored directly inside the rule.

Every rule instead owns a

    PaninianRuleMetadata

instance, making metadata reusable throughout SanskritAI.

Architecture
------------

                PaninianRule
                     │
     ┌───────────────┼────────────────┐
     │               │                │
 SamjnaRule      VidhiRule      SandhiRule
     │               │                │
     ▼               ▼                ▼
Concrete Sutra  Concrete Sutra  Concrete Sutra

Responsibilities
----------------

PaninianRule

• determines applicability

• validates execution

• performs grammatical transformation

• participates in tracing

• exposes immutable metadata

Version
-------
v2.0.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.panini.paninian_rule_metadata import (
    PaninianRuleMetadata,
)


@dataclass(frozen=True, slots=True)
class PaninianRule(
    ValueObject,
    Immutable,
    Displayable,
    ABC,
):
    """
    Canonical executable Paninian rule.
    """

    metadata: PaninianRuleMetadata

    enabled: bool = True

    runtime_metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.metadata.display_name

    @property
    def display_text(self) -> str:
        return self.metadata.display_text

    @property
    def display_description(self) -> str:
        return self.metadata.display_description

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        return self.metadata.rule_name

    @property
    def sutra_number(self) -> str:
        return self.metadata.sutra_number

    @property
    def sutra(self) -> str:
        return self.metadata.sutra_text

    @property
    def category(self):
        return self.metadata.category

    @property
    def rule_type(self):
        return self.metadata.rule_type

    @property
    def priority(self):
        return self.metadata.priority

    @property
    def adhyaya(self) -> int:
        return self.metadata.adhyaya

    @property
    def pada(self) -> int:
        return self.metadata.pada

    @property
    def location(self) -> str:
        return self.metadata.canonical_location

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_optional(self) -> bool:
        return self.metadata.is_optional

    @property
    def is_exception(self) -> bool:
        return self.metadata.is_exception

    @property
    def is_default_rule(self) -> bool:
        return self.metadata.is_default_rule

    @property
    def is_meta_rule(self) -> bool:
        return self.metadata.is_meta_rule

    @property
    def is_morphological(self) -> bool:
        return self.metadata.is_morphological

    @property
    def is_phonological(self) -> bool:
        return self.metadata.is_phonological

    @property
    def is_semantic(self) -> bool:
        return self.metadata.is_semantic

    # ---------------------------------------------------------
    # Execution Life-cycle
    # ---------------------------------------------------------

    def supports(
        self,
        context: Any,
    ) -> bool:
        """
        Determines whether this rule may participate
        in the current derivation.

        Concrete rules may override.
        """
        return self.enabled

    def validate(
        self,
        context: Any,
    ) -> bool:
        """
        Performs rule-specific validation.

        Default implementation accepts every context.
        """
        return True

    def before_apply(
        self,
        context: Any,
    ) -> Any:
        """
        Hook executed immediately before apply().
        """
        return context

    @abstractmethod
    def apply(
        self,
        context: Any,
    ) -> tuple[Any, ...]:
        """
        Applies the grammatical rule.

        Returns
        -------
        tuple[Any, ...]

        Zero or more candidate derivations.
        """
        raise NotImplementedError

    def after_apply(
        self,
        context: Any,
        result: tuple[Any, ...],
    ) -> tuple[Any, ...]:
        """
        Hook executed after apply().
        """
        return result

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def explain(self) -> str:
        """
        Returns the canonical explanation.
        """
        return self.metadata.display_description

    def trace(self) -> dict[str, Any]:
        """
        Returns a structured trace payload.
        """
        return {
            "sutra_number": self.sutra_number,
            "sutra": self.sutra,
            "category": self.category.value,
            "rule_type": self.rule_type.value,
            "priority": int(self.priority),
            "location": self.location,
        }

    # ---------------------------------------------------------
    # Ordering
    # ---------------------------------------------------------

    def __lt__(
        self,
        other: "PaninianRule",
    ) -> bool:
        return self.priority < other.priority

    def __str__(self) -> str:
        return self.display_text
