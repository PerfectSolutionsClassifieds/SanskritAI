from __future__ import annotations

"""
SanskritAI
==========

Registry Entry

Defines the canonical immutable entry stored within a Registry.

A RegistryEntry associates a RegistryKey with a registered
component while carrying optional descriptive metadata.

Entries are immutable value objects and therefore compare by
value.

Typical registered components include:

- Parser
- Tokenizer
- Validator
- Builder
- Dictionary
- Corpus
- Plugin
- AI Model

Architecture
------------

Immutable
      │
      ▼
ValueObject
      │
      ▼
RegistryEntry

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from SanskritAI.core.registry.registry_key import RegistryKey
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(slots=True, frozen=True)
class RegistryEntry(ValueObject):
    """
    Immutable registry entry.
    """

    key: RegistryKey

    value: Any

    name: str = ""

    description: str = ""

    enabled: bool = True

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )

    @property
    def is_enabled(self) -> bool:
        """
        Returns True if this entry is enabled.
        """
        return self.enabled

    @property
    def has_metadata(self) -> bool:
        """
        Returns True if metadata has been supplied.
        """
        return bool(self.metadata)

    def __str__(self) -> str:
        return str(self.key)
