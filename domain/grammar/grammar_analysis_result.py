from __future__ import annotations

"""
SanskritAI
==========

Grammar Analysis Result

Defines the immutable outcome produced by a grammar analyzer.

A GrammarAnalysisResult carries the subject that was analyzed,
the outputs produced by the grammar rule set, and summary
information such as confidence and notes.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class GrammarAnalysisResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable grammar analysis result.
    """

    subject: Any

    outputs: tuple[Any, ...] = field(default_factory=tuple)

    analyzer: str = ""

    confidence: float = 1.0

    notes: str = ""

    @property
    def display_name(self) -> str:
        return "Grammar Analysis Result"

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
    def first_output(self) -> Any | None:
        if not self.outputs:
            return None
        return self.outputs[0]

    @property
    def last_output(self) -> Any | None:
        if not self.outputs:
            return None
        return self.outputs[-1]

    @property
    def result(self) -> tuple[Any, ...]:
        """
        Canonical payload accessor for compatibility.
        """
        return self.outputs

    def __str__(self) -> str:
        return self.display_text
