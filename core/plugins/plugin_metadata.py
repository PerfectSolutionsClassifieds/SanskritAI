from __future__ import annotations

"""
SanskritAI
==========

Plugin Metadata

Defines the immutable descriptive metadata of a plugin.

Architecture
------------

PluginMetadata
      │
      ├── PluginId
      ├── Version
      ├── frozenset[PluginDependency]
      ├── CapabilitySet
      └── PluginState

Version
-------
v0.7.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.capabilities.capability_set import CapabilitySet
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.plugins.plugin_dependency import PluginDependency
from SanskritAI.core.plugins.plugin_id import PluginId
from SanskritAI.core.plugins.plugin_state import PluginState
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.core.version.version import Version


@dataclass(frozen=True, slots=True)
class PluginMetadata(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable metadata describing a plugin.
    """

    plugin_id: PluginId

    version: Version

    capabilities: CapabilitySet = field(
        default_factory=CapabilitySet
    )

    dependencies: frozenset[PluginDependency] = field(
        default_factory=frozenset
    )

    state: PluginState = PluginState.REGISTERED

    author: str = ""

    description: str = ""

    license: str = ""

    homepage: str = ""

    @property
    def identifier(self) -> str:
        return self.plugin_id.identifier

    @property
    def display_name(self) -> str:
        return self.plugin_id.display_name

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name} "
            f"v{self.version}"
        )

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def dependency_count(self) -> int:
        return len(self.dependencies)

    @property
    def capability_count(self) -> int:
        return len(self.capabilities)

    def __str__(self) -> str:
        return self.display_text
