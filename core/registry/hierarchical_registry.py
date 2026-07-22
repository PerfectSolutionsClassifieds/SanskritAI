from __future__ import annotations

"""
SanskritAI
==========

Hierarchical Registry

Defines an ordered registry supporting parent-child
relationships between registry entries.

Hierarchy is represented using immutable RegistryNode objects
and RegistryPath value objects.

Typical usages include:

- Corpus navigation
- Amarakośa hierarchy
- Grammar hierarchy
- Knowledge taxonomy
- Plugin dependency trees

Architecture
------------

Registry
      │
      ▼
MutableRegistry
      │
      ▼
TypedRegistry
      │
      ▼
OrderedRegistry
      │
      ▼
HierarchicalRegistry

Version
-------
v0.6.0
"""

from typing import Generic, Iterator, TypeVar

from SanskritAI.core.registry.ordered_registry import OrderedRegistry
from SanskritAI.core.registry.registry_key import RegistryKey
from SanskritAI.core.registry.registry_node import RegistryNode
from SanskritAI.core.registry.registry_path import RegistryPath

K = TypeVar("K", bound=RegistryKey)
V = TypeVar("V")


class HierarchicalRegistry(OrderedRegistry[K, V], Generic[K, V]):
    """
    Registry supporting hierarchical organization.
    """

    def __init__(
        self,
        value_type: type[V],
    ) -> None:
        super().__init__(value_type)

        self._nodes: dict[K, RegistryNode] = {}

    # ---------------------------------------------------------
    # Node management
    # ---------------------------------------------------------

    def add_node(
        self,
        node: RegistryNode,
    ) -> None:
        """
        Registers a hierarchy node.
        """
        self._nodes[node.key] = node

    def get_node(
        self,
        key: K,
    ) -> RegistryNode | None:
        """
        Returns the hierarchy node for a key.
        """
        return self._nodes.get(key)

    def contains_node(
        self,
        key: K,
    ) -> bool:
        """
        Returns True if the hierarchy contains the node.
        """
        return key in self._nodes

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    def parent_of(
        self,
        key: K,
    ) -> RegistryNode | None:
        """
        Returns the parent node.
        """
        node = self.get_node(key)

        if node is None or node.parent is None:
            return None

        return self.get_node(node.parent)

    def children_of(
        self,
        key: K,
    ) -> Iterator[RegistryNode]:
        """
        Returns direct child nodes.
        """
        node = self.get_node(key)

        if node is None:
            return

        for child_key in node.children:
            child = self.get_node(child_key)

            if child is not None:
                yield child

    # ---------------------------------------------------------
    # Paths
    # ---------------------------------------------------------

    def path_of(
        self,
        key: K,
    ) -> RegistryPath | None:
        """
        Computes the path from the root to the node.
        """
        node = self.get_node(key)

        if node is None:
            return None

        components: list[RegistryKey] = []

        while node is not None:
            components.append(node.key)

            if node.parent is None:
                break

            node = self.get_node(node.parent)

        components.reverse()

        return RegistryPath(tuple(components))

    # ---------------------------------------------------------
    # Traversal
    # ---------------------------------------------------------

    def root_nodes(self) -> Iterator[RegistryNode]:
        """
        Returns all root nodes.
        """
        for node in self._nodes.values():
            if node.is_root:
                yield node

    def all_nodes(self) -> Iterator[RegistryNode]:
        """
        Returns every hierarchy node.
        """
        yield from self._nodes.values()

    @property
    def node_count(self) -> int:
        """
        Returns the number of hierarchy nodes.
        """
        return len(self._nodes)
