from __future__ import annotations

"""
SanskritAI
==========

Registry Path

Defines the canonical immutable path used by hierarchical
registries.

A RegistryPath represents the location of a RegistryNode within
a hierarchy. It is composed of an ordered sequence of
RegistryKey objects.

Typical examples include:

- BrahmaPurana / Chapter001 / Sloka001
- Amarakosha / SvargadiKanda / SvargaVarga
- Grammar / Noun / Masculine / Singular

Architecture
------------

ValueObject
      │
      ▼
RegistryPath
      │
      ▼
HierarchicalRegistry

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.registry.registry_key import RegistryKey
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(slots=True, frozen=True)
class RegistryPath(ValueObject):
    """
    Immutable registry path.
    """

    components: tuple[RegistryKey, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if any(component is None for component in self.components):
            raise ValueError(
                "RegistryPath components cannot contain None."
            )

    @property
    def is_root(self) -> bool:
        """
        Returns True if this path represents the root.
        """
        return len(self.components) == 0

    @property
    def depth(self) -> int:
        """
        Returns the number of path components.
        """
        return len(self.components)

    @property
    def parent(self) -> "RegistryPath | None":
        """
        Returns the parent path.

        Returns
        -------
        RegistryPath | None
        """
        if self.is_root:
            return None

        return RegistryPath(self.components[:-1])

    @property
    def leaf(self) -> RegistryKey | None:
        """
        Returns the final component of the path.
        """
        if self.is_root:
            return None

        return self.components[-1]

    def append(
        self,
        key: RegistryKey,
    ) -> "RegistryPath":
        """
        Returns a new path with the supplied component appended.
        """
        return RegistryPath(
            self.components + (key,)
        )

    def starts_with(
        self,
        other: "RegistryPath",
    ) -> bool:
        """
        Returns True if this path begins with another path.
        """
        if other.depth > self.depth:
            return False

        return self.components[: other.depth] == other.components

    def __iter__(self) -> Iterator[RegistryKey]:
        return iter(self.components)

    def __len__(self) -> int:
        return self.depth

    def __str__(self) -> str:
        if self.is_root:
            return "/"

        return "/" + "/".join(str(component) for component in self.components)
