from __future__ import annotations

"""
SanskritAI
==========

Samasa Diagnostic

Defines immutable diagnostics produced during Samasa
resolution.

A SamasaDiagnostic captures informational messages,
warnings, or errors generated while performing compound
analysis, splitting, or classification.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class SamasaDiagnostic(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable Samasa diagnostic.
    """

    code: str

    message: str

    severity: str = "INFO"

    rule: str = ""

    location: str = ""

    @property
    def display_name(self) -> str:
        return self.severity

    @property
    def display_text(self) -> str:
        return f"[{self.severity}] {self.message}"

    @property
    def display_description(self) -> str:
        return self.code

    @property
    def is_info(self) -> bool:
        return self.severity.upper() == "INFO"

    @property
    def is_warning(self) -> bool:
        return self.severity.upper() == "WARNING"

    @property
    def is_error(self) -> bool:
        return self.severity.upper() == "ERROR"

    @property
    def has_rule(self) -> bool:
        return bool(self.rule)

    @property
    def has_location(self) -> bool:
        return bool(self.location)

    def __str__(self) -> str:
        return self.display_text
