from __future__ import annotations

"""
SanskritAI
==========

Comparable Value

Defines the canonical base class for immutable value objects
that possess a natural ordering.

ComparableValue extends ValueObject by introducing a single
canonical comparison value from which all ordering operations
are derived.

Typical subclasses include:

- Identifier
- RegistryKey
- Language
- Script
- CorpusIdentifier
- LexicalIdentifier
- KnowledgeIdentifier

Architecture
------------

Immutable
      │
      ▼
ValueObject
      │
      ▼
ComparableValue

Version
-------
v0.6.0
"""

from abc import abstractmethod

from SanskritAI.core.value_objects.value_object import ValueObject


class ComparableValue(ValueObject):
    """
    Base class for naturally ordered immutable value objects.
    """

    @property
    @abstractmethod
    def comparison_value(self) -> object:
        """
        Returns the canonical value used for ordering.

        Subclasses should return an immutable object that
        supports Python's comparison operators.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Ordering
    # ---------------------------------------------------------

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ComparableValue):
            return NotImplemented
        return self.comparison_value < other.comparison_value

    def __le__(self, other: object) -> bool:
        if not isinstance(other, ComparableValue):
            return NotImplemented
        return self.comparison_value <= other.comparison_value

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, ComparableValue):
            return NotImplemented
        return self.comparison_value > other.comparison_value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, ComparableValue):
            return NotImplemented
        return self.comparison_value >= other.comparison_value

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def compare_to(
        self,
        other: "ComparableValue",
    ) -> int:
        """
        Performs a three-way comparison.

        Returns
        -------
        int
            -1 if self < other
             0 if self == other
             1 if self > other
        """
        if self < other:
            return -1

        if self > other:
            return 1

        return 0
