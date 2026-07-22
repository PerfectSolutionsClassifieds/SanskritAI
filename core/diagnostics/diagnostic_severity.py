from __future__ import annotations

"""
SanskritAI
==========

Diagnostic Severity

Defines the severity levels used throughout the SanskritAI
Diagnostics Kernel.

Severity levels are intentionally subsystem-independent and are
shared by the tokenizer, parser, validators, builders,
morphological engine, importers, and future tooling.

Version
-------
v0.6.0
"""

from enum import Enum, auto


class DiagnosticSeverity(Enum):
    """
    Severity of a diagnostic.
    """

    # ---------------------------------------------------------
    # Informational
    # ---------------------------------------------------------

    TRACE = auto()

    INFO = auto()

    HINT = auto()

    # ---------------------------------------------------------
    # Problems
    # ---------------------------------------------------------

    WARNING = auto()

    ERROR = auto()

    FATAL = auto()

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_error(self) -> bool:
        """
        Returns True if this severity represents an error.
        """
        return self in {
            DiagnosticSeverity.ERROR,
            DiagnosticSeverity.FATAL,
        }

    @property
    def is_warning(self) -> bool:
        """
        Returns True if this severity is a warning.
        """
        return self is DiagnosticSeverity.WARNING

    @property
    def is_information(self) -> bool:
        """
        Returns True if this severity is informational.
        """
        return self in {
            DiagnosticSeverity.TRACE,
            DiagnosticSeverity.INFO,
            DiagnosticSeverity.HINT,
        }

    @property
    def is_fatal(self) -> bool:
        """
        Returns True if processing cannot continue.
        """
        return self is DiagnosticSeverity.FATAL

    @property
    def priority(self) -> int:
        """
        Numeric priority for sorting diagnostics.
        Higher values indicate greater severity.
        """
        return {
            DiagnosticSeverity.TRACE: 0,
            DiagnosticSeverity.INFO: 1,
            DiagnosticSeverity.HINT: 2,
            DiagnosticSeverity.WARNING: 3,
            DiagnosticSeverity.ERROR: 4,
            DiagnosticSeverity.FATAL: 5,
        }[self]
