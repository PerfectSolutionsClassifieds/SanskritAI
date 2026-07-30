from __future__ import annotations

"""
SanskritAI
==========

Grammar Analysis

Defines the immutable outcome of a grammar-domain analysis
operation.

A GrammarAnalysis represents the result produced after a
grammar rule-set or grammar analyzer processes a subject.

It is intentionally generic so that future grammar kernels can
attach richer typed outputs without changing the overall
architecture.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class GrammarAnalysis(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable grammar analysis result.
    """

    identifier: str

    subject: Any

    outputs: tuple[Any, ...] = field(default_factory=tuple)

    analyzer: str = ""

    confidence: float = 1.0

    notes: str = ""

    @property
    def display_name(self) -> str:
        return "Grammar Analysis"

    @property
    def display_text(self) -> str:
        return f"{self.subject} → {len(self.outputs)} outputs"

    @property
    def display_description(self) -> str:
        return self.notes

    @property
    def has_outputs(self) -> bool:
        return len(self.outputs) > 0

    @property
    def output_count(self) -> int:
        return len(self.outputs)

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    @property
    def has_notes(self) -> bool:
        return bool(self.notes)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.outputs)

    def __len__(self) -> int:
        return len(self.outputs)

    def __getitem__(self, index: int) -> Any:
        return self.outputs[index]

    def __str__(self) -> str:
        return self.display_text
