from __future__ import annotations

"""
SanskritAI
==========

Plugin Dependency

Defines an immutable dependency on another plugin.

A PluginDependency specifies:

- the required plugin
- the acceptable version constraint
- whether the dependency is optional

Architecture
------------

ValueObject
      │
      ▼
PluginDependency
      │
      ├── PluginId
      └── VersionConstraint

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.plugins.plugin_id import PluginId
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.core.version.version_constraint import VersionConstraint


@dataclass(frozen=True, slots=True)
class PluginDependency(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable plugin dependency.
    """

    plugin: PluginId

    constraint: VersionConstraint

    optional: bool = False

    @property
    def identifier(self) -> str:
        """
        Returns the canonical dependency identifier.
        """
        return (
            f"{self.plugin.identifier}"
            f" {self.constraint.identifier}"
        )

    @property
    def display_name(self) -> str:
        """
        Returns the dependency name.
        """
        return self.plugin.display_name

    @property
    def display_text(self) -> str:
        """
        Returns the canonical display representation.
        """
        qualifier = "optional" if self.optional else "required"

        return (
            f"{self.plugin.display_name} "
            f"{self.constraint.display_text} "
            f"({qualifier})"
        )

    @property
    def display_description(self) -> str:
        """
        Returns a human-readable description.
        """
        qualifier = "Optional" if self.optional else "Required"

        return (
            f"{qualifier} dependency on "
            f"{self.plugin.display_name} "
            f"matching "
            f"{self.constraint.display_text}."
        )

    def is_required(self) -> bool:
        """
        Returns True if the dependency is required.
        """
        return not self.optional

    def __str__(self) -> str:
        return self.display_text
