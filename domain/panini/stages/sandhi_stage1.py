from __future__ import annotations

"""
SanskritAI
==========

Sandhi Stage

Canonical Phase-3 stage of the Paninian Derivation Pipeline.

Purpose
-------
This stage performs the phonological completion of the
derivation by delegating Sandhi processing to the existing
SanskritAI Sandhi Kernel.

Unlike earlier derivational stages, this stage does not
contain Sandhi rules itself. Instead, it reuses the mature
Sandhi subsystem already implemented under

    SanskritAI.domain.sandhi

This keeps SanskritAI fully modular:

Paninian Pipeline
        │
        └────────► Sandhi Kernel
                        │
                        └── Vowel Sandhi
                        └── Consonant Sandhi
                        └── Visarga Sandhi
                        └── Jastva
                        └── etc.

Current implementation
----------------------

• Delegates to DefaultSandhiResolver
• Updates derivational state
• Records Sandhi diagnostics
• Preserves complete derivation trace

Future versions may additionally

• execute multiple Sandhi passes
• distinguish internal/external Sandhi
• expose Paninian Sandhi sūtras individually

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

from SanskritAI.domain.sandhi.default_sandhi_resolver import (
    DefaultSandhiResolver,
)
from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)


class SandhiStage(
    PaninianDerivationStage,
):
    """
    Executes phonological completion by delegating
    to the Sandhi Kernel.
    """

    def __init__(self) -> None:
        self._resolver = DefaultSandhiResolver()

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Sandhi"

    @property
    def display_description(self) -> str:
        return (
            "Completes phonological derivation using the "
            "Sandhi Kernel."
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

    def _execute_sandhi(
        self,
        form: str,
    ):
        """
        Delegates Sandhi processing to the Sandhi Kernel.
        """

        sandhi_context = SandhiContext(
            identifier="paninian-sandhi",
            subject=form,
        )

        #
        # Existing Sandhi kernel.
        #
        return self._resolver.resolve(
            sandhi_context,
        )

    # ---------------------------------------------------------
    # Stage execution
    # ---------------------------------------------------------

    def apply(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> PaninianDerivationState:

        current = state.current_form

        sandhi_result = self._execute_sandhi(
            current,
        )

        #
        # Obtain resulting form.
        #
        transformed = current

        if (
            sandhi_result.resolved
            and sandhi_result.candidate_count > 0
        ):
            best = sandhi_result.best_candidate

            if best is not None:

                transformed = (
                    getattr(
                        best,
                        "surface_form",
                        None,
                    )
                    or getattr(
                        best,
                        "text",
                        None,
                    )
                    or str(best)
                )

        metadata = dict(
            state.metadata,
        )

        metadata["sandhi_processed"] = True
        metadata["sandhi_changed"] = (
            transformed != current
        )
        metadata["sandhi_result"] = sandhi_result
        metadata["sandhi_resolved"] = (
            sandhi_result.resolved
        )
        metadata["sandhi_candidate_count"] = (
            sandhi_result.candidate_count
        )

        updated = replace(
            state,
            metadata=metadata,
        )

        updated = updated.add_rule(
            self.display_name,
        )

        return updated.with_form(
            transformed,
            stage_name=self.display_name,
        )
