"""Plugin: heritage."""

from interfaces.dictionary import DictionaryInterface


class Plugin(DictionaryInterface):
    name = "heritage"

    def lookup(self, word: str) -> dict | None:
        return None
