"""Plugin: sanskritnlp."""

from interfaces.dictionary import DictionaryInterface


class Plugin(DictionaryInterface):
    name = "sanskritnlp"

    def lookup(self, word: str) -> dict | None:
        return None
