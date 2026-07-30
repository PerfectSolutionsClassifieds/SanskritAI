from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule-Driven Stage

Abstract reusable base class for every executable
Paninian derivation stage.

This class contains ALL orchestration logic.

Concrete stages now only specify

    • display_name
    • rule_set_name

Everything else is delegated here.

Architecture

PaninianDerivationPipeline
            │
            ▼
PaninianRuleDrivenStage
            │
            ▼
PaninianRuleRepository
            │
            ▼
PaninianRuleSet
            │
            ▼
PaninianRuleEngine
            │
            ▼
PaninianRuleEngineResult
            │
            ▼
PaninianDerivationState

Benefits
--------

• No duplicated orchestration code

• Every stage executes identically

• Every grammatical operation becomes a collection of
  PaninianRule objects

• Adding new sūtras never requires changing the pipeline

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import replace

from SanskritAI.domain.panini.default_paninian_rule_repository import (
    DefaultPaninianRuleRepository,
)
from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)
from SanskritAI.domain.panini.paninian_derivation_stage import (
    PaninianDerivationStage,
)
from SanskritAI.domain.panini.paninian_derivation_state import (
    PaninianDerivationState,
)
from SanskritAI.domain.panini.paninian_rule_engine import (
    PaninianRuleEngine,
)
from SanskritAI.domain.panini.paninian_rule_engine_context import (
    PaninianRuleEngineContext,
)


class PaninianRuleDrivenStage(
    PaninianDerivationStage,
    ABC,
):
    """
    Base implementation for all Paninian stages.

    Concrete subclasses only define

        rule_set_name

    and

        display_name.
    """

    def __init__(
        self,
    ) -> None:

        self._repository = (
            DefaultPaninianRuleRepository()
        )

        self._engine = (
            PaninianRuleEngine()
        )

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def rule_set_name(
        self,
    ) -> str:
        """
        Repository identifier of the rule set.
        """
        ...

    # ---------------------------------------------------------
    # Applicability
    # ---------------------------------------------------------

    def is_applicable(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> bool:
        return bool(state.current_form)

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def apply(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> PaninianDerivationState:

        engine_context = (
            PaninianRuleEngineContext(
                derivation_context=context,
                derivation_state=state,
                stage_name=self.display_name,
            )
        )

        rule_set = (
            self._repository.require(
                self.rule_set_name,
            )
        )

        result = self._engine.execute(
            context=engine_context,
            rule_set=rule_set,
        )

        metadata = dict(
            state.metadata,
        )

        metadata[
            f"{self.rule_set_name}_processed"
        ] = True

        metadata[
            f"{self.rule_set_name}_changed"
        ] = result.changed

        metadata[
            f"{self.rule_set_name}_evaluated_rules"
        ] = result.evaluated_rules

        metadata[
            f"{self.rule_set_name}_matched_rules"
        ] = result.matched_rules

        metadata[
            f"{self.rule_set_name}_applied_rules"
        ] = result.applied_rules

        metadata[
            f"{self.rule_set_name}_engine_result"
        ] = result

        updated = replace(
            state,
            metadata=metadata,
        )

        updated = updated.add_rule(
            self.display_name,
        )

        for rule in result.applied_rules:

            updated = updated.add_rule(
                rule,
            )

        return updated.with_form(
            result.resulting_form,
            stage_name=self.display_name,
        )
