from __future__ import annotations

"""
SanskritAI
==========

Plugin Registry

Defines the immutable registry of plugin descriptors.

The PluginRegistry composes the generic HierarchicalRegistry
to provide efficient lookup of registered plugins while
remaining consistent with the Registry Kernel architecture.

Architecture
------------

HierarchicalRegistry
        │
        ▼
PluginRegistry
        │
        ▼
PluginLoader

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.plugins.plugin_descriptor import PluginDescriptor
from SanskritAI.core.registry.hierarchical_registry import (
    HierarchicalRegistry,
)
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PluginRegistry(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable registry of plugin descriptors.
    """

    registry: HierarchicalRegistry[PluginDescriptor]

    @property
    def identifier(self) -> str:
        return "plugin_registry"

    @property
    def display_name(self) -> str:
        return "Plugin Registry"

    @property
    def display_text(self) -> str:
        return (
            f"Plugin Registry "
            f"({len(self)} plugins)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Registry containing all registered plugins."
        )

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Determines whether a plugin exists.
        """
        return self.registry.contains(identifier)

    def lookup(
        self,
        identifier: str,
    ) -> PluginDescriptor | None:
        """
        Looks up a plugin by identifier.
        """
        return self.registry.lookup(identifier)

    def __len__(self) -> int:
        return len(self.registry)

    def __bool__(self) -> bool:
        return len(self) > 0

    def __str__(self) -> str:
        return self.display_text
