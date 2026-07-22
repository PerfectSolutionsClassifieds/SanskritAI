from __future__ import annotations

"""
SanskritAI
==========

Serialization Mixin

Reusable serialization support for dataclasses and simple
Python objects.

The mixin provides a generic implementation of ``to_dict()``
using dataclasses when available, with a fallback to the
instance dictionary.

Version
-------
v0.3.0
"""

from dataclasses import asdict, is_dataclass
from typing import Any


class SerializationMixin:
    """
    Provides generic dictionary serialization.
    """

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Convert the object into a dictionary.
        """

        if is_dataclass(self):
            return asdict(self)

        if hasattr(self, "__dict__"):
            return dict(self.__dict__)

        return {}

    # ---------------------------------------------------------

    def copy_dict(
        self,
    ) -> dict[str, Any]:
        """
        Return a shallow copy of the serialized representation.
        """

        return dict(self.to_dict())
