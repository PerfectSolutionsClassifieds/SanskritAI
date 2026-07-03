"""Plugin: amarakosha."""

from interfaces.dictionary import DictionaryInterface


class Plugin(DictionaryInterface):
    name = "amarakosha"

    def lookup(self, word: str) -> dict | None:
        return None
