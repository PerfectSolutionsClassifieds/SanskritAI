from __future__ import annotations

from analysis.morphology import MorphologyAnalyzer
from lexicon.dictionary import Dictionary
from models.word import Word


class GrammarService:
    def __init__(self, dictionary: Dictionary | None = None):
        self.morphology = MorphologyAnalyzer(dictionary=dictionary)

    def analyze_tokens(self, tokens: list[str]) -> list[Word]:
        return self.morphology.analyze(tokens)
