"""Plugin: dhatupatha."""

from interfaces.dictionary import DictionaryInterface


class Plugin(DictionaryInterface):
    name = "dhatupatha"

    def lookup(self, word: str) -> dict | None:
        return None
