from __future__ import annotations

"""
SanskritAI
==========

Service Lifetime

Defines the lifetime semantics of services managed by the
Dependency Injection kernel.

A ServiceLifetime determines how long a resolved service instance
remains valid.

Typical lifetimes include:

- singleton
- scoped
- transient

Unlike an enumeration, ServiceLifetime is represented as an
immutable value object so that future custom lifetimes may be
introduced without modifying the framework.

Architecture
------------

ValueObject
      │
      ▼
ServiceLifetime
      │
      ▼
ServiceDescriptor

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ServiceLifetime(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable service lifetime.
    """

    name: str

    description: str = ""

    def __post_init__(self) -> None:
        normalized = self.name.strip().lower()

        if not normalized:
            raise ValueError(
                "Service lifetime cannot be empty."
            )

        object.__setattr__(self, "name", normalized)

    @property
    def identifier(self) -> str:
        """
        Returns the canonical lifetime identifier.
        """
        return self.name

    @property
    def is_singleton(self) -> bool:
        return self.name == "singleton"

    @property
    def is_scoped(self) -> bool:
        return self.name == "scoped"

    @property
    def is_transient(self) -> bool:
        return self.name == "transient"

    @property
    def display_name(self) -> str:
        return self.name.title()

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.description

    def __str__(self) -> str:
        return self.display_name


# Canonical lifetime instances

ServiceLifetime.SINGLETON = ServiceLifetime("singleton")
ServiceLifetime.SCOPED = ServiceLifetime("scoped")
ServiceLifetime.TRANSIENT = ServiceLifetime("transient")
