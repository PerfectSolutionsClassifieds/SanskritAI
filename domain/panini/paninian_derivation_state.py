from __future__ import annotations

"""
SanskritAI
==========

Paninian Derivation State

Represents the evolving grammatical state during execution
of the Paninian Derivation Pipeline.

Unlike PaninianDerivationContext (which is immutable input),
this object changes after every derivational stage.

Each stage receives one state and returns a NEW state,
allowing the complete derivation history to be preserved.

Architecture

PaninianDerivationContext
            │
            ▼
Initial PaninianDerivationState
            │
            ▼
Stage 1
            │
            ▼
New State
            │
            ▼
Stage 2
            │
            ▼
New State
            │
            ▼
...
            │
            ▼
Final Surface Form

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field, replace

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PaninianDerivationState(
    Displayable,
):
    """
    Immutable derivational state.

    Each Paninian stage returns a NEW state rather than
    mutating the existing one.
    """

    context: PaninianDerivationContext

    current_form: str

    stage_name: str = "Initial"

    applied_rules: tuple[str, ...] = ()

    annotations: dict[str, object] = field(
        default_factory=dict,
    )

    confidence: float = 1.0

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Paninian Derivation State"

    @property
    def display_text(self) -> str:
        return (
            f"{self.stage_name}: "
            f"{self.current_form}"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable grammatical state produced "
            "during Paninian derivation."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def rule_count(self) -> int:
        return len(self.applied_rules)

    @property
    def latest_rule(self) -> str | None:
        if not self.applied_rules:
            return None

        return self.applied_rules[-1]

    @property
    def has_annotations(self) -> bool:
        return bool(self.annotations)

    # ---------------------------------------------------------
    # Functional updates
    # ---------------------------------------------------------

    def with_form(
        self,
        new_form: str,
        *,
        stage_name: str | None = None,
    ) -> "PaninianDerivationState":
        """
        Returns a new state with an updated surface form.
        """
        return replace(
            self,
            current_form=new_form,
            stage_name=stage_name or self.stage_name,
        )

    def add_rule(
        self,
        rule_name: str,
    ) -> "PaninianDerivationState":
        """
        Returns a new state with one additional applied rule.
        """
        return replace(
            self,
            applied_rules=(
                *self.applied_rules,
                rule_name,
            ),
        )

    def annotate(
        self,
        key: str,
        value: object,
    ) -> "PaninianDerivationState":
        """
        Returns a new state with an added annotation.
        """
        updated = dict(self.annotations)
        updated[key] = value

        return replace(
            self,
            annotations=updated,
        )

    def with_confidence(
        self,
        confidence: float,
    ) -> "PaninianDerivationState":
        """
        Returns a new state with updated confidence.
        """
        return replace(
            self,
            confidence=confidence,
        )

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    @classmethod
    def initial(
        cls,
        context: PaninianDerivationContext,
    ) -> "PaninianDerivationState":
        """
        Creates the initial derivation state from the
        supplied context.

        Initial form defaults to the dhātu root.
        """
        return cls(
            context=context,
            current_form=context.dhatu.root,
            stage_name="Initial",
        )

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
