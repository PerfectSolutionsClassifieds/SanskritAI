from __future__ import annotations

"""
SanskritAI
==========

Serialization Result

Represents the canonical outcome of a serialization operation.

A SerializationResult encapsulates the serialized data together
with format information, status, diagnostics and optional
metadata.

This object is intentionally format-independent and may
represent JSON, XML, YAML, BSON, dictionaries, or any future
serialization format.

Architecture
------------

Serializable
        │
        ▼
Serializer
        │
        ▼
SerializationResult

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from typing import Any, Mapping

from SanskritAI.core.diagnostics.diagnostic_collection import (
    DiagnosticCollection,
)
from SanskritAI.core.serialization.serialization_format import (
    SerializationFormat,
)


@dataclass(slots=True, frozen=True)
class SerializationResult:
    """
    Immutable result of a serialization operation.
    """

    # ---------------------------------------------------------
    # Serialized representation
    # ---------------------------------------------------------

    data: Any

    format: SerializationFormat

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    success: bool = True

    message: str = ""

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    diagnostics: DiagnosticCollection = field(
        default_factory=DiagnosticCollection
    )

    # ---------------------------------------------------------
    # Optional metadata
    # ---------------------------------------------------------

    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def has_data(self) -> bool:
        """
        Returns True if serialized data is available.
        """
        return self.data is not None

    @property
    def has_diagnostics(self) -> bool:
        """
        Returns True if diagnostics are present.
        """
        return not self.diagnostics.is_empty

    @property
    def is_successful(self) -> bool:
        """
        Overall serialization status.
        """
        return (
            self.success
            and not self.diagnostics.has_errors
            and not self.diagnostics.has_fatal
        )

    @property
    def is_empty(self) -> bool:
        """
        Returns True if no serialized representation exists.
        """
        return self.data is None

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __bool__(self) -> bool:
        return self.is_successful

    def __str__(self) -> str:
        return (
            "SerializationResult("
            f"success={self.is_successful}, "
            f"format={self.format.name})"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"format={self.format.name!r}, "
            f"success={self.success!r})"
        )
