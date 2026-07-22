from __future__ import annotations

"""
SanskritAI
==========

Serializer

Defines the canonical serialization contract used throughout
the SanskritAI architecture.

A Serializer transforms Serializable objects into a concrete
representation (dictionary, JSON, YAML, XML, database record,
etc.) and reconstructs objects from those representations.

The interface is intentionally format-independent.

Architecture
------------

Serializable
        │
        ▼
Serializer
        │
        ▼
Concrete Representation

Version
-------
v0.6.0
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from SanskritAI.core.serialization.serializable import Serializable

# ------------------------------------------------------------------
# Generic type parameters
# ------------------------------------------------------------------

S = TypeVar("S", bound=Serializable)
R = TypeVar("R")


class Serializer(ABC, Generic[S, R]):
    """
    Abstract serializer.
    """

    @abstractmethod
    def serialize(
        self,
        obj: S,
    ) -> R:
        """
        Serialize an object into a concrete representation.
        """
        raise NotImplementedError

    @abstractmethod
    def deserialize(
        self,
        data: R,
        object_type: type[S],
    ) -> S:
        """
        Deserialize a representation into an object.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    def can_serialize(
        self,
        obj: Any,
    ) -> bool:
        """
        Returns True if the supplied object implements the
        Serializable interface.
        """
        return isinstance(obj, Serializable)

    @property
    def name(self) -> str:
        """
        Human-readable serializer name.
        """
        return self.__class__.__name__
