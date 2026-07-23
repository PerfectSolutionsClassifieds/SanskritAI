from __future__ import annotations

"""
SanskritAI
==========

Plugin Descriptor

Combines immutable plugin metadata with its deployment manifest.

Architecture
------------

PluginMetadata
        │
        ▼
PluginManifest
        │
        ▼
PluginDescriptor

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.plugins.plugin_manifest import PluginManifest
from SanskritAI.core.plugins.plugin_metadata import PluginMetadata
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PluginDescriptor(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable plugin descriptor.
    """

    metadata: PluginMetadata

    manifest: PluginManifest

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

    def __str__(self) -> str:
        return self.display_text
