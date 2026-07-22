from __future__ import annotations

"""
SanskritAI
==========

Service Factory

Defines the canonical immutable wrapper around a callable capable
of constructing a service instance.

A ServiceFactory encapsulates *how* a service is created while
remaining independent of service metadata, registration, or
lifetime management.

Architecture
------------

ValueObject
      │
      ▼
ServiceFactory
      │
      ▼
ServiceDescriptor

Version
-------
v0.7.0
"""

from dataclasses import dataclass
from typing import Any
from typing import Callable

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ServiceFactory(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable wrapper around a service factory callable.
    """

    factory: Callable[..., Any]

    description: str = ""

    def __post_init__(self) -> None:
        if not callable(self.factory):
            raise TypeError(
                "ServiceFactory requires a callable."
            )

    @property
    def identifier(self) -> str:
        """
        Returns the fully-qualified factory identifier.
        """
        module = getattr(self.factory, "__module__", "<unknown>")
        qualname = getattr(
            self.factory,
            "__qualname__",
            getattr(self.factory, "__name__", "<callable>"),
        )
        return f"{module}.{qualname}"

    @property
    def display_name(self) -> str:
        """
        Returns the callable name.
        """
        return getattr(
            self.factory,
            "__name__",
            self.factory.__class__.__name__,
        )

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        if self.description:
            return self.description

        return (
            f"Factory for service '{self.display_name}'."
        )

    def create(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Creates a service instance.
        """
        return self.factory(*args, **kwargs)

    def __call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Invokes the underlying factory.
        """
        return self.create(*args, **kwargs)

    def __str__(self) -> str:
        return self.display_name
