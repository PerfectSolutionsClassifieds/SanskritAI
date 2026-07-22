from __future__ import annotations

"""
SanskritAI
==========

Value Object

Defines the canonical immutable value object used throughout
the SanskritAI architecture.

A Value Object is completely defined by its values rather than
its identity. Two Value Objects with identical values are
considered equal.

Unlike Entity objects, Value Objects have no independent
identity and are freely replaceable when their values are
equal.

ValueObject extends the Immutable mixin by adding value
semantics while reusing the common immutable object
introspection facilities.

Architecture
------------

Immutable
      │
      ▼
ValueObject
      │
      ├── Identifier
      ├── ComparableValue
      ├── NamedValue
      ├── CodedValue
      ├── MeasurableValue
      ├── NormalizedValue
      ├── RangedValue
      └── ScoredValue

Version
-------
v0.6.0
"""

from dataclasses import fields

from SanskritAI.core.mixins.immutable import Immutable


class ValueObject(Immutable):
    """
    Root class for immutable value objects.

    Concrete subclasses are expected to be implemented as
    frozen dataclasses.
    """

    # ---------------------------------------------------------
    # Value Semantics
    # ---------------------------------------------------------

    def same_value_as(
        self,
        other: object,
    ) -> bool:
        """
        Returns True if this value object represents the same
        value as another.
        """
        return self == other

    @property
    def value(self) -> object:
        """
        Canonical value representation.

        For single-field value objects, returns the contained
        value directly.

        For multi-field value objects, returns an immutable
        tuple of field values.
        """
        values = tuple(
            getattr(self, field.name)
            for field in fields(self)
        )

        if len(values) == 1:
            return values[0]

        return values

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        field_values = ", ".join(
            f"{field.name}={getattr(self, field.name)!r}"
            for field in fields(self)
        )

        return (
            f"{self.__class__.__name__}"
            f"({field_values})"
        )
