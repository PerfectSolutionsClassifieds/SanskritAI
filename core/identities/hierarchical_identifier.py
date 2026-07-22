from __future__ import annotations

"""
SanskritAI
==========

Hierarchical Identifier

Represents an immutable hierarchical identifier.

Unlike a simple Identifier, a HierarchicalIdentifier consists
of multiple ordered components that together define the
identity of an object.

Examples
--------
BRAHMA.001.023.005

AMARAKOSHA.SVARGA.001.012

VEDA.RIG.001.001.003

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.identities.identifier import Identifier


@dataclass(slots=True, frozen=True)
class HierarchicalIdentifier(Identifier):
    """
    Immutable hierarchical identifier.
    """

    parts: tuple[str, ...] = field(default_factory=tuple)

    separator: str = "."

    def __post_init__(self) -> None:
        """
        Normalize the hierarchy.

        If parts are supplied, the identifier value is derived
        from them. Otherwise, the supplied value is parsed into
        hierarchy parts.
        """

        if self.parts:
            normalized_parts = tuple(
                part.strip()
                for part in self.parts
                if part.strip()
            )

            if not normalized_parts:
                raise ValueError(
                    "HierarchicalIdentifier must contain at least one part."
                )

            object.__setattr__(self, "parts", normalized_parts)

            object.__setattr__(
                self,
                "value",
                self.separator.join(normalized_parts),
            )

        else:
            value = self.value.strip()

            if not value:
                raise ValueError(
                    "HierarchicalIdentifier cannot be empty."
                )

            parsed = tuple(
                part.strip()
                for part in value.split(self.separator)
                if part.strip()
            )

            if not parsed:
                raise ValueError(
                    "HierarchicalIdentifier contains no valid parts."
                )

            object.__setattr__(self, "parts", parsed)

            object.__setattr__(
                self,
                "value",
                self.separator.join(parsed),
            )

    # ---------------------------------------------------------
    # Hierarchy
    # ---------------------------------------------------------

    @property
    def depth(self) -> int:
        """
        Number of hierarchy levels.
        """
        return len(self.parts)

    @property
    def root(self) -> str:
        """
        Top-most hierarchy component.
        """
        return self.parts[0]

    @property
    def leaf(self) -> str:
        """
        Lowest hierarchy component.
        """
        return self.parts[-1]

    @property
    def parent(self) -> "HierarchicalIdentifier | None":
        """
        Parent hierarchy or None if already at the root.
        """
        if self.depth <= 1:
            return None

        return HierarchicalIdentifier(
            value="",
            parts=self.parts[:-1],
            separator=self.separator,
        )

    def child(
        self,
        component: str,
    ) -> "HierarchicalIdentifier":
        """
        Return a child identifier.
        """
        return HierarchicalIdentifier(
            value="",
            parts=self.parts + (component,),
            separator=self.separator,
        )

    def starts_with(
        self,
        other: "HierarchicalIdentifier",
    ) -> bool:
        """
        Returns True if this hierarchy begins with another.
        """
        if other.depth > self.depth:
            return False

        return self.parts[: other.depth] == other.parts

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.separator.join(self.parts)
