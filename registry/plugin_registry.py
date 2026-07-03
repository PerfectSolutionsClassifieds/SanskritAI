from __future__ import annotations

from interfaces.dictionary import DictionaryInterface


class PluginRegistry:
    def __init__(self):
        self._dictionary_plugins: dict[str, DictionaryInterface] = {}

    def register_dictionary(self, plugin: DictionaryInterface) -> None:
        self._dictionary_plugins[plugin.name] = plugin

    def get_dictionary(self, name: str) -> DictionaryInterface | None:
        return self._dictionary_plugins.get(name)

    def dictionaries(self) -> list[str]:
        return sorted(self._dictionary_plugins)
