from __future__ import annotations

"""
SanskritAI
==========

Service Scope

Defines the canonical immutable execution scope for dependency
resolution.

A ServiceScope represents the logical boundary within which
services are resolved. It does not itself own or cache service
instances; lifetime management is the responsibility of the
ServiceContainer.

Typical scopes include:

- application
- request
- pipeline
- notebook
- worker
- test

Architecture
------------

ValueObject
      │
      ▼
ServiceScope
      │
      ▼
ServiceProvider

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ServiceScope(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable dependency injection execution scope.
    """

    name: str

    description: str = ""

    def __post_init__(self) -> None:
        normalized = self.name.strip().lower()

        if not normalized:
            raise ValueError(
                "Service scope cannot be empty."
            )

        object.__setattr__(self, "name", normalized)

    @property
    def identifier(self) -> str:
        """
        Returns the canonical scope identifier.
        """
        return self.name

    @property
    def display_name(self) -> str:
        """
        Returns the human-readable scope name.
        """
        return self.name.replace("_", " ").title()

    @property
    def display_text(self) -> str:
        """
        Returns the canonical display representation.
        """
        return self.display_name

    @property
    def display_description(self) -> str:
        """
        Returns the optional scope description.
        """
        return self.description

    def matches(
        self,
        name: str,
    ) -> bool:
        """
        Determines whether the supplied scope name matches this
        instance.
        """
        return self.name == name.strip().lower()

    def __str__(self) -> str:
        return self.display_name


# ------------------------------------------------------------------
# Canonical Scopes
# ------------------------------------------------------------------

ServiceScope.APPLICATION = ServiceScope("application")
ServiceScope.REQUEST = ServiceScope("request")
ServiceScope.PIPELINE = ServiceScope("pipeline")
ServiceScope.NOTEBOOK = ServiceScope("notebook")
ServiceScope.WORKER = ServiceScope("worker")
ServiceScope.TEST = ServiceScope("test")
