from __future__ import annotations

"""
SanskritAI
==========

Diagnostic Report

Canonical outcome of a diagnostics-producing operation.

A DiagnosticReport aggregates a DiagnosticCollection and
provides high-level summary information while remaining
independent of any presentation or rendering concerns.

Rendering (text, JSON, HTML, IDE, etc.) belongs to future
formatter or renderer components.

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.diagnostics.diagnostic_collection import (
    DiagnosticCollection,
)
from SanskritAI.core.diagnostics.diagnostic_severity import (
    DiagnosticSeverity,
)


@dataclass(slots=True, frozen=True)
class DiagnosticReport:
    """
    Immutable diagnostic report.
    """

    # ---------------------------------------------------------
    # Collection
    # ---------------------------------------------------------

    diagnostics: DiagnosticCollection = field(
        default_factory=DiagnosticCollection
    )

    # ---------------------------------------------------------
    # Overall status
    # ---------------------------------------------------------

    success: bool = True

    title: str = ""

    # ---------------------------------------------------------
    # Summary Properties
    # ---------------------------------------------------------

    @property
    def total(self) -> int:
        """
        Total number of diagnostics.
        """
        return len(self.diagnostics)

    @property
    def errors(self) -> int:
        """
        Number of error diagnostics.
        """
        return self.diagnostics.count(
            DiagnosticSeverity.ERROR
        )

    @property
    def warnings(self) -> int:
        """
        Number of warning diagnostics.
        """
        return self.diagnostics.count(
            DiagnosticSeverity.WARNING
        )

    @property
    def infos(self) -> int:
        """
        Number of informational diagnostics.
        """
        return (
            self.diagnostics.count(DiagnosticSeverity.INFO)
            + self.diagnostics.count(DiagnosticSeverity.HINT)
            + self.diagnostics.count(DiagnosticSeverity.TRACE)
        )

    @property
    def fatals(self) -> int:
        """
        Number of fatal diagnostics.
        """
        return self.diagnostics.count(
            DiagnosticSeverity.FATAL
        )

    @property
    def has_errors(self) -> bool:
        return self.diagnostics.has_errors

    @property
    def has_warnings(self) -> bool:
        return self.diagnostics.has_warnings

    @property
    def has_fatal(self) -> bool:
        return self.diagnostics.has_fatal

    @property
    def is_clean(self) -> bool:
        """
        Returns True if there are no diagnostics.
        """
        return self.diagnostics.is_empty

    @property
    def is_successful(self) -> bool:
        """
        Overall success state.

        A report is considered successful only if explicitly
        marked successful and it contains no fatal or error
        diagnostics.
        """
        return (
            self.success
            and not self.has_errors
            and not self.has_fatal
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def __bool__(self) -> bool:
        """
        Truthiness reflects overall success.
        """
        return self.is_successful

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return (
            "DiagnosticReport("
            f"success={self.is_successful}, "
            f"total={self.total}, "
            f"errors={self.errors}, "
            f"warnings={self.warnings}, "
            f"fatals={self.fatals})"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"diagnostics={self.diagnostics!r}, "
            f"success={self.success!r}, "
            f"title={self.title!r})"
        )
