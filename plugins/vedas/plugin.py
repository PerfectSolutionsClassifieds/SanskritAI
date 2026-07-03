"""Plugin: vedas."""

from interfaces.dictionary import DictionaryInterface


class Plugin(DictionaryInterface):
    name = "vedas"

    def lookup(self, word: str) -> dict | None:
        return None
