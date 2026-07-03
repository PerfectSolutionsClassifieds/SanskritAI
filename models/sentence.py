"""
SanskritAI
Sentence Domain Model

Represents one Sanskrit sentence.

A Sentence is an ordered collection of Word objects.
Every stage of processing is preserved so that no
information is ever lost during analysis.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from models.base import BaseModel
from models.word import Word
from models.pipeline_state import PipelineState

from models.enums.language import Language


@dataclass
class Sentence(BaseModel):
    """
    Represents one Sanskrit sentence.
    """

    # ---------------------------------------------------------
    # Original Text
    # ---------------------------------------------------------

    original_text: str = ""

    normalized_text: str = ""

    #language: str = "Sanskrit"
    language: Language = Language.SANSKRIT

    # ---------------------------------------------------------
    # Word Collections
    # ---------------------------------------------------------

    # Raw tokenizer output
    original_words: list[Word] = field(default_factory=list)

    # Output after Padaccheda
    padaccheda_words: list[Word] = field(default_factory=list)

    # Output after grammar analysis
    analyzed_words: list[Word] = field(default_factory=list)

    # Output after dictionary lookup
    lexical_words: list[Word] = field(default_factory=list)

    # ---------------------------------------------------------
    # Position
    # ---------------------------------------------------------

    sentence_number: int = 1

    line_number: int = 1

    paragraph_number: int = 1

    chapter_number: int = 1

    # ---------------------------------------------------------
    # Processing State
    # ---------------------------------------------------------

    pipeline: PipelineState = field(
        default_factory=PipelineState
    )

    # ---------------------------------------------------------
    # Original Tokens
    # ---------------------------------------------------------

    def add_original_word(self, word: Word):

        word.position = len(self.original_words) + 1
        word.sentence_number = self.sentence_number

        self.original_words.append(word)

        self.touch()

    # ---------------------------------------------------------

    def add_padaccheda_word(self, word: Word):

        word.position = len(self.padaccheda_words) + 1

        self.padaccheda_words.append(word)

        self.touch()

    # ---------------------------------------------------------

    def add_analyzed_word(self, word: Word):

        word.position = len(self.analyzed_words) + 1

        self.analyzed_words.append(word)

        self.touch()

    # ---------------------------------------------------------

    def add_lexical_word(self, word: Word):

        word.position = len(self.lexical_words) + 1

        self.lexical_words.append(word)

        self.touch()

    # ---------------------------------------------------------
    # Active Words
    # ---------------------------------------------------------

    @property
    def words(self) -> list[Word]:
        """
        Return the latest available representation.
        """

        if self.lexical_words:
            return self.lexical_words

        if self.analyzed_words:
            return self.analyzed_words

        if self.padaccheda_words:
            return self.padaccheda_words

        return self.original_words

    # ---------------------------------------------------------

    @property
    def word_count(self) -> int:

        return len(self.words)

    # ---------------------------------------------------------
    
    def add_word(self, word: Word) -> None:
        """
        Backward-compatible alias.
        Adds a word to the original word collection.
        """
        self.add_original_word(word)
    
    def get_word(self, position: int) -> Optional[Word]:

        if 0 <= position < len(self.words):
            return self.words[position]

        return None

    # ---------------------------------------------------------

    def text(self) -> str:

        return " ".join(
            word.original_text
            for word in self.words
        )

    # ---------------------------------------------------------

    def clear_analysis(self):

        self.padaccheda_words.clear()

        self.analyzed_words.clear()

        self.lexical_words.clear()

        self.pipeline = PipelineState()

        self.touch()

    # ---------------------------------------------------------

    def original_text_view(self) -> str:

        return " ".join(
            word.original_text
            for word in self.original_words
        )

    # ---------------------------------------------------------

    def padaccheda_text(self) -> str:

        return " ".join(
            word.original_text
            for word in self.padaccheda_words
        )

    # ---------------------------------------------------------

    def analyzed_text(self) -> str:

        return " ".join(
            word.original_text
            for word in self.analyzed_words
        )

    # ---------------------------------------------------------

    def lexical_text(self) -> str:

        return " ".join(
            word.original_text
            for word in self.lexical_words
        )

    # ---------------------------------------------------------

    def summary(self):

        return (
            f"Sentence("
            f"words={self.word_count}, "
            f"stage={self.pipeline.current_stage.value}, "
            f"text='{self.text()}')"
        )
