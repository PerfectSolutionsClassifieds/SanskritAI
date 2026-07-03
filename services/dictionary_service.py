from __future__ import annotations

from lexicon.dictionary import Dictionary
from registry.plugin_registry import PluginRegistry


class DictionaryService:
    def __init__(
        self,
        dictionary: Dictionary | None = None,
        registry: PluginRegistry | None = None,
    ):
        self.dictionary = dictionary
        self.registry = registry or PluginRegistry()

    def lookup(self, word: str, plugin_name: str | None = None) -> dict | None:
        if plugin_name:
            plugin = self.registry.get_dictionary(plugin_name)
            return plugin.lookup(word) if plugin else None
        return self.dictionary.lookup(word) if self.dictionary else None
