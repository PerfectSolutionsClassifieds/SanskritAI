from __future__ import annotations

"""
SanskritAI
==========

Typed Registry

Defines a mutable registry that accepts only values of a
specified type.

TypedRegistry extends MutableRegistry by enforcing runtime
type safety for all registered values.

Typical usages include:

- ParserRegistry
- TokenizerRegistry
- BuilderRegistry
- ValidatorRegistry
- DictionaryRegistry
- CorpusRegistry

Architecture
------------

Registry
      │
      ▼
MutableRegistry
      │
      ▼
TypedRegistry

Version
-------
v0.6.0
"""

from typing import Generic, TypeVar

from SanskritAI.core.registry.mutable_registry import MutableRegistry
from SanskritAI.core.registry.registry_exception import RegistryException
from SanskritAI.core.registry.registry_key import RegistryKey

K = TypeVar("K", bound=RegistryKey)
V = TypeVar("V")


class TypedRegistry(MutableRegistry[K, V], Generic[K, V]):
    """
    Registry enforcing runtime type safety.
    """

    def __init__(
        self,
        value_type: type[V],
    ) -> None:
        """
        Initializes a typed registry.

        Parameters
        ----------
        value_type:
            The only value type accepted by this registry.
        """
        super().__init__()
        self._value_type = value_type

    @property
    def value_type(self) -> type[V]:
        """
        Returns the accepted value type.
        """
        return self._value_type

    def register(
        self,
        key: K,
        value: V,
    ) -> None:
        """
        Registers a typed value.

        Raises
        ------
        RegistryException
            If the supplied value is not of the expected type.
        """
        if not isinstance(value, self._value_type):
            raise RegistryException(
                message=(
                    f"Invalid registry value type. "
                    f"Expected '{self._value_type.__name__}', "
                    f"received '{type(value).__name__}'."
                ),
                key=key,
                value=value,
            )

        super().register(key, value)

    def accepts(
        self,
        value: object,
    ) -> bool:
        """
        Returns True if the supplied value is accepted by this
        registry.
        """
        return isinstance(value, self._value_type)
