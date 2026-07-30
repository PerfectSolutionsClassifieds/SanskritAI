from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Engine Context

This object is passed from every Paninian derivation stage
into the Paninian Rule Engine.

It bundles together everything a PaninianRule may need while
remaining completely independent of any particular stage.

The rule engine therefore becomes reusable by

    • Dhātu Selection
    • Pratyaya Selection
    • It-Saṃjñā
    • Aṅga Processing
    • Guṇa
    • Vṛddhi
    • Āgama
    • Lopa
    • Ādeśa
    • Sandhi
    • Tripādī

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)
from SanskritAI.domain.panini.paninian_derivation_state import (
    PaninianDerivationState,
)


@dataclass(slots=True)
class PaninianRuleEngineContext(Displayable):
    """
    Immutable execution context supplied to the
    Paninian Rule Engine.
    """

    derivation_context: PaninianDerivationContext

    derivation_state: PaninianDerivationState

    stage_name: str

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Paninian Rule Engine Context"

    @property
    def display_description(self) -> str:
        return (
            "Execution context supplied to the "
            "Paninian Rule Engine."
        )

    # ---------------------------------------------------------

    @property
    def current_form(self) -> str:
        return self.derivation_state.current_form

    @property
    def metadata(self):
        return self.derivation_state.metadata

    @property
    def stage(self) -> str:
        return self.stage_name

    def __str__(self) -> str:
        return (
            f"{self.stage_name}: "
            f"{self.current_form}"
        )
