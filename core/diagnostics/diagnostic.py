from __future__ import annotations

"""
SanskritAI
==========

Diagnostic

Represents a single immutable diagnostic produced by any
SanskritAI subsystem.

Diagnostics are intentionally subsystem-independent and may
originate from:

- Tokenizer
- Parser
- Validators
- Builders
- Corpus
- Lexical
- Amarakośa
- Morphological Engine
- Sandhi Engine
- Padaccheda Engine
- Importers

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from typing import Any, Mapping

from SanskritAI.core.diagnostics.diagnostic_code import DiagnosticCode
from SanskritAI.core.diagnostics.diagnostic_severity import (
    DiagnosticSeverity,
)


@dataclass(slots=True, frozen=True)
class Diagnostic:
    """
    Immutable diagnostic.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    code: DiagnosticCode

    severity: DiagnosticSeverity

    # ---------------------------------------------------------
    # Message
    # ---------------------------------------------------------

    message: str

    # ---------------------------------------------------------
    # Optional source location
    # ---------------------------------------------------------

    location: object | None = None

    # ---------------------------------------------------------
    # Optional metadata
    # ---------------------------------------------------------

    metadata: Mapping[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------
    # Convenience properties
    # ---------------------------------------------------------

    @property
    def is_error(self) -> bool:
        """
        Returns True if this diagnostic represents an error.
        """
        return self.severity.is_error

    @property
    def is_warning(self) -> bool:
        """
        Returns True if this diagnostic is a warning.
        """
        return self.severity.is_warning

    @property
    def is_information(self) -> bool:
        """
        Returns True if this diagnostic is informational.
        """
        return self.severity.is_information

    @property
    def is_fatal(self) -> bool:
        """
        Returns True if this diagnostic is fatal.
        """
        return self.severity.is_fatal

    @property
    def has_location(self) -> bool:
        """
        Returns True if source location information is present.
        """
        return self.location is not None

    @property
    def has_metadata(self) -> bool:
        """
        Returns True if metadata is attached.
        """
        return bool(self.metadata)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        text = (
            f"[{self.severity.name}] "
            f"{self.code}: {self.message}"
        )

        if self.location is not None:
            text += f" @ {self.location}"

        return text

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"code={self.code!r}, "
            f"severity={self.severity.name}, "
            f"message={self.message!r})"
        )
