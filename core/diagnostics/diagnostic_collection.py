from __future__ import annotations

"""
SanskritAI
==========

Diagnostic Collection

Immutable collection of Diagnostic objects.

This class serves as the canonical container for diagnostics
produced throughout the SanskritAI architecture.

Responsibilities
----------------
- Immutable storage
- Iteration
- Filtering
- Severity summaries
- Query helpers

Presentation and rendering are handled separately by
DiagnosticReport.

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from collections.abc import Iterator

from SanskritAI.core.diagnostics.diagnostic import Diagnostic
from SanskritAI.core.diagnostics.diagnostic_severity import (
    DiagnosticSeverity,
)


@dataclass(slots=True, frozen=True)
class DiagnosticCollection:
    """
    Immutable collection of diagnostics.
    """

    diagnostics: tuple[Diagnostic, ...] = field(
        default_factory=tuple
    )

    # ---------------------------------------------------------
    # Collection Properties
    # ---------------------------------------------------------

    @property
    def size(self) -> int:
        """
        Total number of diagnostics.
        """
        return len(self.diagnostics)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if the collection contains no diagnostics.
        """
        return not self.diagnostics

    @property
    def has_errors(self) -> bool:
        """
        Returns True if any error diagnostics exist.
        """
        return any(d.is_error for d in self.diagnostics)

    @property
    def has_warnings(self) -> bool:
        """
        Returns True if any warning diagnostics exist.
        """
        return any(d.is_warning for d in self.diagnostics)

    @property
    def has_information(self) -> bool:
        """
        Returns True if informational diagnostics exist.
        """
        return any(d.is_information for d in self.diagnostics)

    @property
    def has_fatal(self) -> bool:
        """
        Returns True if a fatal diagnostic exists.
        """
        return any(d.is_fatal for d in self.diagnostics)

    # ---------------------------------------------------------
    # Counts
    # ---------------------------------------------------------

    def count(
        self,
        severity: DiagnosticSeverity,
    ) -> int:
        """
        Count diagnostics of a given severity.
        """
        return sum(
            1
            for diagnostic in self.diagnostics
            if diagnostic.severity == severity
        )

    # ---------------------------------------------------------
    # Filtering
    # ---------------------------------------------------------

    def filter(
        self,
        severity: DiagnosticSeverity,
    ) -> "DiagnosticCollection":
        """
        Return diagnostics having the specified severity.
        """
        return DiagnosticCollection(
            diagnostics=tuple(
                diagnostic
                for diagnostic in self.diagnostics
                if diagnostic.severity == severity
            )
        )

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return len(self.diagnostics)

    def __iter__(self) -> Iterator[Diagnostic]:
        return iter(self.diagnostics)

    def __getitem__(
        self,
        index: int | slice,
    ):
        if isinstance(index, slice):
            return DiagnosticCollection(
                diagnostics=self.diagnostics[index]
            )
        return self.diagnostics[index]

    def __contains__(
        self,
        diagnostic: Diagnostic,
    ) -> bool:
        return diagnostic in self.diagnostics

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"DiagnosticCollection("
            f"size={self.size}, "
            f"errors={self.has_errors}, "
            f"warnings={self.has_warnings})"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(diagnostics={self.diagnostics!r})"
        )
