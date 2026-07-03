"""
SanskritAI
Samasa Analysis Model

Represents one grammatical analysis of a Sanskrit compound.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from models.base import BaseModel
from models.enums.samasa import Samasa
from models.word import Word
from models.sentence import Sentence


@dataclass
class SamasaAnalysis(BaseModel):
    """
    Represents one Samasa analysis.
    """

    # ---------------------------------------------------------
    # Compound
    # ---------------------------------------------------------

    compound: Optional[Word] = None

    # ---------------------------------------------------------
    # Members
    # ---------------------------------------------------------

    members: list[Word] = field(default_factory=list)

    # ---------------------------------------------------------
    # Vigraha
    # ---------------------------------------------------------

    vigraha: Optional[Sentence] = None

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    samasa: Samasa = Samasa.UNKNOWN

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

    alternatives: list["SamasaAnalysis"] = field(default_factory=list)

    notes: str = ""

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def add_member(self, word: Word) -> None:
        """
        Add one member of the compound.
        """
        self.members.append(word)
        self.touch()

    # ---------------------------------------------------------

    def add_alternative(self, analysis: "SamasaAnalysis") -> None:
        """
        Store another possible Samasa interpretation.
        """
        self.alternatives.append(analysis)
        self.touch()

    # ---------------------------------------------------------

    @property
    def compound_text(self) -> str:
        if self.compound:
            return self.compound.original_text
        return ""

    # ---------------------------------------------------------

    def summary(self) -> str:
        return (
            f"{self.compound_text} "
            f"({self.samasa.value})"
        )
