from __future__ import annotations

"""
SanskritAI
==========

Immutable Mixin

Defines the semantic contract for immutable objects used
throughout the SanskritAI architecture.

Unlike ValueObject, Immutable is not a domain concept.
Instead, it is a lightweight mixin indicating that an object
is intended to be immutable.

Typical users include:

- Value Objects
- Records
- DTOs
- Diagnostics
- Validation Results
- Build Results
- Serialization Results
- Tokenizer Objects

Immutability itself is normally enforced using
``@dataclass(frozen=True)`` or other immutable Python
constructs. This mixin provides common semantics and
introspection utilities.

Architecture
------------

Immutable
    ├── ValueObject
    ├── DataRecord
    ├── DTO
    ├── Diagnostic
    ├── BuildResult
    ├── ValidationResult
    └── SerializationResult

Version
-------
v0.6.0
"""

from dataclasses import fields, is_dataclass
from typing import Any


class Immutable:
    """
    Semantic base class for immutable objects.
    """

    @property
    def is_immutable(self) -> bool:
        """
        Indicates that this object follows immutable semantics.
        """
        return True

    @property
    def field_count(self) -> int:
        """
        Number of declared dataclass fields.

        Returns zero for non-dataclass subclasses.
        """
        if not is_dataclass(self):
            return 0

        return len(fields(self))

    @property
    def field_names(self) -> tuple[str, ...]:
        """
        Names of declared dataclass fields.

        Returns an empty tuple for non-dataclass subclasses.
        """
        if not is_dataclass(self):
            return ()

        return tuple(field.name for field in fields(self))

    def as_dict(self) -> dict[str, Any]:
        """
        Returns a shallow dictionary representation of the object.

        Intended for debugging and lightweight introspection.
        """
        if not is_dataclass(self):
            return {}

        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
        }

    def copy(self, **changes: Any) -> "Immutable":
        """
        Immutable objects should not be copied by mutation.

        Subclasses implemented as frozen dataclasses should
        instead use dataclasses.replace().
        """
        raise NotImplementedError(
            "Use dataclasses.replace() for frozen dataclass "
            "instances."
        )
