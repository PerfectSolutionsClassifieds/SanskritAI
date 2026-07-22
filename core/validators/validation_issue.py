from __future__ import annotations

"""
SanskritAI
==========

Validation Issue

Represents a single validation issue detected during
validation of a record or domain object.

A ValidationIssue is intentionally immutable and lightweight.

Version
-------
v0.4.0
"""

from dataclasses import dataclass
from enum import Enum


class ValidationSeverity(str, Enum):
    """
    Severity of a validation issue.
    """

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(slots=True, frozen=True)
class ValidationIssue:
    """
    Represents a single validation issue.
    """

    code: str

    message: str

    severity: ValidationSeverity = ValidationSeverity.ERROR

    field: str = ""

    location: str = ""

    suggestion: str = ""

    @property
    def is_error(self) -> bool:
        """
        Returns True if this issue is an error.
        """
        return self.severity == ValidationSeverity.ERROR

    @property
    def is_warning(self) -> bool:
        """
        Returns True if this issue is a warning.
        """
        return self.severity == ValidationSeverity.WARNING

    @property
    def is_info(self) -> bool:
        """
        Returns True if this issue is informational.
        """
        return self.severity == ValidationSeverity.INFO
