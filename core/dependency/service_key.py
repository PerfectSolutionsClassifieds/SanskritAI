from __future__ import annotations

"""
SanskritAI
==========

Service Key

Defines the canonical immutable identifier for a concrete service
registration.

A ServiceKey combines a semantic ServiceType with a unique service
name, providing namespaced identities for dependency injection.

Examples
--------

ServiceKey(
    service_type=ServiceType.PARSER,
    name="paninian"
)

ServiceKey(
    service_type=ServiceType.DICTIONARY,
    name="amarakosha"
)

Architecture
------------

ValueObject
      │
      ▼
ServiceKey
      │
      ├── ServiceType
      └── name

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.dependency.service_type import ServiceType
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ServiceKey(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable identifier of a concrete service.
    """

    service_type: ServiceType

    name: str

    def __post_init__(self) -> None:
        normalized = self.name.strip().lower()

        if not normalized:
            raise ValueError(
                "Service name cannot be empty."
            )

        object.__setattr__(self, "name", normalized)

    @property
    def identifier(self) -> str:
        """
        Returns the fully-qualified service identifier.
        """
        return f"{self.service_type.identifier}:{self.name}"

    @property
    def display_name(self) -> str:
        """
        Returns the service name.
        """
        return self.name.replace("_", " ").title()

    @property
    def display_text(self) -> str:
        """
        Returns the canonical display representation.
        """
        return (
            f"{self.service_type.display_name}"
            f" :: {self.display_name}"
        )

    @property
    def display_description(self) -> str:
        """
        Returns a human-readable description.
        """
        return (
            f"{self.service_type.display_name} "
            f"service '{self.display_name}'."
        )

    def matches(
        self,
        service_type: ServiceType,
        name: str,
    ) -> bool:
        """
        Determines whether this key matches the supplied
        service type and name.
        """
        return (
            self.service_type == service_type
            and self.name == name.strip().lower()
        )

    def __str__(self) -> str:
        return self.identifier
