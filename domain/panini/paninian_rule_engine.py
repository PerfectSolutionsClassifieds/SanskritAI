from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Engine

Canonical execution engine for PaninianRule objects.

Responsibilities
----------------

The engine is intentionally grammar-independent.

It only

    • iterates through rules
    • evaluates applicability
    • applies matching rules
    • records execution statistics
    • returns an immutable
      PaninianRuleEngineResult

Actual grammatical intelligence belongs exclusively to

    • PaninianRule
    • PaninianRuleSet
    • PaninianRuleRepository

Pipeline

Stage
   ↓
Rule Engine
   ↓
Rule Set
   ↓
Rules
   ↓
Rule Engine Result

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.panini.paninian_rule_engine_context import (
    PaninianRuleEngineContext,
)
from SanskritAI.domain.panini.paninian_rule_engine_result import (
    PaninianRuleEngineResult,
)
from SanskritAI.domain.panini.paninian_rule_set import (
    PaninianRuleSet,
)
from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)


@dataclass(slots=True)
class PaninianRuleEngine(Displayable):
    """
    Executes PaninianRule objects.

    The engine itself contains absolutely no grammatical
    knowledge.

    All grammar resides inside PaninianRule subclasses.
    """

    stop_after_first_match: bool = False

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Paninian Rule Engine"

    @property
    def display_description(self) -> str:
        return (
            "Executes PaninianRule objects over a "
            "PaninianRuleSet."
        )

    # ---------------------------------------------------------
    # Rule Execution
    # ---------------------------------------------------------

    def execute(
        self,
        *,
        context: PaninianRuleEngineContext,
        rule_set: PaninianRuleSet,
    ) -> PaninianRuleEngineResult:
        """
        Executes every rule in the supplied rule set.

        Parameters
        ----------
        context
            Immutable execution context.

        rule_set
            Ordered Paninian rule collection.

        Returns
        -------
        PaninianRuleEngineResult
        """

        current_form = context.current_form

        evaluated_rules: list[str] = []
        matched_rules: list[str] = []
        applied_rules: list[str] = []

        #
        # Execute rules in canonical order.
        #
        for rule in rule_set:

            if not isinstance(
                rule,
                PaninianRule,
            ):
                continue

            evaluated_rules.append(
                rule.display_name,
            )

            if not rule.matches(context):

                continue

            matched_rules.append(
                rule.display_name,
            )

            new_form = rule.apply(
                current_form,
                context,
            )

            #
            # Only record actual transformations.
            #
            if new_form != current_form:

                current_form = new_form

                applied_rules.append(
                    rule.display_name,
                )

            if (
                self.stop_after_first_match
                and applied_rules
            ):
                break

        return PaninianRuleEngineResult(
            resulting_form=current_form,
            evaluated_rules=tuple(
                evaluated_rules,
            ),
            matched_rules=tuple(
                matched_rules,
            ),
            applied_rules=tuple(
                applied_rules,
            ),
            metadata={
                "stage": context.stage,
                "rule_count": len(rule_set),
                "evaluated": len(
                    evaluated_rules,
                ),
                "matched": len(
                    matched_rules,
                ),
                "applied": len(
                    applied_rules,
                ),
            },
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def execute_single_rule(
        self,
        *,
        context: PaninianRuleEngineContext,
        rule: PaninianRule,
    ) -> PaninianRuleEngineResult:
        """
        Executes a single Paninian rule.

        Useful for unit testing individual sūtras.
        """

        return self.execute(
            context=context,
            rule_set=PaninianRuleSet(
                rules=[rule],
            ),
        )

    def __str__(self) -> str:
        return self.display_name
