from __future__ import annotations

"""
SanskritAI
==========

Vakya Result

Defines the immutable outcome produced by every Vakya
analysis.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.vakya.vakya_context import VakyaContext
from SanskritAI.domain.vakya.vakya_diagnostic import VakyaDiagnostic


@dataclass(frozen=True, slots=True)
class VakyaResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable result produced by Vakya resolution.
    """

    context: VakyaContext

    value: Any = None

    succeeded: bool = True

    confidence: float = 1.0

    diagnostics: tuple[
        VakyaDiagnostic,
        ...
    ] = field(default_factory=tuple)

    @property
    def identifier(self) -> str:
        return self.context.identifier

    @property
    def display_name(self) -> str:
        return "Vakya Result"

    @property
    def display_text(self) -> str:
        state = "Succeeded" if self.succeeded else "Failed"
        return f"{self.display_name} [{state}]"

    @property
    def display_description(self) -> str:
        if self.has_diagnostics:
            return self.diagnostics[0].message
        return ""

    @property
    def subject(self):
        return self.context.subject

    @property
    def source(self) -> str:
        return self.context.source

    @property
    def language(self) -> str:
        return self.context.language

    @property
    def script(self) -> str:
        return self.context.script

    @property
    def has_diagnostics(self) -> bool:
        return len(self.diagnostics) > 0

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def has_errors(self) -> bool:
        return any(
            diagnostic.is_error
            for diagnostic in self.diagnostics
        )

    @property
    def has_warnings(self) -> bool:
        return any(
            diagnostic.is_warning
            for diagnostic in self.diagnostics
        )

    @property
    def first_diagnostic(
        self,
    ) -> VakyaDiagnostic | None:
        if not self.diagnostics:
            return None
        return self.diagnostics[0]

    @property
    def resolved(self) -> bool:
        return self.succeeded and self.value is not None

    @property
    def unresolved(self) -> bool:
        return not self.resolved

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    @property
    def has_value(self) -> bool:
        return self.value is not None

    @property
    def result(self):
        return self.value

    def __str__(self) -> str:
        return self.display_text
