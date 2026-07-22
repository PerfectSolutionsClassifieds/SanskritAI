from __future__ import annotations

"""
SanskritAI
==========

SupportsSerialization Protocol

Defines the structural protocol for serializable components.

Unlike semantic Contracts, this protocol specifies only the
required structural interface and enables structural typing
(PEP 544).

This protocol intentionally avoids depending on concrete
serialization classes, allowing implementations to choose
their own serialization formats and result types.

Typical implementations include:

- Value Objects
- Registry Entries
- Corpus Objects
- Dictionary Entries
- Knowledge Objects
- Configuration Objects

Architecture
------------

Protocol
      │
      ▼
SupportsSerialization

Version
-------
v0.6.0
"""

from typing import Generic
from typing import TypeVar
from typing import runtime_checkable

from SanskritAI.core.protocols.protocol import Protocol

F = TypeVar("F")  # Serialization format
R = TypeVar("R")  # Serialization result


@runtime_checkable
class SupportsSerialization(Protocol, Generic[F, R]):
    """
    Structural protocol for serializable components.
    """

    def serialize(
        self,
        format: F,
    ) -> R:
        """
        Serializes this object into the requested format.
        """
        ...
