from __future__ import annotations

"""
SanskritAI
==========

Tripādī Stage

Canonical Phase-3 stage of the Paninian Derivation Pipeline.

Purpose
-------
Executes the final ordered transformations governed by the
Tripādī (Aṣṭādhyāyī Chapters 8.2–8.4).

Unlike previous stages, the Tripādī has special execution
semantics. Later rules frequently override earlier rules,
making rule ordering particularly important.

Current implementation
----------------------
This implementation provides the orchestration framework.

Actual Tripādī rules will later be supplied by the
PaninianRuleEngine / PaninianRuleRepository.

Examples of future Tripādī rules

    • णत्व
    • षत्व
    • जश्त्व
    • चरत्व
    • परसवर्ण
    • अनुस्वार
    • विसर्ग transformations
    • Final phonological adjustments

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
Substitution
        ↓
Sandhi
        ↓
Tripādī        ← this stage
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


class TripadiStage(
    PaninianDerivationStage,
):
    """
    Executes final Tripādī transformations.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Tripādī"

    @property
    def display_description(self) -> str:
        return (
            "Executes final ordered Tripādī "
            "transformations (Aṣṭādhyāyī 8.2–8.4)."
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
    # Internal execution
    # ---------------------------------------------------------

    def _apply_tripadi(
        self,
        form: str,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> tuple[str, list[str]]:
        """
        Executes Tripādī rules.

        Returns
        -------
        (
            transformed_form,
            applied_rule_names,
        )

        Current implementation intentionally performs no
        transformations.
        """

        applied_rules: list[str] = []

        #
        # Future implementation:
        #
        # for rule in tripadi_rule_set:
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

        transformed, rules = self._apply_tripadi(
            current,
            context,
            state,
        )

        metadata = dict(state.metadata)

        metadata["tripadi_processed"] = True
        metadata["tripadi_changed"] = (
            transformed != current
        )
        metadata["tripadi_rule_count"] = len(
            rules
        )
        metadata["tripadi_rules"] = tuple(
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
            updated = updated.add_rule(rule)

        return updated.with_form(
            transformed,
            stage_name=self.display_name,
        )
