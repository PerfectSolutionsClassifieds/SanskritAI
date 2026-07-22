from __future__ import annotations

"""
SanskritAI
==========

Registry Node

Defines the canonical immutable node used by hierarchical
registries.

A RegistryNode represents a single node within a registry tree.
It stores structural relationships while remaining independent
of any specific registry implementation.

Typical usages include:

- Corpus trees
- Dictionary hierarchies
- Amarakośa Kāṇḍa → Varga → Synset
- Grammar trees
- Plugin dependency trees
- Knowledge hierarchies

Architecture
------------

ValueObject
      │
      ▼
RegistryNode
      │
      ▼
HierarchicalRegistry

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.registry.registry_entry import RegistryEntry
from SanskritAI.core.registry.registry_key import RegistryKey
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(slots=True, frozen=True)
class RegistryNode(ValueObject):
    """
    Immutable registry node.
    """

    key: RegistryKey

    entry: RegistryEntry | None = None

    parent: RegistryKey | None = None

    children: tuple[RegistryKey, ...] = field(default_factory=tuple)

    @property
    def is_root(self) -> bool:
        """
        Returns True if this node has no parent.
        """
        return self.parent is None

    @property
    def is_leaf(self) -> bool:
        """
        Returns True if this node has no children.
        """
        return len(self.children) == 0

    @property
    def child_count(self) -> int:
        """
        Returns the number of child nodes.
        """
        return len(self.children)

    def has_child(
        self,
        key: RegistryKey,
    ) -> bool:
        """
        Returns True if the supplied key is a direct child.
        """
        return key in self.children

    def __str__(self) -> str:
        return str(self.key)
