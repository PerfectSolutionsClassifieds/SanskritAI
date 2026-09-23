from __future__ import annotations

"""
SanskritAI
==========

Lopa Stage

Canonical Phase-2 stage of the Paninian Derivation Pipeline.

Purpose
-------
Executes Paninian Lopa (elision/deletion) operations.

This is the first stage where the It-markers identified by the
It-Saṃjñā stage begin to affect the derivation.

Current implementation
----------------------

This version intentionally implements only the architectural
framework.

It performs a very conservative form of It-marker removal using
metadata produced by the It-Saṃjñā stage.

Future versions will execute hundreds of Paninian lopa rules.

Examples

    • तस्य लोपः (1.3.9)
    • लुक्
    • श्लु
    • लुप्
    • प्रत्ययलोप
    • अङ्गलोप
    • धातुलोप
    • सुप्-लोप
    • तिङ्-लोप

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
Lopa                ← this stage
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


class LopaStage(
    PaninianDerivationStage,
):
    """
    Executes Paninian Lopa operations.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Lopa"

    @property
    def display_description(self) -> str:
        return (
            "Applies Paninian Lopa (elision) rules."
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
    # Internal Engine
    # ---------------------------------------------------------

    def _apply_lopa(
        self,
        form: str,
        state: PaninianDerivationState,
    ) -> tuple[str, list[str], list[str]]:
        """
        Applies currently known Lopa operations.

        Returns
        -------
        (
            transformed_form,
            removed_elements,
            applied_rule_names,
        )
        """

        removed: list[str] = []
        rules: list[str] = []

        markers = (
            state.metadata.get(
                "it_markers",
                (),
            )
        )

        transformed = form

        #
        # Initial implementation:
        #
        # Remove previously detected It markers.
        #
        for marker in markers:

            if marker in transformed:

                transformed = transformed.replace(
                    marker,
                    "",
                )

                removed.append(marker)

                rules.append(
                    "tasya_lopah"
                )

        return (
            transformed,
            removed,
            rules,
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
            removed,
            rules,
        ) = self._apply_lopa(
            current,
            state,
        )

        metadata = dict(
            state.metadata,
        )

        metadata["lopa_processed"] = True
        metadata["lopa_changed"] = (
            transformed != current
        )
        metadata["removed_elements"] = tuple(
            removed,
        )
        metadata["lopa_count"] = len(
            removed,
        )
        metadata["lopa_rules"] = tuple(
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
