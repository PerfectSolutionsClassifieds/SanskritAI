"""Plugin: puranas."""

from interfaces.dictionary import DictionaryInterface


class Plugin(DictionaryInterface):
    name = "puranas"

    def lookup(self, word: str) -> dict | None:
        return None
