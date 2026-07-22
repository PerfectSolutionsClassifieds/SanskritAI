from __future__ import annotations

"""
SanskritAI
==========

Registry Key

Defines the canonical immutable key used by the Registry
Kernel.

A RegistryKey uniquely identifies an entry within a registry
while remaining independent of the registered value.

Registry keys are immutable value objects and therefore compare
by value rather than by identity.

Typical examples include:

- "amarakosha"
- "lexeme"
- "sandhi"
- "parser.xml"
- "validator.default"

Architecture
------------

Immutable
      │
      ▼
ValueObject
      │
      ▼
RegistryKey

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(slots=True, frozen=True)
class RegistryKey(ValueObject):
    """
    Canonical immutable registry key.
    """

    value: str

    def __post_init__(self) -> None:
        value = self.value.strip()

        if not value:
            raise ValueError(
                "Registry key cannot be empty."
            )

        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value
