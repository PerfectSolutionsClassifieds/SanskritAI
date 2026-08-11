from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule

Canonical abstract base class for every executable
Paninian grammatical rule.

Architecture
------------

             PaninianRule
                  │
      ┌───────────┼──────────────┐
      │           │              │
  SamjnaRule  VidhiRule     SandhiRule
      │           │              │
      ▼           ▼              ▼
 Concrete Sūtras  Concrete Sūtras  Concrete Sūtras

Every rule owns exactly one immutable
PaninianRuleMetadata instance.

The metadata separates:

    • Classical Sūtra Category

          Saṃjñā
          Paribhāṣā
          Vidhi
          Niyama
          Atideśa
          Adhikāra

    from

    • Operational Behaviour

          Āgama
          Lopa
          Ādeśa
          Sandhi
          Tripādī
          Pratyaya
          Samāsa
          ...

PaninianRuleBehaviour is deliberately NOT stored as an
independent field.

It is derived from the canonical metadata so that the
same grammatical classification is not duplicated in
multiple places.

Version
-------
v3.1.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.panini.paninian_rule_behaviour import (
    PaninianRuleBehaviour,
)

from SanskritAI.domain.panini.paninian_rule_metadata import (
    PaninianRuleMetadata,
)

from SanskritAI.domain.panini.paninian_rule_operation import (
    PaninianRuleOperation,
)

from SanskritAI.domain.panini.paninian_rule_type import (
    PaninianRuleType,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PaninianRule(
    ValueObject,
    Immutable,
    Displayable,
    ABC,
):
    """
    Canonical executable Paninian grammatical rule.
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
    # Classical Classification
    # ---------------------------------------------------------

    @property
    def category(self):
        """
        Classical Paninian classification.

        Examples

            SAMJNA

            PARIBHASHA

            NIYAMA

            ATIDESHA

            ADHIKARA
        """
        return self.metadata.category

    # ---------------------------------------------------------
    # Operational Behaviour
    # ---------------------------------------------------------

    @property
    def operation(self):
        """
        Operational grammatical behaviour.

        Examples

            AGAMA

            LOPA

            ADESHA

            SANDHI
        """
        return self.metadata.operation

    # ---------------------------------------------------------
    # Derived Execution Behaviour
    # ---------------------------------------------------------

    @property
    def behaviour(self) -> PaninianRuleBehaviour:
        """
        Derived execution behaviour of this rule.

        PaninianRuleBehaviour is intentionally derived from
        the canonical metadata rather than stored independently.

        Mapping
        -------

        Saṃjñā      -> DESIGNATION
        Niyama      -> RESTRICTION
        Atideśa     -> EXTENSION
        Paribhāṣā   -> INTERPRETATION
        Adhikāra    -> SCOPE

        Operational rules with an actual grammatical operation
        are treated as TRANSFORMATION.

        Rules with no operation and no special contextual
        classification are treated as ORGANIZATIONAL.
        """

        category = self.category
        rule_type = self.rule_type
        operation = self.operation

        # -----------------------------------------------------
        # Classical semantic classifications take precedence.
        # -----------------------------------------------------

        if rule_type is PaninianRuleType.NIYAMA:
            return PaninianRuleBehaviour.RESTRICTION

        if rule_type is PaninianRuleType.ATIDESHA:
            return PaninianRuleBehaviour.EXTENSION

        category_name = getattr(
            category,
            "name",
            "",
        )

        if category_name == "SAMJNA":
            return PaninianRuleBehaviour.DESIGNATION

        if category_name == "PARIBHASHA":
            return PaninianRuleBehaviour.INTERPRETATION

        if category_name == "ADHIKARA":
            return PaninianRuleBehaviour.SCOPE

        # -----------------------------------------------------
        # Any actual grammatical operation is transformational.
        # -----------------------------------------------------

        if operation is not PaninianRuleOperation.NONE:
            return PaninianRuleBehaviour.TRANSFORMATION

        # -----------------------------------------------------
        # No operation and no special semantic classification.
        # -----------------------------------------------------

        return PaninianRuleBehaviour.ORGANIZATIONAL

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def rule_type(self):
        return self.metadata.rule_type

    @property
    def priority(self):
        return self.metadata.priority

    @property
    def source(self) -> str:
        return self.metadata.source

    @property
    def notes(self) -> str:
        return self.metadata.notes

    @property
    def tags(self) -> tuple[str, ...]:
        return self.metadata.tags

    # ---------------------------------------------------------
    # Canonical Sūtra convenience
    # ---------------------------------------------------------

    @property
    def sutra(self):
        return self.metadata.sutra

    @property
    def sutra_number(self) -> str:
        return self.metadata.sutra.sutra_number

    @property
    def sutra_text(self) -> str:
        return self.metadata.sutra.sutra_text

    @property
    def transliteration(self) -> str:
        return self.metadata.sutra.transliteration

    @property
    def translation(self) -> str:
        return self.metadata.sutra.translation

    @property
    def adhyaya(self) -> int:
        return self.metadata.sutra.adhyaya

    @property
    def pada(self) -> int:
        return self.metadata.sutra.pada

    @property
    def canonical_location(self) -> str:
        return self.metadata.sutra.canonical_location

    # ---------------------------------------------------------
    # Classification Helpers
    # ---------------------------------------------------------

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_transformational(self) -> bool:
        return self.metadata.is_transformational

    @property
    def is_phonological(self) -> bool:
        return self.metadata.is_phonological

    @property
    def is_morphological(self) -> bool:
        return self.metadata.is_morphological

    @property
    def has_operation(self) -> bool:
        return self.metadata.has_operation

    # ---------------------------------------------------------
    # Life-cycle
    # ---------------------------------------------------------

    def supports(
        self,
        context: Any,
    ) -> bool:
        """
        Determines whether this rule may participate in
        the current derivation.

        Concrete subclasses may override.
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
        Executes the grammatical transformation.

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
        Hook executed immediately after apply().
        """
        return result

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def explain(self) -> str:
        """
        Returns a human-readable explanation.
        """
        return self.display_description

    def trace(self) -> dict[str, Any]:
        """
        Returns structured trace information.
        """
        return {
            "category": self.category.value,
            "operation": self.operation.value,
            "rule_type": self.rule_type.value,
            "behaviour": self.behaviour.value,
            "priority": self.priority.value,
            "source": self.source,
            "tags": self.tags,
        }

    # ---------------------------------------------------------
    # Ordering
    # ---------------------------------------------------------

    def __lt__(
        self,
        other: "PaninianRule",
    ) -> bool:
        return self.priority.value < other.priority.value

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
