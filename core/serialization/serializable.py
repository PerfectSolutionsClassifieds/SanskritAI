from __future__ import annotations

"""
SanskritAI
==========

Serializable

Defines the canonical serialization contract for immutable
objects throughout the SanskritAI architecture.

Serializable objects expose a format-independent dictionary
representation. Concrete serializers (JSON, YAML, XML,
Database, etc.) transform this representation into specific
serialization formats.

Architecture
------------

Serializable
        │
        ▼
Dictionary Representation
        │
        ▼
Serializer
        │
        ▼
JSON / YAML / XML / Database

Version
-------
v0.6.0
"""

from abc import ABC, abstractmethod
from typing import Any, Mapping


class Serializable(ABC):
    """
    Base interface for serializable objects.
    """

    @abstractmethod
    def to_dict(self) -> Mapping[str, Any]:
        """
        Return a canonical dictionary representation of the
        object.

        The returned mapping must be suitable for further
        serialization by any Serializer implementation.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(
        cls,
        data: Mapping[str, Any],
    ) -> "Serializable":
        """
        Construct an instance from a canonical dictionary
        representation.
        """
        raise NotImplementedError

    @property
    def is_serializable(self) -> bool:
        """
        Indicates that this object implements the serialization
        contract.
        """
        return True
