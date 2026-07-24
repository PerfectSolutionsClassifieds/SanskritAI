from __future__ import annotations

"""
SanskritAI
==========

Plugin Capability

Defines an immutable capability provided by a plugin.

A PluginCapability is a semantic declaration of what a plugin
contributes to the SanskritAI ecosystem.

Examples
--------

Dictionary

Corpus

Tokenizer

Morphology

Semantic Search

Architecture
------------

ValueObject
      │
      ▼
PluginCapability
      │
      ▼
PluginMetadata

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.capabilities.capability import Capability
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PluginCapability(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable plugin capability.
    """

    capability: Capability

    @property
    def identifier(self) -> str:
        """
        Returns the canonical capability identifier.
        """
        return self.capability.identifier

    @property
    def display_name(self) -> str:
        """
        Returns the human-readable capability name.
        """
        return self.capability.display_name

    @property
    def display_text(self) -> str:
        """
        Returns the canonical display representation.
        """
        return self.capability.display_text

    @property
    def display_description(self) -> str:
        """
        Returns the capability description.
        """
        return (
            f"Plugin provides "
            f"{self.capability.display_name} capability."
        )

    def __str__(self) -> str:
        return self.display_text
