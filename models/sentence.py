"""
SanskritAI
Sentence Model

Represents one Sanskrit sentence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from models.base import BaseModel
from models.word import Word
from models.pipeline_state import PipelineState
from models.enums.pipeline_stage import PipelineStage


@dataclass
class Sentence(BaseModel):
    """
    Represents one Sanskrit sentence.

    A Sentence is a collection of Word objects together with
    its processing state.

    Future pipeline:

        Raw Text
            ↓
        Normalization
            ↓
        Tokenization
            ↓
        Padaccheda
            ↓
        Morphology
            ↓
        Grammar
            ↓
        Translation
    """

    original_text: str = ""
    normalized_text: str = ""

    words: List[Word] = field(default_factory=list)

    sentence_number: int = 1
    line_number: int = 1

    pipeline: PipelineState = field(default_factory=PipelineState)

    # ---------------------------------------------------------
    # Pipeline helpers
    # ---------------------------------------------------------

    def start_analysis(self):
        """Start the analysis pipeline."""
        self.pipeline.start()

    def finish_analysis(self):
        """Finish the analysis pipeline."""
        self.pipeline.finish()

    def set_stage(self, stage: PipelineStage):
        """Advance to a specific pipeline stage."""
        self.pipeline.advance(stage)

    # ---------------------------------------------------------
    # Word Management
    # ---------------------------------------------------------

    def add_original_word(self, word: Word):
        """
        Add a word exactly as found in the manuscript.
        """

        word.position = len(self.words) + 1
        word.line_number = self.line_number
        word.sentence_number = self.sentence_number

        self.words.append(word)

        if self.pipeline.current_stage.value == "created":
            self.pipeline.start()

        self.pipeline.advance(PipelineStage.TOKENIZED)

    def add_word(self, word: Word):
        """
        Alias maintained for backward compatibility.
        """
        self.add_original_word(word)

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    @property
    def word_count(self):
        return len(self.words)

    def text(self):
        return " ".join(word.original_text for word in self.words)

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    def normalize(self):
        self.pipeline.advance(PipelineStage.NORMALIZED)

    def tokenize(self):
        self.pipeline.advance(PipelineStage.TOKENIZED)

    def padaccheda_complete(self):
        self.pipeline.advance(PipelineStage.PADACCHEDA)

    def morphology_complete(self):
        self.pipeline.advance(PipelineStage.MORPHOLOGY)

    def grammar_complete(self):
        self.pipeline.advance(PipelineStage.GRAMMAR)

    def translation_complete(self):
        self.pipeline.advance(PipelineStage.TRANSLATED)

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self):

        return (
            f"Sentence("
            f"words={self.word_count}, "
            f"stage={self.pipeline.current_stage.value}, "
            f"text='{self.text()}'"
            f")"
        )

    def __str__(self):
        return self.summary()
