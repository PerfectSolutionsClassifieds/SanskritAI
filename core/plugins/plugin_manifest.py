from __future__ import annotations

"""
SanskritAI
==========

Plugin Manifest

Defines the immutable deployment manifest of a plugin.

A PluginManifest describes how a plugin is packaged and loaded.
Unlike PluginMetadata, it contains deployment information rather
than descriptive information.

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
from dataclasses import field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PluginManifest(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable deployment manifest.
    """

    module: str

    entry_point: str

    implementation: type | None = None

    resources: frozenset[str] = field(
        default_factory=frozenset
    )

    auto_load: bool = True

    @property
    def identifier(self) -> str:
        return self.module

    @property
    def display_name(self) -> str:
        return self.module

    @property
    def display_text(self) -> str:
        return (
            f"{self.module}:{self.entry_point}"
        )

    @property
    def display_description(self) -> str:
        return (
            "Plugin deployment manifest."
        )

    @property
    def has_implementation(self) -> bool:
        return self.implementation is not None

    def __str__(self) -> str:
        return self.display_text
