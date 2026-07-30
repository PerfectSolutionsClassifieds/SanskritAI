from __future__ import annotations

"""
SanskritAI
==========

Derivation Output Collection

Immutable collection of DerivationOutput objects.

This mirrors the collection pattern used throughout the other
kernels and gives the Morphological Derivation Kernel a stable
container for actual generated outputs.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.derivation.derivation_output import DerivationOutput


@dataclass(frozen=True, slots=True)
class DerivationOutputCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable ordered collection of derivation outputs.
    """

    outputs: tuple[DerivationOutput, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Derivation Outputs"

    @property
    def display_text(self) -> str:
        return f"{len(self.outputs)} outputs"

    @property
    def display_description(self) -> str:
        return "Immutable collection of derivation outputs."

    @property
    def count(self) -> int:
        return len(self.outputs)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(self) -> DerivationOutput | None:
        if self.is_empty:
            return None
        return self.outputs[0]

    @property
    def last(self) -> DerivationOutput | None:
        if self.is_empty:
            return None
        return self.outputs[-1]

    def add(
        self,
        output: DerivationOutput,
    ) -> "DerivationOutputCollection":
        return DerivationOutputCollection(
            outputs=self.outputs + (output,),
        )

    def extend(
        self,
        other: "DerivationOutputCollection",
    ) -> "DerivationOutputCollection":
        return DerivationOutputCollection(
            outputs=self.outputs + other.outputs,
        )

    def __iter__(self) -> Iterator[DerivationOutput]:
        return iter(self.outputs)

    def __len__(self) -> int:
        return len(self.outputs)

    def __getitem__(self, index: int) -> DerivationOutput:
        return self.outputs[index]

    def __str__(self) -> str:
        return self.display_text
