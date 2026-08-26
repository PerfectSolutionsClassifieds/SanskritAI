from __future__ import annotations

"""
SanskritAI
==========

Sandhi Analysis

Defines the immutable outcome of one Sandhi analysis operation.

A SandhiAnalysis represents the result produced after a
Sandhi rule, strategy, resolver, or analyzer processes a
Sandhi subject.

The structure intentionally mirrors the SamasaAnalysis
architecture so that all linguistic analysis kernels expose
a consistent value-object model.

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
class SandhiAnalysis(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable Sandhi analysis result.

    Represents one analysis produced for a Sandhi subject.

    Parameters
    ----------
    identifier:
        Stable identifier for this analysis.

    subject:
        Original Sandhi subject being analyzed.

    outputs:
        Candidate Sandhi outputs produced by the analyzer.

    analyzer:
        Name or identifier of the analyzer/rule/strategy
        that produced the analysis.

    confidence:
        Confidence score associated with the analysis.

    notes:
        Optional explanatory or provenance information.
    """

    identifier: str
    subject: Any
    outputs: tuple[Any, ...] = field(
        default_factory=tuple,
    )
    analyzer: str = ""
    confidence: float = 1.0
    notes: str = ""

    @property
    def display_name(self) -> str:
        return "Sandhi Analysis"

    @property
    def display_text(self) -> str:
        return (
            f"{self.subject}"
            f" → {len(self.outputs)} outputs"
        )

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
