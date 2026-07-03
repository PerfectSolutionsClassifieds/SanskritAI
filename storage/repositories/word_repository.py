from __future__ import annotations

from models.word import Word


class WordRepository:
    def __init__(self):
        self._items: dict[str, Word] = {}

    def save(self, word: Word) -> None:
        self._items[word.text] = word

    def get(self, text: str) -> Word | None:
        return self._items.get(text)
