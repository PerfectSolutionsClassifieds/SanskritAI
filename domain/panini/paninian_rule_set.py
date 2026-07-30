from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Set

Defines the executable collection of Paninian rules.

Unlike PaninianRuleCollection (which is simply an immutable
container), PaninianRuleSet knows how to evaluate a context by

    1. Selecting applicable rules
    2. Ordering them by priority
    3. Executing them
    4. Returning candidate outputs

The rule set is completely kernel-independent and serves as the
shared execution mechanism for

    • Sandhi
    • Samāsa
    • Dhātu
    • Pratyaya
    • Derivation
    • Grammar
    • Vākya
    • Semantics
    • Chandas
    • Alaṅkāra

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.panini.paninian_rule import PaninianRule
from SanskritAI.domain.panini.paninian_rule_collection import (
    PaninianRuleCollection,
)


@dataclass(frozen=True, slots=True)
class PaninianRuleSet(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Executable Paninian rule set.
    """

    rules: PaninianRuleCollection

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Paninian Rule Set"

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name}"
            f" ({self.rule_count} rules)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Executable collection of canonical "
            "Paninian grammatical rules."
        )

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def rule_count(self) -> int:
        return self.rules.count

    @property
    def is_empty(self) -> bool:
        return self.rules.is_empty

    @property
    def enabled_rules(
        self,
    ) -> PaninianRuleCollection:
        return (
            self.rules
            .enabled()
            .sorted()
        )

    # ---------------------------------------------------------
    # Rule selection
    # ---------------------------------------------------------

    def applicable_rules(
        self,
        context: Any,
    ) -> PaninianRuleCollection:
        """
        Returns all enabled rules that support
        the supplied context.
        """

        applicable = []

        for rule in self.enabled_rules:
            try:
                if rule.supports(context):
                    applicable.append(rule)
            except Exception:
                # Individual rules should never stop the
                # execution of the complete rule set.
                continue

        return PaninianRuleCollection(
            tuple(applicable)
        )

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def apply(
        self,
        context: Any,
    ) -> tuple[Any, ...]:
        """
        Executes all applicable rules.

        Returns
        -------
        tuple[Any, ...]

        Candidate outputs accumulated from every rule.
        """

        outputs: list[Any] = []

        for rule in self.applicable_rules(context):

            try:
                result = rule.apply(context)

                if not result:
                    continue

                outputs.extend(result)

            except Exception:
                # Future versions may emit diagnostics here.
                continue

        return tuple(outputs)

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def add_rule(
        self,
        rule: PaninianRule,
    ) -> "PaninianRuleSet":
        """
        Returns a new RuleSet with the supplied rule.
        """

        return PaninianRuleSet(
            rules=self.rules.add(rule)
        )

    def remove_rule(
        self,
        identifier: str,
    ) -> "PaninianRuleSet":
        """
        Returns a new RuleSet with one rule removed.
        """

        return PaninianRuleSet(
            rules=self.rules.remove_by_identifier(
                identifier
            )
        )

    def __len__(self) -> int:
        return self.rule_count

    def __iter__(self):
        return iter(self.rules)

    def __str__(self) -> str:
        return self.display_text
