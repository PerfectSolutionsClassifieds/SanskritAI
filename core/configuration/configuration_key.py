from __future__ import annotations

"""
SanskritAI
==========

Configuration Key

Defines the canonical immutable identifier for configuration
entries.

A ConfigurationKey represents the unique hierarchical name of a
configuration option. Keys are normalized to ensure consistent
lookup across configuration sources.

Typical examples include:

- parser.strict_panini
- parser.max_recursion
- dictionary.cache.enabled
- ai.embedding.model
- database.postgres.host

Architecture
------------

ValueObject
      │
      ▼
ConfigurationKey
      │
      ▼
ConfigurationEntry

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ConfigurationKey(ValueObject, Immutable, Displayable):
    """
    Immutable hierarchical configuration key.
    """

    name: str

    def __post_init__(self) -> None:
        normalized = self.name.strip().lower()

        if not normalized:
            raise ValueError(
                "Configuration key cannot be empty."
            )

        object.__setattr__(self, "name", normalized)

    @property
    def identifier(self) -> str:
        """
        Returns the canonical identifier.
        """
        return self.name

    @property
    def segments(self) -> tuple[str, ...]:
        """
        Returns the hierarchical path segments.

        Example
        -------
        parser.strict_panini

        becomes

        ("parser", "strict_panini")
        """
        return tuple(
            segment
            for segment in self.name.split(".")
            if segment
        )

    @property
    def parent(self) -> "ConfigurationKey | None":
        """
        Returns the parent configuration key, if one exists.
        """
        if len(self.segments) <= 1:
            return None

        return ConfigurationKey(
            ".".join(self.segments[:-1])
        )

    @property
    def leaf(self) -> str:
        """
        Returns the final segment of the key.
        """
        return self.segments[-1]

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.name

    def starts_with(
        self,
        prefix: str,
    ) -> bool:
        """
        Determines whether this key belongs to the supplied
        namespace.
        """
        return self.name.startswith(prefix.strip().lower())

    def __str__(self) -> str:
        return self.name
