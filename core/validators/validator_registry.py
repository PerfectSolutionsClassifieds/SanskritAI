
from __future__ import annotations

"""
SanskritAI
==========

Validator Registry
------------------

Provides a typed registry for Validator instances.

The registry is deliberately generic and belongs to the core
validation layer rather than to the lexical domain.

A domain such as ``lexical`` may register its concrete validators
without changing this implementation.

Architecture
------------

Registry
    ↓
TypedRegistry
    ↓
ValidatorRegistry
    ↓
Domain-specific registrations
"""

from typing import Generic, TypeVar

from SanskritAI.core.registry.registry_key import RegistryKey
from SanskritAI.core.registry.typed_registry import TypedRegistry
from SanskritAI.core.validators.validator import Validator


TObject = TypeVar("TObject")


class ValidatorRegistry(
    TypedRegistry[RegistryKey, Validator[TObject]],
    Generic[TObject],
):
    """
    Registry containing Validator instances.

    Validators are registered under immutable RegistryKey values.
    """

    def __init__(self) -> None:
        super().__init__(Validator)

    # =========================================================
    # Convenience registration
    # =========================================================

    def register_validator(
        self,
        name: str,
        validator: Validator[TObject],
    ) -> None:
        """
        Register a validator using a string name.
        """

        self.register(
            RegistryKey(name),
            validator,
        )

    # =========================================================
    # Convenience lookup
    # =========================================================

    def get_validator(
        self,
        name: str,
    ) -> Validator[TObject] | None:
        """
        Retrieve a validator by name.
        """

        return self.get(
            RegistryKey(name)
        )

    # =========================================================
    # Capability lookup
    # =========================================================

    def supporting(
        self,
        obj: object,
    ) -> tuple[Validator[TObject], ...]:
        """
        Return all registered validators that support ``obj``.

        Registration order is preserved.
        """

        return tuple(
            validator
            for validator in self.values()
            if validator.supports(obj)
        )
