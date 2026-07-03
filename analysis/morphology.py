from __future__ import annotations

from core.constants import SANSKRIT_PUNCTUATION
from lexicon.dictionary import Dictionary
from models.word import Word


class MorphologyAnalyzer:
    def __init__(self, dictionary: Dictionary | None = None):
        self.dictionary = dictionary

    def analyze_token(self, token: str) -> Word:
        if token in SANSKRIT_PUNCTUATION:
            return Word(text=token, pos="punctuation")

        entry = self.dictionary.lookup(token) if self.dictionary else None
        if not entry:
            return Word(text=token, lemma=token, features={"status": "unknown"})

        return Word(
            text=token,
            lemma=entry.get("lemma", token),
            meaning=entry.get("meaning"),
            pos=entry.get("pos"),
            features=entry.get("features", {}),
        )

    def analyze(self, tokens: list[str]) -> list[Word]:
        return [self.analyze_token(token) for token in tokens]
