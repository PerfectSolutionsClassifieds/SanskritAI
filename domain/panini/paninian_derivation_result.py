from __future__ import annotations

"""
SanskritAI
==========

Paninian Derivation Result

Canonical result object produced by the
Paninian Derivation Pipeline.

This class aggregates

    • immutable derivation context
    • final derivation state
    • complete derivation trace
    • diagnostics
    • success status
    • confidence

Unlike the lightweight kernel Result objects, this class
captures the complete grammatical evolution of a word
through the Paninian pipeline.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)
from SanskritAI.domain.panini.paninian_derivation_state import (
    PaninianDerivationState,
)
from SanskritAI.domain.panini.paninian_derivation_trace import (
    PaninianDerivationTrace,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PaninianDerivationResult(
    Displayable,
):
    """
    Result of the complete Paninian derivation.
    """

    context: PaninianDerivationContext

    final_state: PaninianDerivationState

    trace: PaninianDerivationTrace

    succeeded: bool = True

    confidence: float = 1.0

    diagnostics: tuple[str, ...] = field(
        default_factory=tuple,
    )

    metadata: dict[
        str,
        object,
    ] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Paninian Derivation Result"

    @property
    def display_text(
        self,
    ) -> str:
        return (
            f"{self.display_name}: "
            f"{self.surface_form}"
        )

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Complete result produced by the "
            "Paninian Derivation Pipeline."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def surface_form(
        self,
    ) -> str:
        """
        Final derived form.
        """
        return self.final_state.current_form

    @property
    def current_form(
        self,
    ) -> str:
        """
        Compatibility alias.
        """
        return self.surface_form

    @property
    def dhatu(
        self,
    ):
        return self.context.dhatu

    @property
    def pratyaya(
        self,
    ):
        return self.context.pratyaya

    @property
    def stage_count(
        self,
    ) -> int:
        return self.trace.state_count

    @property
    def has_trace(
        self,
    ) -> bool:
        return self.trace.is_not_empty

    @property
    def trace_states(
        self,
    ) -> tuple[
        PaninianDerivationState,
        ...
    ]:
        return self.trace.states

    @property
    def applied_rules(
        self,
    ) -> tuple[str, ...]:
        return self.final_state.applied_rules

    @property
    def rule_count(
        self,
    ) -> int:
        return len(
            self.applied_rules
        )

    @property
    def latest_rule(
        self,
    ) -> str | None:
        return self.final_state.latest_rule

    @property
    def has_diagnostics(
        self,
    ) -> bool:
        return bool(
            self.diagnostics
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata
        )

    # ---------------------------------------------------------
    # Lookup helpers
    # ---------------------------------------------------------

    def metadata_value(
        self,
        key: str,
        default: object | None = None,
    ) -> object | None:
        """
        Returns a metadata value.
        """
        return self.metadata.get(
            key,
            default,
        )

    def diagnostic_messages(
        self,
    ) -> tuple[str, ...]:
        """
        Returns every diagnostic.
        """
        return self.diagnostics

    # ---------------------------------------------------------
    # Compatibility aliases
    # ---------------------------------------------------------

    @property
    def resolved(
        self,
    ) -> bool:
        """
        Compatibility alias for kernel Result objects.
        """
        return self.succeeded

    @property
    def state(
        self,
    ) -> PaninianDerivationState:
        """
        Compatibility alias.
        """
        return self.final_state

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text
