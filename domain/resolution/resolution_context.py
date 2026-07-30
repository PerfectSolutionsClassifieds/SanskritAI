from __future__ import annotations

"""
SanskritAI
==========

Resolution Context

Defines the immutable context supplied to every domain
resolver.

ResolutionContext is the foundational value object of the
Resolution Kernel. It encapsulates the subject being resolved
together with optional contextual information required by a
resolution strategy.

The class is intentionally generic so that it can be reused by
all future domain kernels.

Examples
--------

Lexical Resolution

    WordForm
        │
        ▼
    ResolutionContext

Morphological Resolution

    Token
        │
        ▼
    ResolutionContext

Sandhi Resolution

    Surface Form
        │
        ▼
    ResolutionContext

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ResolutionContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable context supplied to a domain resolver.
    """

    identifier: str

    subject: Any

    source: str = ""

    language: str = ""

    script: str = ""

    metadata: dict[str, Any] | None = None

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Resolution Context"

    @property
    def display_text(self) -> str:
        return str(self.subject)

    @property
    def display_description(self) -> str:
        return (
            "Immutable context supplied to a "
            "domain resolver."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_source(self) -> bool:
        return bool(self.source)

    @property
    def has_language(self) -> bool:
        return bool(self.language)

    @property
    def has_script(self) -> bool:
        return bool(self.script)

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieves a metadata value.

        Returns the supplied default when the key does not
        exist.
        """

        if self.metadata is None:
            return default

        return self.metadata.get(key, default)

    def __str__(self) -> str:
        return self.display_text
