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

This class intentionally contains no domain-specific logic and
serves as the common base for immutable concepts such as:

- Identifier
- DiagnosticCode
- TokenPosition
- Language
- Script
- Version
- CanonicalName
- ConfidenceScore

Architecture
------------

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


class ValueObject:
    """
    Root class for immutable value objects.

    Concrete subclasses are expected to be implemented as
    frozen dataclasses.

    Example
    -------
    @dataclass(slots=True, frozen=True)
    class Language(ValueObject):
        code: str
    """

    # ---------------------------------------------------------
    # Equality
    # ---------------------------------------------------------

    def same_value_as(
        self,
        other: object,
    ) -> bool:
        """
        Returns True if two value objects are equal.
        """
        return self == other

    # ---------------------------------------------------------
    # Introspection
    # ---------------------------------------------------------

    def as_dict(self) -> dict[str, object]:
        """
        Returns the object's fields as a dictionary.

        Intended for debugging, testing, and lightweight
        introspection.
        """
        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
        }

    @property
    def field_names(self) -> tuple[str, ...]:
        """
        Returns the declared field names.
        """
        return tuple(
            field.name
            for field in fields(self)
        )

    @property
    def field_count(self) -> int:
        """
        Number of declared fields.
        """
        return len(fields(self))

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    @property
    def value(self) -> object:
        """
        Canonical value representation.

        If the value object contains exactly one field,
        that field is returned directly.

        Otherwise, a tuple containing all field values
        is returned.
        """
        values = tuple(
            getattr(self, field.name)
            for field in fields(self)
        )

        if len(values) == 1:
            return values[0]

        return values

    def __repr__(self) -> str:
        field_values = ", ".join(
            f"{field.name}={getattr(self, field.name)!r}"
            for field in fields(self)
        )

        return (
            f"{self.__class__.__name__}"
            f"({field_values})"
        )
