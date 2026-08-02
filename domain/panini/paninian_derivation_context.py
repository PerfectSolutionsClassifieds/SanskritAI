from __future__ import annotations

"""
SanskritAI
==========

Paninian Derivation Context

Canonical immutable derivation state used by the
Paninian Derivation Engine.

Purpose
-------

Represents ONE snapshot of a derivation.

Every executable Pāṇinian Sūtra receives one immutable
PaninianDerivationContext and produces either

    • the same context

or

    • a new context.

The context intentionally contains no execution history.
History is maintained separately by
PaninianExecutionTrace.

Architecture
------------

PaninianExecutionTrace
        │
        ▼
PaninianExecutionStep
        │
        ▼
PaninianDerivationContext

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PaninianDerivationContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable linguistic derivation state.
    """

    # ---------------------------------------------------------
    # Primary linguistic object
    # ---------------------------------------------------------

    subject: Any

    # ---------------------------------------------------------
    # Derivation metadata
    # ---------------------------------------------------------

    derivation_id: str = ""

    stage: str = ""

    description: str = ""

    iteration: int = 0

    # ---------------------------------------------------------
    # Optional execution information
    # ---------------------------------------------------------

    active_rule: str = ""

    active_sutra: str = ""

    # ---------------------------------------------------------
    # Immutable linguistic state
    # ---------------------------------------------------------

    attributes: dict[str, Any] = field(
        default_factory=dict,
    )

    tags: tuple[str, ...] = field(
        default_factory=tuple,
    )

    diagnostics: tuple[str, ...] = field(
        default_factory=tuple,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.derivation_id or "Derivation"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.description

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_active_rule(self) -> bool:
        return bool(self.active_rule)

    @property
    def has_tags(self) -> bool:
        return len(self.tags) > 0

    @property
    def tag_count(self) -> int:
        return len(self.tags)

    @property
    def has_diagnostics(self) -> bool:
        return len(self.diagnostics) > 0

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    # ---------------------------------------------------------
    # Immutable update operations
    # ---------------------------------------------------------

    def with_subject(
        self,
        subject: Any,
    ) -> "PaninianDerivationContext":
        """
        Returns a new context with a different subject.
        """
        return PaninianDerivationContext(
            subject=subject,
            derivation_id=self.derivation_id,
            stage=self.stage,
            description=self.description,
            iteration=self.iteration,
            active_rule=self.active_rule,
            active_sutra=self.active_sutra,
            attributes=self.attributes.copy(),
            tags=self.tags,
            diagnostics=self.diagnostics,
            metadata=self.metadata.copy(),
        )

    def with_rule(
        self,
        *,
        rule: str,
        sutra: str,
    ) -> "PaninianDerivationContext":
        """
        Returns a new context with the active rule updated.
        """
        return PaninianDerivationContext(
            subject=self.subject,
            derivation_id=self.derivation_id,
            stage=self.stage,
            description=self.description,
            iteration=self.iteration,
            active_rule=rule,
            active_sutra=sutra,
            attributes=self.attributes.copy(),
            tags=self.tags,
            diagnostics=self.diagnostics,
            metadata=self.metadata.copy(),
        )

    def next_iteration(
        self,
    ) -> "PaninianDerivationContext":
        """
        Advances the derivation iteration.
        """
        return PaninianDerivationContext(
            subject=self.subject,
            derivation_id=self.derivation_id,
            stage=self.stage,
            description=self.description,
            iteration=self.iteration + 1,
            active_rule=self.active_rule,
            active_sutra=self.active_sutra,
            attributes=self.attributes.copy(),
            tags=self.tags,
            diagnostics=self.diagnostics,
            metadata=self.metadata.copy(),
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict[str, Any]:
        """
        Returns a structured summary of the derivation state.
        """
        return {
            "derivation_id": self.derivation_id,
            "stage": self.stage,
            "iteration": self.iteration,
            "active_rule": self.active_rule,
            "active_sutra": self.active_sutra,
            "tag_count": self.tag_count,
            "diagnostic_count": self.diagnostic_count,
        }

    def __str__(self) -> str:
        return (
            f"PaninianDerivationContext("
            f"id='{self.derivation_id}', "
            f"iteration={self.iteration}, "
            f"rule='{self.active_rule}')"
        )
