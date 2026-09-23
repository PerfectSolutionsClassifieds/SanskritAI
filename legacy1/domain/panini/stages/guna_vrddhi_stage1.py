from __future__ import annotations

"""
SanskritAI
==========

Guṇa–Vṛddhi Stage

Canonical Phase-2 stage of the Paninian Derivation Pipeline.

Purpose
-------
This stage performs vowel-strengthening operations on the
current Aṅga whenever permitted by the Paninian rule system.

The current implementation intentionally provides only the
framework.

Actual Guṇa / Vṛddhi transformations will gradually be
implemented by adding PaninianRule objects corresponding to
individual sūtras.

Examples

इ  → ए   (Guṇa)
उ  → ओ
ऋ  → अर्

ए  → ऐ   (Vṛddhi)
ओ  → औ
अर् → आर्

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
Guṇa–Vṛddhi      ← this stage
        ↓
Āgama
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


class GunaVrddhiStage(
    PaninianDerivationStage,
):
    """
    Applies Guṇa and Vṛddhi operations.

    Initial implementation only prepares the pipeline
    architecture.

    Future implementations will execute PaninianRule objects
    belonging to this stage.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Guṇa–Vṛddhi"

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Applies Guṇa and Vṛddhi transformations "
            "to the current Aṅga."
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

    def _apply_guna_vrddhi(
        self,
        form: str,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> tuple[str, list[str]]:
        """
        Executes Guṇa/Vṛddhi rules.

        Current implementation intentionally performs no
        phonological transformation.

        Future versions will dispatch PaninianRule objects
        belonging to the Guṇa–Vṛddhi subsystem.

        Returns
        -------
        (new_form, applied_rules)
        """

        applied_rules: list[str] = []

        #
        # Placeholder.
        #
        # Future implementation:
        #
        # for rule in self.rule_set:
        #     if rule.matches(...):
        #         form = rule.apply(...)
        #         applied_rules.append(rule.identifier)
        #

        return form, applied_rules

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def apply(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> PaninianDerivationState:

        current = state.current_form

        transformed, paninian_rules = (
            self._apply_guna_vrddhi(
                current,
                context,
                state,
            )
        )

        metadata = dict(state.metadata)

        metadata["guna_vrddhi_processed"] = True
        metadata["guna_vrddhi_changed"] = (
            transformed != current
        )
        metadata["guna_vrddhi_rule_count"] = (
            len(paninian_rules)
        )
        metadata["guna_vrddhi_rules"] = tuple(
            paninian_rules
        )

        updated = replace(
            state,
            metadata=metadata,
        )

        updated = updated.add_rule(
            self.display_name
        )

        for rule in paninian_rules:
            updated = updated.add_rule(rule)

        return updated.with_form(
            transformed,
            stage_name=self.display_name,
        )
