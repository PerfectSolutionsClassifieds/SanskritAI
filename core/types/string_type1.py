from __future__ import annotations

"""
Immutable string type.
"""

from dataclasses import dataclass

from SanskritAI.core.types.type import Type


@dataclass(frozen=True, slots=True)
class StringType(Type[str]):
    """
    Immutable string wrapper.
    """

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError(
                "String value cannot be empty."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )

    def matches(
        self,
        value: str,
        *,
        case_sensitive: bool = False,
    ) -> bool:
        if case_sensitive:
            return self.value == value

        return self.value.casefold() == value.casefold()
