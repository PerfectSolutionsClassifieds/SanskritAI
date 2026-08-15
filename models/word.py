
"""
SanskritAI
==========

Word Domain Model

Represents a single Sanskrit word or token.

The object is progressively enriched by the analysis pipeline:

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

Compatibility
-------------
The model retains the newer explicit ``original_text`` and
``normalized_text`` fields while also exposing the legacy/simple
``text`` and ``features`` interface.

This allows older consumers and tests to continue using:

    Word(text="धर्म")
    word.features

without removing the richer domain representation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from models.base import BaseModel
from models.meaning import Meaning
from models.enums.script import Script
from models.enums.gender import Gender
from models.enums.part_of_speech import PartOfSpeech


@dataclass
class Word(BaseModel):
    """
    Represents a single Sanskrit word.

    The object initially stores textual information and is progressively
    enriched by later analysis stages.
    """

    # ------------------------------------------------------------------
    # Compatibility / Raw Text
    # ------------------------------------------------------------------

    # ``text`` is retained as the simple public input representation.
    #
    # Existing code may construct:
    #
    #     Word(text="धर्म")
    #
    # The canonical domain fields remain ``original_text`` and
    # ``normalized_text``.
    text: str = ""

    original_text: str = ""
    normalized_text: str = ""

    # ------------------------------------------------------------------
    # Generic Features
    # ------------------------------------------------------------------

    # Compatibility container for lightweight / externally supplied
    # linguistic features.
    #
    # This intentionally remains a generic mapping at this layer.
    # Structured grammatical information continues to live in the
    # dedicated fields below.
    features: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Script Information
    # ------------------------------------------------------------------

    script: Script = Script.UNKNOWN

    # ------------------------------------------------------------------
    # Position Information
    # ------------------------------------------------------------------

    position: int = -1
    line_number: int = 1
    sentence_number: int = 1

    # ------------------------------------------------------------------
    # Lexical Information
    # ------------------------------------------------------------------

    lemma: Optional[str] = None
    stem: Optional[str] = None
    root: Optional[str] = None

    # ------------------------------------------------------------------
    # Grammar
    # ------------------------------------------------------------------

    gender: Gender = Gender.UNKNOWN
    part_of_speech: PartOfSpeech = PartOfSpeech.UNKNOWN

    number: Optional[str] = None
    case: Optional[str] = None
    person: Optional[str] = None
    tense: Optional[str] = None
    voice: Optional[str] = None
    lakara: Optional[str] = None

    # ------------------------------------------------------------------
    # Meaning
    # ------------------------------------------------------------------

    meanings: list[Meaning] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Dictionary Links
    # ------------------------------------------------------------------

    lexeme_ids: list[str] = field(default_factory=list)
    concept_ids: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Processing Flags
    # ------------------------------------------------------------------

    normalized: bool = False
    tokenized: bool = False
    analyzed: bool = False

    # ------------------------------------------------------------------
    # Initialization Compatibility
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Synchronize the compatibility ``text`` field with the canonical
        ``original_text`` field.

        ``text`` takes precedence when supplied explicitly.

        This preserves support for:

            Word(text="धर्म")

        while also supporting:

            Word(original_text="धर्म")

        The method deliberately does not normalize the text. Normalization
        remains the responsibility of ``normalize()``.
        """
        if self.text and not self.original_text:
            self.original_text = self.text
        elif self.original_text and not self.text:
            self.text = self.original_text

    # ------------------------------------------------------------------
    # Text Handling
    # ------------------------------------------------------------------

    def normalize(self, text: str) -> None:
        """
        Store the normalized form.

        The original/input text is preserved.
        """
        self.normalized_text = text
        self.normalized = True
        self.touch()

    # ------------------------------------------------------------------
    # Meaning
    # ------------------------------------------------------------------

    def add_meaning(self, meaning: Meaning) -> None:
        """
        Add a dictionary meaning if it is not already present.
        """
        if meaning not in self.meanings:
            self.meanings.append(meaning)

        self.touch()

    # ------------------------------------------------------------------
    # Lexical Associations
    # ------------------------------------------------------------------

    def add_lexeme(self, lexeme_id: str) -> None:
        """
        Associate a Lexeme with this word.
        """
        if lexeme_id not in self.lexeme_ids:
            self.lexeme_ids.append(lexeme_id)

        self.touch()

    def add_concept(self, concept_id: str) -> None:
        """
        Associate a lexical concept with this word.
        """
        if concept_id not in self.concept_ids:
            self.concept_ids.append(concept_id)

        self.touch()

    # ------------------------------------------------------------------
    # Features
    # ------------------------------------------------------------------

    def set_feature(self, name: str, value: Any) -> None:
        """
        Set or replace a generic linguistic feature.

        Generic features are intentionally kept separate from the
        strongly typed grammatical fields.
        """
        self.features[name] = value
        self.touch()

    def get_feature(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a generic linguistic feature.
        """
        return self.features.get(name, default)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(self) -> str:
        """
        Return a compact human-readable representation.
        """
        return (
            f"Word("
            f"text='{self.original_text}', "
            f"lemma='{self.lemma}', "
            f"script='{self.script.value}')"
        )
