from __future__ import annotations

"""
Immutable integer type.
"""

from dataclasses import dataclass

from SanskritAI.core.types.type import Type


@dataclass(frozen=True, slots=True)
class IntegerType(Type[int]):
    """
    Immutable integer wrapper.
    """

    def increment(self) -> "IntegerType":
        return IntegerType(self.value + 1)

    def decrement(self) -> "IntegerType":
        return IntegerType(self.value - 1)
