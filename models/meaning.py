"""
SanskritAI
Meaning Domain Model

Represents one semantic meaning attached to a Sanskrit word.

The same Meaning object can be reused by:
    - Word
    - Lexeme
    - LexicalConcept
    - Dictionary Services
    - Amarakosha
    - Translation Engine
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from models.base import BaseModel
from models.enums.language import Language
from models.enums.dictionary_source import DictionarySource

@dataclass
class Meaning(BaseModel):
    """
    Represents one meaning of a lexical item.
    """

    # ---------------------------------------------------------
    # Meaning
    # ---------------------------------------------------------

    text: str = ""

    #language: str = "English"
    language: Language = Language.ENGLISH


    # ---------------------------------------------------------
    # Source Information
    # ---------------------------------------------------------

    #source: Optional[str] = None
    source: DictionarySource = DictionarySource.UNKNOWN

    source_reference: Optional[str] = None

    # ---------------------------------------------------------
    # Ranking
    # ---------------------------------------------------------

    priority: int = 1

    confidence: float = 1.0

    # ---------------------------------------------------------
    # Optional Notes
    # ---------------------------------------------------------

    notes: str = ""

    # ---------------------------------------------------------

    def summary(self) -> str:
        return (
            f"Meaning("
            f"text='{self.text}', "
            f"language='{self.language}', "
            f"source='{self.source}')"
        )
