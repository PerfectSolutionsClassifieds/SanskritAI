from __future__ import annotations

"""
SanskritAI
==========

Alankara Context

Defines the canonical context for Alankara analysis.

AlankaraContext is the foundational value object of the
Alankara Kernel. Every figure-of-speech analysis operation
begins with an AlankaraContext, which encapsulates the
subject and metadata required by alankara analyzers and rules.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class AlankaraContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical context supplied to every Alankara operation.
    """

    identifier: str

    subject: Any

    source: str = ""

    language: str = "Sanskrit"

    script: str = "Devanagari"

    allow_multiple_analyses: bool = True

    enable_recursive_analysis: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return "Alankara Context"

    @property
    def display_text(self) -> str:
        return str(self.subject)

    @property
    def display_description(self) -> str:
        return "Canonical context for Alankara analysis."

    @property
    def has_source(self) -> bool:
        return bool(self.source)

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    @property
    def metadata_count(self) -> int:
        return len(self.metadata)

    @property
    def recursive(self) -> bool:
        return self.enable_recursive_analysis

    @property
    def multiple_analyses_enabled(self) -> bool:
        return self.allow_multiple_analyses

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def __str__(self) -> str:
        return self.display_text
