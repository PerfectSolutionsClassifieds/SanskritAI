from __future__ import annotations

"""
SanskritAI
==========

Plugin Descriptor

Defines the immutable runtime descriptor of a plugin.

A PluginDescriptor combines plugin metadata with the concrete
implementation that can be instantiated by the PluginLoader.

Architecture
------------

PluginMetadata
        │
        ▼
PluginDescriptor
        │
        ▼
PluginLoader

Version
-------
v0.7.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.plugins.plugin_metadata import PluginMetadata
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PluginDescriptor(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable runtime descriptor of a plugin.
    """

    metadata: PluginMetadata

    implementation: type[Any] | None = None

    entry_point: str = ""

    @property
    def identifier(self) -> str:
        return self.metadata.identifier

    @property
    def display_name(self) -> str:
        return self.metadata.display_name

    @property
    def display_text(self) -> str:
        return self.metadata.display_text

    @property
    def display_description(self) -> str:
        return self.metadata.display_description

    @property
    def has_implementation(self) -> bool:
        """
        Indicates whether the plugin has a concrete implementation.
        """
        return self.implementation is not None

    @property
    def has_entry_point(self) -> bool:
        """
        Indicates whether an entry point has been specified.
        """
        return bool(self.entry_point)

    def __str__(self) -> str:
        return self.display_text
