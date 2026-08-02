from __future__ import annotations

"""
SanskritAI
==========

Paninian Derivation Engine

Canonical orchestration engine for executable
Paninian grammar.

Responsibilities
----------------

• owns derivation lifecycle

• discovers applicable rules

• executes rules

• records derivation history

• produces explainable execution traces

Architecture
------------

PaninianDerivationContext
            │
            ▼
PaninianDerivationEngine
            │
     ┌──────┴────────┐
     ▼               ▼
PaninianRuleMatcher  PaninianSutraCatalog
            │               │
            └──────┬────────┘
                   ▼
             Executable Rules

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.domain.panini.paninian_rule import PaninianRule
from SanskritAI.domain.panini.paninian_rule_matcher import PaninianRuleMatcher
from SanskritAI.domain.panini.paninian_sutra_catalog import PaninianSutraCatalog


@dataclass(slots=True)
class PaninianDerivationEngine:
    """
    Canonical orchestration engine.
    """

    catalog: PaninianSutraCatalog = field(
        default_factory=PaninianSutraCatalog,
    )

    matcher: PaninianRuleMatcher | None = None

    execution_history: list[dict[str, Any]] = field(
        default_factory=list,
    )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def before_derivation(
        self,
        context: Any,
    ) -> Any:
        """
        Hook executed before derivation.
        """
        return context

    def after_derivation(
        self,
        context: Any,
    ) -> Any:
        """
        Hook executed after derivation.
        """
        return context

    # ---------------------------------------------------------
    # Rule execution
    # ---------------------------------------------------------

    def execute_rule(
        self,
        rule: PaninianRule,
        context: Any,
    ) -> tuple[Any, ...]:
        """
        Executes one Paninian rule.
        """

        result = rule.apply(context)

        self.execution_history.append(
            {
                "sutra_number": rule.sutra_number,
                "sutra": rule.sutra,
                "operation": rule.metadata.operation.name,
                "rule_type": rule.metadata.rule_type.name,
            }
        )

        return result

    # ---------------------------------------------------------
    # Derivation
    # ---------------------------------------------------------

    def derive(
        self,
        context: Any,
    ) -> Any:
        """
        Performs one derivation cycle.

        NOTE
        ----
        This first version performs orchestration only.

        Rule scheduling, conflict resolution,
        iterative derivation, optional rules,
        vipratiṣedha, etc. will be added later.
        """

        context = self.before_derivation(
            context,
        )

        if self.matcher is None:
            raise RuntimeError(
                "No PaninianRuleMatcher configured."
            )

        matches = self.matcher.match(
            context=context,
            rules=self.catalog.all(),
        )

        for match in matches:

            if not match.matched:
                continue

            self.execute_rule(
                match.rule,
                context,
            )

        context = self.after_derivation(
            context,
        )

        return context

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def executed_rule_count(
        self,
    ) -> int:
        return len(self.execution_history)

    def clear_history(
        self,
    ) -> None:
        self.execution_history.clear()

    def summary(
        self,
    ) -> dict:
        return {
            "executed_rules": self.executed_rule_count,
            "catalog_size": self.catalog.count,
        }
