from __future__ import annotations

"""
SanskritAI
==========

Diagnostic Code

Represents a canonical identifier for a diagnostic.

Diagnostic codes are immutable value objects shared across all
SanskritAI subsystems.

Examples
--------
TOKEN0001
PARSER0015
LEX0007
AMARA0021
MORPH0104
IMPORT0003

Version
-------
v0.6.0
"""

from dataclasses import dataclass
import re


@dataclass(slots=True, frozen=True)
class DiagnosticCode:
    """
    Immutable diagnostic identifier.

    A diagnostic code consists of:

        subsystem + numeric identifier

    Examples
    --------
    TOKEN0001
    PARSER0012
    MORPH0103
    """

    value: str

    _PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*\d+$")

    def __post_init__(self) -> None:
        """
        Validate the diagnostic code format.
        """
        code = self.value.strip().upper()

        object.__setattr__(self, "value", code)

        if not code:
            raise ValueError("Diagnostic code cannot be empty.")

        if not self._PATTERN.fullmatch(code):
            raise ValueError(
                f"Invalid diagnostic code: {code!r}"
            )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def subsystem(self) -> str:
        """
        Alphabetic subsystem prefix.

        Example
        -------
        TOKEN0001 -> TOKEN
        """
        i = 0
        while i < len(self.value) and not self.value[i].isdigit():
            i += 1
        return self.value[:i]

    @property
    def number(self) -> int:
        """
        Numeric identifier.

        Example
        -------
        TOKEN0001 -> 1
        """
        i = 0
        while i < len(self.value) and not self.value[i].isdigit():
            i += 1

        return int(self.value[i:])

    @property
    def is_tokenizer(self) -> bool:
        return self.subsystem == "TOKEN"

    @property
    def is_parser(self) -> bool:
        return self.subsystem == "PARSER"

    @property
    def is_morphology(self) -> bool:
        return self.subsystem == "MORPH"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(value={self.value!r})"
        )
