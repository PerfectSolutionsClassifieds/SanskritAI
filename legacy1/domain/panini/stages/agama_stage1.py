from __future__ import annotations

"""
SanskritAI
==========

Āgama Stage

Canonical Phase-2 stage of the Paninian Derivation Pipeline.

Purpose
-------
Processes Paninian Āgama (augment) operations.

An Āgama is an element inserted into the derivation without
replacing existing material.

Examples (future implementations)

    • इट्-आगम
    • नुम्-आगम
    • मुक्
    • तुक्
    • शप्
    • श्नु
    • सिच्
    • various vikaraṇa augment rules

This stage intentionally contains only the orchestration
framework.

Actual augment rules will later be implemented as
PaninianRule objects.

Pipeline Position
-----------------

Dhātu Selection
        ↓
Pratyaya Selection
        ↓
It-Saṃjñā
        ↓
Aṅga Processing
        ↓
Guṇa–Vṛddhi
        ↓
Āgama              ← this stage
        ↓
Lopa
        ↓
Substitution
        ↓
Sandhi

Version
-------
v1.0.0
"""

from dataclasses import replace

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)
from SanskritAI.domain.panini.paninian_derivation_stage import (
    PaninianDerivationStage,
)
from SanskritAI.domain.panini.paninian_derivation_state import (
    PaninianDerivationState,
)


class AgamaStage(
    PaninianDerivationStage,
):
    """
    Executes Paninian augment rules.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Āgama"

    @property
    def display_description(self) -> str:
        return (
            "Applies Paninian augment (Āgama) rules."
        )

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
    # Internal Rule Engine (placeholder)
    # ---------------------------------------------------------

    def _apply_agama(
        self,
        form: str,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> tuple[str, list[str], list[str]]:
        """
        Executes Āgama rules.

        Returns
        -------
        (
            transformed_form,
            inserted_augments,
            applied_paninian_rules,
        )

        Current implementation performs no insertion.
        """

        inserted_augments: list[str] = []
        applied_rules: list[str] = []

        #
        # Future implementation:
        #
        # for rule in agama_rule_set:
        #     if rule.matches(...):
        #         form = rule.apply(...)
        #         inserted_augments.append(...)
        #         applied_rules.append(rule.identifier)
        #

        return (
            form,
            inserted_augments,
            applied_rules,
        )

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def apply(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> PaninianDerivationState:

        current = state.current_form

        (
            transformed,
            augments,
            rules,
        ) = self._apply_agama(
            current,
            context,
            state,
        )

        metadata = dict(state.metadata)

        metadata["agama_processed"] = True
        metadata["agama_changed"] = (
            transformed != current
        )
        metadata["inserted_agamas"] = tuple(
            augments
        )
        metadata["agama_count"] = len(
            augments
        )
        metadata["agama_rules"] = tuple(
            rules
        )

        updated = replace(
            state,
            metadata=metadata,
        )

        updated = updated.add_rule(
            self.display_name
        )

        for rule in rules:
            updated = updated.add_rule(
                rule
            )

        return updated.with_form(
            transformed,
            stage_name=self.display_name,
        )
