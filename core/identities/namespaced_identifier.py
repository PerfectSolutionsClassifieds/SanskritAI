from __future__ import annotations

"""
SanskritAI
==========

Namespaced Identifier

Defines a reusable identifier consisting of a namespace and a
hierarchical local identifier.

Examples
--------
LEX:राम

AMARA:SVARGA:001:012

CORPUS:RIGVEDA:001:001:003

A NamespacedIdentifier is implemented as a specialized
HierarchicalIdentifier whose first hierarchy component is the
namespace.

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.identities.hierarchical_identifier import (
    HierarchicalIdentifier,
)


@dataclass(slots=True, frozen=True)
class NamespacedIdentifier(HierarchicalIdentifier):
    """
    Immutable namespaced identifier.
    """

    namespace: str = ""

    local_parts: tuple[str, ...] = field(default_factory=tuple)

    namespace_separator: str = ":"

    def __post_init__(self) -> None:
        """
        Build the hierarchy from namespace and local parts, or
        parse an existing identifier value.
        """

        # -----------------------------------------------------
        # Construct from namespace + local_parts
        # -----------------------------------------------------

        if self.namespace:

            namespace = self.namespace.strip().upper()

            if not namespace:
                raise ValueError(
                    "Namespace cannot be empty."
                )

            if not self.local_parts:
                raise ValueError(
                    "NamespacedIdentifier requires at least one local component."
                )

            hierarchy = (namespace,) + tuple(
                part.strip()
                for part in self.local_parts
                if part.strip()
            )

            object.__setattr__(self, "parts", hierarchy)
            object.__setattr__(
                self,
                "separator",
                self.namespace_separator,
            )

            super().__post_init__()

            return

        # -----------------------------------------------------
        # Parse from existing identifier value
        # -----------------------------------------------------

        super().__post_init__()

        if self.depth < 2:
            raise ValueError(
                "NamespacedIdentifier requires both namespace "
                "and local identifier."
            )

        object.__setattr__(
            self,
            "namespace",
            self.parts[0],
        )

        object.__setattr__(
            self,
            "local_parts",
            self.parts[1:],
        )

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def local_identifier(self) -> str:
        """
        Returns the local identifier portion.
        """
        return self.namespace_separator.join(
            self.local_parts
        )

    @property
    def has_multiple_levels(self) -> bool:
        """
        Returns True if the local identifier itself is
        hierarchical.
        """
        return len(self.local_parts) > 1

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def with_local(
        self,
        *components: str,
    ) -> "NamespacedIdentifier":
        """
        Return a new identifier with a different local hierarchy.
        """
        return NamespacedIdentifier(
            value="",
            namespace=self.namespace,
            local_parts=tuple(components),
            namespace_separator=self.namespace_separator,
        )

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return (
            self.namespace
            + self.namespace_separator
            + self.local_identifier
        )
