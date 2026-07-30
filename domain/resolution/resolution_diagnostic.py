from __future__ import annotations

"""
SanskritAI
==========

Resolution Diagnostic

Defines an immutable diagnostic produced during a domain
resolution operation.

Diagnostics provide structured information describing
successful resolution decisions, informational messages,
warnings, and errors.

Unlike exceptions, diagnostics are intended to accompany a
ResolutionResult and allow downstream components to inspect
how a resolver reached its conclusion.

The class is intentionally domain-independent and therefore
can be reused by:

    • Lexical Resolution

    • Morphological Resolution

    • Sandhi Resolution

    • Samāsa Resolution

    • Dhātu Resolution

    • Grammar Resolution

    • Semantic Resolution

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ResolutionDiagnostic(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable diagnostic emitted by a domain resolver.
    """

    code: str

    message: str

    severity: str = "information"

    source: str = ""

    recoverable: bool = True

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        return self.code

    @property
    def display_name(self) -> str:
        return self.code

    @property
    def display_text(self) -> str:
        return (
            f"[{self.severity.upper()}] "
            f"{self.message}"
        )

    @property
    def display_description(self) -> str:
        return self.message

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_information(self) -> bool:
        return self.severity.lower() == "information"

    @property
    def is_warning(self) -> bool:
        return self.severity.lower() == "warning"

    @property
    def is_error(self) -> bool:
        return self.severity.lower() == "error"

    @property
    def is_fatal(self) -> bool:
        return (
            self.is_error
            and not self.recoverable
        )

    @property
    def has_source(self) -> bool:
        return bool(self.source)

    def __str__(self) -> str:
        return self.display_text
