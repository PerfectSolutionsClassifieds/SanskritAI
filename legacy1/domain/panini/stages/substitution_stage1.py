from __future__ import annotations

"""
SanskritAI
==========

Substitution Stage (Ādeśa)

Canonical Phase-2 stage of the Paninian Derivation Pipeline.

Purpose
-------
Executes Paninian substitution (आदेश) operations.

Unlike Lopa (deletion) and Āgama (insertion), this stage
replaces one linguistic unit with another.

Examples implemented in future versions

    • गुणादेश
    • वृद्धिादेश
    • यणादेश
    • संप्रसारण
    • आत्व
    • इत्व
    • एत्व
    • ओत्व
    • सकारादेश
    • षत्व
    • णत्व
    • अनेक धात्वादेशाः
    • प्रत्ययादेशाः

Current implementation
----------------------

This file intentionally implements only the orchestration
framework.

Actual substitutions will later be supplied by
PaninianRule objects loaded from PaninianRuleRepository.

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
Āgama
        ↓
Lopa
        ↓
Substitution (Ādeśa)
        ↓
Sandhi
        ↓
Tripādī
        ↓
Final Form

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


class SubstitutionStage(
    PaninianDerivationStage,
):
    """
    Executes Paninian Ādeśa (substitution) rules.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Substitution"

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Applies Paninian substitution "
            "(Ādeśa) rules."
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
    # Internal Rule Engine
    # ---------------------------------------------------------

    def _apply_substitutions(
        self,
        form: str,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> tuple[str, list[dict[str, str]], list[str]]:
        """
        Executes Paninian substitution rules.

        Returns
        -------
        (
            transformed_form,
            substitutions,
            applied_rules,
        )

        substitutions example

        [
            {
                "from": "...",
                "to": "...",
            }
        ]

        Current implementation performs no substitutions.
        """

        substitutions: list[dict[str, str]] = []
        applied_rules: list[str] = []

        #
        # Future implementation
        #
        # for rule in substitution_rule_set:
        #
        #     if rule.matches(...):
        #
        #         form = rule.apply(...)
        #
        #         substitutions.append(...)
        #
        #         applied_rules.append(...)
        #

        return (
            form,
            substitutions,
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
            substitutions,
            rules,
        ) = self._apply_substitutions(
            current,
            context,
            state,
        )

        metadata = dict(
            state.metadata,
        )

        metadata["substitution_processed"] = True
        metadata["substitution_changed"] = (
            transformed != current
        )
        metadata["substitution_count"] = len(
            substitutions,
        )
        metadata["substitutions"] = tuple(
            tuple(item.items())
            for item in substitutions
        )
        metadata["substitution_rules"] = tuple(
            rules,
        )

        updated = replace(
            state,
            metadata=metadata,
        )

        updated = updated.add_rule(
            self.display_name,
        )

        for rule in rules:
            updated = updated.add_rule(
                rule,
            )

        return updated.with_form(
            transformed,
            stage_name=self.display_name,
        )
