from __future__ import annotations

"""
SanskritAI
==========

It-Saṃjñā Stage

Canonical third stage of the Paninian Derivation Pipeline.

Purpose
-------
Assigns the Paninian technical designation "It" (इत्-संज्ञा)
to eligible markers (अनुबन्धाः) present in the selected
Pratyaya (and later Dhātu / Āgama where applicable).

IMPORTANT

This stage DOES NOT remove It letters.

Removal (तस्य लोपः — Aṣṭādhyāyī 1.3.9) is handled later by the
Lopa Stage.

Responsibilities
----------------

• Detect candidate It markers.
• Record them in derivational metadata.
• Preserve the original derivational form.
• Leave subsequent stages responsible for actual deletion.

Current implementation
----------------------

The present implementation intentionally supports a very
small subset of Paninian behaviour so that the derivation
pipeline can evolve incrementally.

Future versions will implement:

    • उपदेशेऽजनुनासिक इत् (1.3.2)
    • हलन्त्यम् (1.3.3)
    • न विभक्तौ तुस्माः (1.3.4)
    • आदिर्ञिटुडवः
    • ञिṭ / किट् / ङिट् recognition
    • technical marker classification

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


class ItSamjnaStage(
    PaninianDerivationStage,
):
    """
    Assigns It-Saṃjñā to technical markers.

    No phonological modification occurs here.
    """

    #
    # Initial marker inventory.
    #
    # This intentionally remains conservative.
    #
    _KNOWN_IT_MARKERS = frozenset(
        {
            "ङ्",
            "ञ्",
            "ण्",
            "ट्",
            "ड्",
            "क्",
            "ग्",
            "म्",
            "स्",
        }
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "It-Saṃjñā"

    @property
    def display_description(self) -> str:
        return (
            "Recognizes Paninian It markers "
            "without deleting them."
        )

    # ---------------------------------------------------------
    # Applicability
    # ---------------------------------------------------------

    def is_applicable(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> bool:
        return context.pratyaya is not None

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _pratyaya_text(
        self,
        pratyaya,
    ) -> str:
        return (
            getattr(pratyaya, "text", None)
            or getattr(pratyaya, "surface_form", None)
            or getattr(pratyaya, "value", None)
            or getattr(pratyaya, "identifier", None)
            or str(pratyaya)
        )

    def _detect_it_markers(
        self,
        pratyaya_text: str,
    ) -> tuple[str, ...]:
        """
        Very small initial recognizer.

        Future versions will implement the
        Paninian definitions directly.
        """

        markers: list[str] = []

        for marker in self._KNOWN_IT_MARKERS:
            if marker in pratyaya_text:
                markers.append(marker)

        return tuple(sorted(markers))

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def apply(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> PaninianDerivationState:

        if context.pratyaya is None:
            return state

        pratyaya_text = self._pratyaya_text(
            context.pratyaya,
        )

        markers = self._detect_it_markers(
            pratyaya_text,
        )

        metadata = dict(state.metadata)

        metadata["it_markers"] = markers
        metadata["has_it_markers"] = bool(markers)
        metadata["it_samjna_assigned"] = True

        updated_state = replace(
            state,
            metadata=metadata,
        )

        return (
            updated_state
            .add_rule(self.display_name)
            .with_form(
                updated_state.current_form,
                stage_name=self.display_name,
            )
        )
