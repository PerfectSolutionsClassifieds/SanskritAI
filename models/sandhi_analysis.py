"""
SanskritAI
Sandhi Analysis Model

Represents one Sandhi analysis between two Word objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from models.base import BaseModel
from models.enums.sandhi import Sandhi
from models.word import Word


@dataclass
class SandhiAnalysis(BaseModel):
    """
    Represents one Sandhi analysis.
    """

    # ---------------------------------------------------------
    # Original Input
    # ---------------------------------------------------------

    original_text: str = ""

    # ---------------------------------------------------------
    # Word Objects
    # ---------------------------------------------------------

    left_word: Optional[Word] = None

    right_word: Optional[Word] = None

    result_word: Optional[Word] = None

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    sandhi: Sandhi = Sandhi.UNKNOWN

    # ---------------------------------------------------------
    # Grammar
    # ---------------------------------------------------------

    sutra: Optional[str] = None

    sutra_number: Optional[str] = None

    rule_description: str = ""

    # ---------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------

    confidence: float = 1.0

    ambiguous: bool = False

    alternatives: list["SandhiAnalysis"] = field(default_factory=list)

    notes: str = ""

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def add_alternative(self, analysis: "SandhiAnalysis") -> None:
        """
        Add another possible Sandhi interpretation.
        """
        self.alternatives.append(analysis)
        self.touch()

    # ---------------------------------------------------------

    @property
    def left_text(self) -> str:
        return self.left_word.original_text if self.left_word else ""

    @property
    def right_text(self) -> str:
        return self.right_word.original_text if self.right_word else ""

    @property
    def result_text(self) -> str:
        return self.result_word.original_text if self.result_word else ""

    # ---------------------------------------------------------

    def summary(self) -> str:
        return (
            f"{self.left_text} + "
            f"{self.right_text} → "
            f"{self.result_text} "
            f"({self.sandhi.value})"
        )
