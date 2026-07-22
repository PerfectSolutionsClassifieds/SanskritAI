from __future__ import annotations

"""
SanskritAI
==========

UUID Identifier

Provides a universally unique, immutable identifier for
persistent objects.

Unlike a plain UUID, a UUIDIdentifier is namespaced so that
identities remain self-describing throughout the SanskritAI
architecture.

Examples
--------
LEX:550e8400-e29b-41d4-a716-446655440000

AMARA:550e8400-e29b-41d4-a716-446655440000

CORPUS:550e8400-e29b-41d4-a716-446655440000

Version
-------
v0.6.0
"""

import uuid
from dataclasses import dataclass

from SanskritAI.core.identities.namespaced_identifier import (
    NamespacedIdentifier,
)


@dataclass(slots=True, frozen=True)
class UUIDIdentifier(NamespacedIdentifier):
    """
    Immutable UUID-based identifier.
    """

    def __post_init__(self) -> None:
        """
        Validate the UUID component.
        """
        super().__post_init__()

        if len(self.local_parts) != 1:
            raise ValueError(
                "UUIDIdentifier must contain exactly one UUID."
            )

        try:
            uuid.UUID(self.local_parts[0])

        except ValueError as exc:
            raise ValueError(
                f"Invalid UUID: {self.local_parts[0]!r}"
            ) from exc

    # ---------------------------------------------------------
    # UUID Convenience
    # ---------------------------------------------------------

    @property
    def uuid(self) -> uuid.UUID:
        """
        Returns the UUID object.
        """
        return uuid.UUID(self.local_parts[0])

    @property
    def hex(self) -> str:
        """
        Returns the hexadecimal UUID.
        """
        return self.uuid.hex

    @property
    def version(self) -> int:
        """
        UUID version.
        """
        return self.uuid.version

    # ---------------------------------------------------------
    # Factory Methods
    # ---------------------------------------------------------

    @classmethod
    def generate(
        cls,
        namespace: str,
    ) -> "UUIDIdentifier":
        """
        Generate a new random UUID identifier.
        """
        return cls(
            value="",
            namespace=namespace,
            local_parts=(str(uuid.uuid4()),),
        )

    @classmethod
    def from_uuid(
        cls,
        namespace: str,
        value: uuid.UUID,
    ) -> "UUIDIdentifier":
        """
        Construct from an existing UUID.
        """
        return cls(
            value="",
            namespace=namespace,
            local_parts=(str(value),),
        )

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"{self.namespace}"
            f"{self.namespace_separator}"
            f"{self.local_parts[0]}"
        )
