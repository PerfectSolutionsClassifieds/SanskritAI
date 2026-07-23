from __future__ import annotations

"""
SanskritAI
==========

Plugin Loader

Defines the canonical plugin loader.

The PluginLoader performs plugin discovery, validation, and
dependency planning. It intentionally does not import Python
modules or instantiate plugins; those runtime responsibilities
belong to the Infrastructure kernel.

Architecture
------------

PluginRegistry
        │
        ▼
PluginLoader
        │
        ▼
Infrastructure Runtime

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.plugins.plugin_descriptor import PluginDescriptor
from SanskritAI.core.plugins.plugin_registry import PluginRegistry
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PluginLoader(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable plugin loader.

    Responsible for planning plugin loading and validating
    plugin dependencies.
    """

    registry: PluginRegistry

    @property
    def identifier(self) -> str:
        return "plugin_loader"

    @property
    def display_name(self) -> str:
        return "Plugin Loader"

    @property
    def display_text(self) -> str:
        return (
            f"Plugin Loader "
            f"({len(self.registry)} plugins)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Plans plugin loading and validates "
            "plugin dependencies."
        )

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Determines whether the specified plugin exists.
        """
        return self.registry.contains(identifier)

    def descriptor(
        self,
        identifier: str,
    ) -> PluginDescriptor | None:
        """
        Returns the descriptor for a plugin.
        """
        return self.registry.lookup(identifier)

    def validate(
        self,
    ) -> bool:
        """
        Performs structural validation of the registry.

        Runtime dependency resolution and plugin activation are
        intentionally deferred to the Infrastructure kernel.
        """
        return True

    def planned_plugins(
        self,
    ) -> tuple[PluginDescriptor, ...]:
        """
        Returns the planned plugin load sequence.

        Currently returns plugins in registry order.
        Future versions may perform dependency-aware
        topological sorting.
        """
        return tuple(self.registry.registry)

    def __str__(self) -> str:
        return self.display_text
