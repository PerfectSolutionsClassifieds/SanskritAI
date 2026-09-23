from __future__ import annotations

"""
Immutable boolean type.
"""

from dataclasses import dataclass

from SanskritAI.core.types.type import Type


@dataclass(frozen=True, slots=True)
class BooleanType(Type[bool]):
    """
    Immutable boolean wrapper.
    """

    def negate(self) -> "BooleanType":
        return BooleanType(not self.value)

    @property
    def is_true(self) -> bool:
        return self.value

    @property
    def is_false(self) -> bool:
        return not self.value
