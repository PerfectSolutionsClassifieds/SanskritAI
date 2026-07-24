from __future__ import annotations

"""
SanskritAI
==========

Plugin Identifier

Defines the canonical immutable identifier of a plugin.

A PluginId uniquely identifies a plugin independently of its
implementation or version.

Examples
--------

amarakosha

vachaspatyam

sanskrit_heritage

Architecture
------------

ValueObject
      │
      ▼
PluginId
      │
      ▼
PluginMetadata

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PluginId(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable identifier of a plugin.
    """

    name: str

    def __post_init__(self) -> None:
        normalized = self.name.strip().lower()

        if not normalized:
            raise ValueError(
                "Plugin identifier cannot be empty."
            )

        object.__setattr__(
            self,
            "name",
            normalized,
        )

    @property
    def identifier(self) -> str:
        """
        Returns the canonical plugin identifier.
        """
        return self.name

    @property
    def display_name(self) -> str:
        """
        Returns the human-readable plugin name.
        """
        return self.name.replace("_", " ").title()

    @property
    def display_text(self) -> str:
        """
        Returns the canonical display representation.
        """
        return self.display_name

    @property
    def display_description(self) -> str:
        """
        Returns a human-readable description.
        """
        return (
            f"Plugin '{self.display_name}'."
        )

    def matches(
        self,
        identifier: str,
    ) -> bool:
        """
        Determines whether the supplied identifier matches
        this plugin.
        """
        return (
            self.name ==
            identifier.strip().lower()
        )

    def __str__(self) -> str:
        return self.identifier
