from __future__ import annotations

"""
SanskritAI
==========

Paninian Execution Trace

Immutable derivation history.

Stores an ordered sequence of
PaninianExecutionStep objects.

Purpose
-------

Supports

    • Explainable AI

    • Replay

    • Debugging

    • Mahābhāṣya reasoning

    • Backtracking

    • Derivation trees
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.panini.paninian_execution_step import (
    PaninianExecutionStep,
)


@dataclass(frozen=True, slots=True)
class PaninianExecutionTrace(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable execution history.
    """

    steps: tuple[PaninianExecutionStep, ...] = ()

    @property
    def display_name(self) -> str:
        return "Execution Trace"

    @property
    def display_text(self) -> str:
        return (
            f"{self.step_count} execution steps"
        )

    @property
    def display_description(self) -> str:
        return "Immutable derivation history"

    @property
    def step_count(self) -> int:
        return len(self.steps)

    @property
    def is_empty(self) -> bool:
        return self.step_count == 0

    @property
    def first_step(self):
        if self.is_empty:
            return None
        return self.steps[0]

    @property
    def last_step(self):
        if self.is_empty:
            return None
        return self.steps[-1]

    def append(
        self,
        step: PaninianExecutionStep,
    ) -> "PaninianExecutionTrace":
        """
        Returns a NEW trace with one additional step.
        """
        return PaninianExecutionTrace(
            steps=self.steps + (step,),
        )

    def summary(self) -> dict:
        return {
            "step_count": self.step_count,
        }

    def __len__(self):
        return self.step_count

    def __iter__(self):
        yield from self.steps

    def __getitem__(self, index):
        return self.steps[index]
