from __future__ import annotations

"""
SanskritAI
==========

Resource Identifier

Defines a reusable immutable identifier for persistent domain
resources.

A ResourceIdentifier represents an addressable resource within
the SanskritAI ecosystem. It provides common behavior shared by
CorpusIdentifier, LexicalIdentifier, KnowledgeIdentifier, and
future resource-based identifiers.

Architecture
------------

Identifier
    │
    ▼
HierarchicalIdentifier
    │
    ▼
NamespacedIdentifier
    │
    ▼
ResourceIdentifier
    ├── CorpusIdentifier
    ├── LexicalIdentifier
    └── KnowledgeIdentifier

Version
-------
v0.6.0
"""

from __future__ import annotations

from dataclasses import dataclass

from SanskritAI.core.identities.namespaced_identifier import (
    NamespacedIdentifier,
)


@dataclass(slots=True, frozen=True)
class ResourceIdentifier(NamespacedIdentifier):
    """
    Base class for identifiers representing persistent
    resources.
    """

    # ---------------------------------------------------------
    # Resource Information
    # ---------------------------------------------------------

    @property
    def resource_name(self) -> str:
        """
        Returns the final component of the resource hierarchy.
        """
        return self.local_parts[-1]

    @property
    def resource_path(self) -> tuple[str, ...]:
        """
        Returns the resource hierarchy excluding the namespace.
        """
        return self.local_parts

    @property
    def resource_depth(self) -> int:
        """
        Number of resource hierarchy levels.
        """
        return len(self.local_parts)

    @property
    def parent_resource(self) -> "ResourceIdentifier | None":
        """
        Returns the parent resource, or None if already at the
        root resource.
        """
        if self.resource_depth <= 1:
            return None

        return self.__class__(
            value="",
            namespace=self.namespace,
            local_parts=self.local_parts[:-1],
            namespace_separator=self.namespace_separator,
        )

    def child_resource(
        self,
        component: str,
    ) -> "ResourceIdentifier":
        """
        Creates a child resource identifier.
        """
        return self.__class__(
            value="",
            namespace=self.namespace,
            local_parts=self.local_parts + (component,),
            namespace_separator=self.namespace_separator,
        )

    # ---------------------------------------------------------
    # Matching
    # ---------------------------------------------------------

    def is_descendant_of(
        self,
        other: "ResourceIdentifier",
    ) -> bool:
        """
        Returns True if this resource is contained within the
        supplied resource hierarchy.
        """
        if self.namespace != other.namespace:
            return False

        if other.resource_depth > self.resource_depth:
            return False

        return (
            self.resource_path[: other.resource_depth]
            == other.resource_path
        )

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"namespace={self.namespace!r}, "
            f"path={self.resource_path!r})"
        )
