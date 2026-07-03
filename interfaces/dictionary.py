from __future__ import annotations

from abc import ABC, abstractmethod


class DictionaryInterface(ABC):
    """Contract implemented by dictionary plugins such as Amarakosha or Heritage."""

    name: str

    @abstractmethod
    def lookup(self, word: str) -> dict | None:
        """Return a dictionary entry for a word, or None when unknown."""
