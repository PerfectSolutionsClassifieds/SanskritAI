from __future__ import annotations

"""
SanskritAI
==========

Sandhi Result

Defines the immutable outcome produced by every Sandhi
operation.

SandhiResult is the central value object of the Sandhi
Kernel.

Every splitter, joiner, analyzer, and resolver returns
a SandhiResult.

Future specializations
----------------------

SandhiResult
      │
      ├── SandhiSplitResult
      ├── SandhiJoinResult
      ├── SandhiAnalysisResult
      └── RecursiveSandhiResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)
from SanskritAI.domain.sandhi.sandhi_diagnostic import (
    SandhiDiagnostic,
)


@dataclass(frozen=True, slots=True)
class SandhiResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable result produced by Sandhi resolution.
    """

    context: SandhiContext

    value: Any = None

    succeeded: bool = True

    confidence: float = 1.0

    diagnostics: tuple[
        SandhiDiagnostic,
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
        return "Sandhi Result"

    @property
    def display_text(self) -> str:

        state = (
            "Succeeded"
            if self.succeeded
            else "Failed"
        )

        return f"{self.display_name} [{state}]"

    @property
    def display_description(self) -> str:

        if self.has_diagnostics:
            return self.diagnostics[0].message

        return ""

    # ---------------------------------------------------------
    # Context Convenience
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
    # Diagnostics
    # ---------------------------------------------------------

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
    ) -> SandhiDiagnostic | None:

        if not self.diagnostics:
            return None

        return self.diagnostics[0]

    # ---------------------------------------------------------
    # Resolution State
    # ---------------------------------------------------------

    @property
    def resolved(self) -> bool:
        return (
            self.succeeded
            and self.value is not None
        )

    @property
    def unresolved(self) -> bool:
        return not self.resolved

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    # ---------------------------------------------------------
    # Sandhi Convenience
    # ---------------------------------------------------------

    @property
    def has_value(self) -> bool:
        return self.value is not None

    @property
    def candidate_count(self) -> int:
        """
        Returns the number of candidate analyses.

        If the value is a tuple/list of candidate splits,
        returns its size. Otherwise returns 1 when a value
        exists.
        """

        if self.value is None:
            return 0

        if isinstance(
            self.value,
            (tuple, list),
        ):
            return len(self.value)

        return 1

    @property
    def is_ambiguous(self) -> bool:
        """
        Indicates multiple Sandhi candidates.
        """
        return self.candidate_count > 1

    def __str__(self) -> str:
        return self.display_text
