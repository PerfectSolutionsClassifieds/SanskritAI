from __future__ import annotations

"""
SanskritAI
==========

Resolution Result

Defines the immutable outcome produced by every domain
resolver.

ResolutionResult is the central value object of the
Resolution Kernel.

Every domain-specific resolver returns either this class or a
specialized subclass.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)


@dataclass(frozen=True, slots=True)
class ResolutionResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable result produced by a domain resolver.
    """

    context: ResolutionContext

    payload: Any = None

    succeeded: bool = True

    confidence: float = 1.0

    diagnostics: tuple[
        ResolutionDiagnostic,
        ...
    ] = field(default_factory=tuple)

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        return self.context.identifier

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Resolution Result"

    @property
    def display_text(self) -> str:

        status = (
            "Succeeded"
            if self.succeeded
            else "Failed"
        )

        return (
            f"{self.display_name} "
            f"[{status}]"
        )

    @property
    def display_description(self) -> str:

        if self.has_diagnostics:
            return self.first_diagnostic.message

        return ""

    # ---------------------------------------------------------
    # Context
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Payload
    # ---------------------------------------------------------

    @property
    def result(self):
        """
        Domain object produced by the resolver.

        Specialized subclasses may override this property.
        """
        return self.payload

    @property
    def has_payload(self) -> bool:
        return self.payload is not None

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def has_diagnostics(self) -> bool:
        return bool(self.diagnostics)

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def first_diagnostic(
        self,
    ) -> ResolutionDiagnostic | None:

        if not self.diagnostics:
            return None

        return self.diagnostics[0]

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

    # ---------------------------------------------------------
    # Resolution State
    # ---------------------------------------------------------

    @property
    def resolved(self) -> bool:
        return (
            self.succeeded
            and self.has_payload
        )

    @property
    def unresolved(self) -> bool:
        return not self.resolved

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
