from __future__ import annotations

"""
SanskritAI
==========

Object Factory

A generic registry-driven object factory.

The ObjectFactory centralizes object creation while remaining
independent of domain-specific classes. Types register their
constructors with the factory, allowing objects to be created
without introducing hard-coded dependencies.

Typical Usage
-------------

ObjectFactory.register(Corpus, Corpus)

corpus = ObjectFactory.create(
    Corpus,
    id=...,
    metadata=...,
)

Version
-------
v0.3.0
"""

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


class ObjectFactory:
    """
    Registry-driven object factory.
    """

    _constructors: dict[type[Any], Callable[..., Any]] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    @classmethod
    def register(
        cls,
        object_type: type[T],
        constructor: Callable[..., T] | None = None,
    ) -> None:
        """
        Register a constructor for an object type.

        If no constructor is supplied, the class itself is used.
        """

        cls._constructors[object_type] = (
            constructor or object_type
        )

    # ---------------------------------------------------------

    @classmethod
    def unregister(
        cls,
        object_type: type[Any],
    ) -> None:
        """
        Remove a registered constructor.
        """

        cls._constructors.pop(object_type, None)

    # ---------------------------------------------------------

    @classmethod
    def create(
        cls,
        object_type: type[T],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """
        Create an instance of the requested type.
        """

        constructor = cls._constructors.get(
            object_type,
            object_type,
        )

        return constructor(*args, **kwargs)

    # ---------------------------------------------------------

    @classmethod
    def is_registered(
        cls,
        object_type: type[Any],
    ) -> bool:
        """
        Returns True if the type has an explicitly registered
        constructor.
        """

        return object_type in cls._constructors

    # ---------------------------------------------------------

    @classmethod
    def registered_types(
        cls,
    ) -> tuple[type[Any], ...]:
        """
        Return all registered object types.
        """

        return tuple(cls._constructors.keys())

    # ---------------------------------------------------------

    @classmethod
    def clear(
        cls,
    ) -> None:
        """
        Remove all registered constructors.
        """

        cls._constructors.clear()

    # ---------------------------------------------------------

    @classmethod
    def constructor_for(
        cls,
        object_type: type[T],
    ) -> Callable[..., T]:
        """
        Return the constructor associated with an object type.
        """

        return cls._constructors.get(
            object_type,
            object_type,
        )
