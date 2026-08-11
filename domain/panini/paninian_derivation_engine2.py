from __future__ import annotations

"""
SanskritAI
==========

Paninian Derivation Engine

Canonical execution engine for the Paninian grammar.

Responsibilities
----------------

• accepts an immutable PaninianDerivationContext

• discovers applicable rules

• resolves conflicts using the canonical
  Paribhāṣā pipeline

• executes rules

• produces a NEW immutable derivation context

• records a complete PaninianExecutionTrace

Architecture
------------

PaninianDerivationContext
            │
            ▼
PaninianRuleMatcher
            │
            ▼
PaninianRuleConflict
            │
            ▼
DefaultPaninianConflictPipeline
            │
            ▼
Selected Rule(s)
            │
            ▼
Rule.apply()
            │
            ▼
New PaninianDerivationContext
            │
            ▼
PaninianExecutionTrace

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.panini.default_paninian_rule_matcher import (
    DefaultPaninianRuleMatcher,
)

from SanskritAI.domain.panini.paninian_default_conflict_pipeline import (
    DefaultPaninianConflictPipeline,
)

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)

from SanskritAI.domain.panini.paninian_execution_step import (
    PaninianExecutionStep,
)

from SanskritAI.domain.panini.paninian_execution_trace import (
    PaninianExecutionTrace,
)

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)

from SanskritAI.domain.panini.paninian_rule_conflict import (
    PaninianRuleConflict,
)

from SanskritAI.domain.panini.paninian_sutra_catalog import (
    PaninianSutraCatalog,
)


@dataclass(slots=True)
class PaninianDerivationEngine:
    """
    Canonical Paninian derivation engine.
    """

    catalog: PaninianSutraCatalog = field(
        default_factory=PaninianSutraCatalog,
    )

    matcher: DefaultPaninianRuleMatcher = field(
        default_factory=DefaultPaninianRuleMatcher,
    )

    conflict_pipeline: DefaultPaninianConflictPipeline = field(
        default_factory=DefaultPaninianConflictPipeline,
    )

    trace: PaninianExecutionTrace = field(
        default_factory=PaninianExecutionTrace,
        init=False,
    )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def before_derivation(
        self,
        context: PaninianDerivationContext,
    ) -> PaninianDerivationContext:
        """
        Hook executed before derivation.
        """
        return context

    def after_derivation(
        self,
        context: PaninianDerivationContext,
    ) -> PaninianDerivationContext:
        """
        Hook executed after derivation.
        """
        return context

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------

    def _record_step(
        self,
        *,
        before: PaninianDerivationContext,
        rule: PaninianRule,
        after: PaninianDerivationContext,
        candidates: tuple = (),
    ) -> None:
        """
        Appends one execution step.
        """

        step = PaninianExecutionStep(
            before=before,
            rule=rule,
            after=after,
            candidates=candidates,
        )

        self.trace = self.trace.append(
            step,
        )

    # ---------------------------------------------------------
    # Rule execution
    # ---------------------------------------------------------

    def execute_rule(
        self,
        rule: PaninianRule,
        context: PaninianDerivationContext,
    ) -> PaninianDerivationContext:
        """
        Executes one rule.

        Every executable rule returns one or more
        candidate derivation contexts.
        """

        candidates = rule.apply(
            context,
        )

        if not candidates:
            return context

        new_context = candidates[0]

        if not isinstance(
            new_context,
            PaninianDerivationContext,
        ):
            raise TypeError(
                f"{rule.display_name} returned "
                "an invalid derivation context."
            )

        self._record_step(
            before=context,
            rule=rule,
            after=new_context,
            candidates=candidates,
        )

        return new_context

    # ---------------------------------------------------------
    # Canonical derivation
    # ---------------------------------------------------------

    def derive(
        self,
        context: PaninianDerivationContext,
    ) -> PaninianDerivationContext:
        """
        Performs one derivation cycle.
        """

        context = self.before_derivation(
            context,
        )

        # ---------------------------------------------
        # Rule matching
        # ---------------------------------------------

        match_results = self.matcher.match(
            context=context,
            rules=self.catalog.all(),
        )

        matched_rules = tuple(
            result.rule
            for result in match_results
            if result.matched
        )

        if not matched_rules:
            return self.after_derivation(
                context,
            )

        # ---------------------------------------------
        # Conflict resolution
        # ---------------------------------------------

        if len(matched_rules) > 1:

            conflict = PaninianRuleConflict(
                context=context,
                candidate_rules=matched_rules,
            )

            matched_rules = (
                self.conflict_pipeline
                .get_pipeline()
                .resolve(
                    conflict,
                )
            )

        # ---------------------------------------------
        # Execute selected rules
        # ---------------------------------------------

        current_context = context

        for rule in matched_rules:

            current_context = self.execute_rule(
                rule,
                current_context,
            )

        return self.after_derivation(
            current_context,
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def execution_trace(
        self,
    ) -> PaninianExecutionTrace:
        return self.trace

    @property
    def executed_rule_count(
        self,
    ) -> int:
        return self.trace.step_count

    def clear_trace(
        self,
    ) -> None:
        """
        Clears execution history.
        """
        self.trace = PaninianExecutionTrace()

    def summary(
        self,
    ) -> dict:
        return {
            "catalog_size": self.catalog.count,
            "executed_rules": self.executed_rule_count,
            "trace_steps": self.trace.step_count,
            "pipeline": (
                self.conflict_pipeline.summary()
            ),
        }

    def __str__(
        self,
    ) -> str:
        return (
            "PaninianDerivationEngine("
            f"{self.executed_rule_count} executed rules)"
        )
