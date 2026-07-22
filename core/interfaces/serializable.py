from __future__ import annotations

"""
SanskritAI
==========

Serializable Interface

Defines the contract for converting framework objects to and
from serializable representations.

The interface intentionally does not prescribe JSON, YAML,
XML, or database formats. It simply defines a canonical
dictionary representation.

Version
-------
v0.3.0
"""

from abc import ABC, abstractmethod
from typing import Any


class Serializable(ABC):
    """
    Contract for serializable objects.
    """

    # ---------------------------------------------------------

    @abstractmethod
    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Convert the object into a dictionary.
        """
        ...

    # ---------------------------------------------------------

    @classmethod
    @abstractmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "Serializable":
        """
        Construct an object from a dictionary.
        """
        ...

    # ---------------------------------------------------------

    def copy_dict(
        self,
    ) -> dict[str, Any]:
        """
        Convenience wrapper returning a shallow copy of the
        serialized representation.
        """

        return dict(self.to_dict())
