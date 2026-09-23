
"""
SanskritAI
Word Domain Model

Represents a single Sanskrit word or token.

This object is progressively enriched by the analysis pipeline:
    Normalizer
        ↓
    Tokenizer
        ↓
    Padaccheda
        ↓
    Morphology
        ↓
    Grammar
        ↓
    Dictionary
        ↓
    Translation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from models.base import BaseModel
from models.meaning import Meaning
from models.enums.script import Script
from models.enums.gender import Gender
from models.enums.part_of_speech import PartOfSpeech

@dataclass
class Word(BaseModel):
    """
    Represents a single Sanskrit word.

    Initially this class only stores information.
    Later analyzers populate grammatical and lexical fields.
    """

    # ---------------------------------------------------------
    # Raw Text
    # ---------------------------------------------------------

    original_text: str = ""
    normalized_text: str = ""

    # ---------------------------------------------------------
    # Script Information
    # ---------------------------------------------------------

    script: Script = Script.UNKNOWN

    # ---------------------------------------------------------
    # Position Information
    # ---------------------------------------------------------

    position: int = -1

    line_number: int = 1

    sentence_number: int = 1

    # ---------------------------------------------------------
    # Lexical Information
    # ---------------------------------------------------------

    lemma: Optional[str] = None

    stem: Optional[str] = None

    root: Optional[str] = None

    # ---------------------------------------------------------
    # Grammar (Filled Later)
    # ---------------------------------------------------------

    #gender: Optional[str] = None
    gender: Gender = Gender.UNKNOWN

    #part_of_speech: Optional[str] = None
    part_of_speech: PartOfSpeech = PartOfSpeech.UNKNOWN

    number: Optional[str] = None

    case: Optional[str] = None

    person: Optional[str] = None

    tense: Optional[str] = None

    voice: Optional[str] = None

    lakara: Optional[str] = None

    # ---------------------------------------------------------
    # Meaning
    # ---------------------------------------------------------

    # meanings: list[str] = field(default_factory=list)
    meanings: list[Meaning] = field(default_factory=list)

    # ---------------------------------------------------------
    # Dictionary Links
    # ---------------------------------------------------------

    lexeme_ids: list[str] = field(default_factory=list)

    concept_ids: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Processing Flags
    # ---------------------------------------------------------

    normalized: bool = False

    tokenized: bool = False

    analyzed: bool = False

    # ---------------------------------------------------------

    def normalize(self, text: str) -> None:
        """
        Store normalized form.
        """
        self.normalized_text = text
        self.normalized = True
        self.touch()

    # ---------------------------------------------------------

    def add_meaning(self, meaning: Meaning) -> None:
        """
        Add a dictionary meaning.
        """
        if meaning not in self.meanings:
            self.meanings.append(meaning)
            self.touch()

    # ---------------------------------------------------------

    def add_lexeme(self, lexeme_id: str) -> None:
        """
        Associate a Lexeme with this word.
        """
        if lexeme_id not in self.lexeme_ids:
            self.lexeme_ids.append(lexeme_id)
            self.touch()

    # ---------------------------------------------------------

    def add_concept(self, concept_id: str) -> None:
        """
        Associate a LexicalConcept with this word.
        """
        if concept_id not in self.concept_ids:
            self.concept_ids.append(concept_id)
            self.touch()

    # ---------------------------------------------------------

    def summary(self) -> str:
        return (
            f"Word("
            f"text='{self.original_text}', "
            f"lemma='{self.lemma}', "
            f"script='{self.script.value}')"
        )
