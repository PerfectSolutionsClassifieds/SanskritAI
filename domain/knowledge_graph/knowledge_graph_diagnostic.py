from __future__ import annotations

"""
SanskritAI
==========

Knowledge Graph Diagnostic

Defines immutable diagnostics produced during graph
construction.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class KnowledgeGraphDiagnostic(
    ValueObject,
    Immutable,
    Displayable,
):
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

    def __str__(self) -> str:
        return self.display_text
