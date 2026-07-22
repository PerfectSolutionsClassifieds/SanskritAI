from __future__ import annotations

"""
SanskritAI
==========

Serializable Contract

Defines the canonical contract for objects that can be
serialized into one or more external representations.

This contract specifies *what* an object can do, not *how*
serialization is implemented. Concrete serialization logic is
provided by the Core Serialization Kernel.

Typical implementations include:

- Corpus objects
- Dictionary entries
- Grammar models
- Registry entries
- Configuration objects

Architecture
------------

Contract
      │
      ▼
Serializable

Version
-------
v0.6.0
"""

from abc import abstractmethod

from SanskritAI.core.contracts.contract import Contract
from SanskritAI.core.serialization.serialization_format import SerializationFormat
from SanskritAI.core.serialization.serialization_result import SerializationResult


class Serializable(Contract):
    """
    Contract for serializable components.
    """

    @abstractmethod
    def serialize(
        self,
        format: SerializationFormat,
    ) -> SerializationResult:
        """
        Serializes this object into the requested format.

        Parameters
        ----------
        format:
            Desired serialization format.

        Returns
        -------
        SerializationResult
            Result of the serialization operation.
        """
        raise NotImplementedError
