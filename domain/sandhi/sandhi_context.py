from __future__ import annotations

"""
SanskritAI
==========

Sandhi Context

Defines the canonical context for Sandhi resolution.

SandhiContext is the foundational value object of the Sandhi
Kernel. Every Sandhi operation begins with a SandhiContext,
which encapsulates the linguistic subject together with the
metadata required by Sandhi analyzers, splitters, joiners, and
future phonological engines.

The class intentionally mirrors the Resolution Kernel's
ResolutionContext while remaining specific to Sandhi.

Future consumers
----------------

• SandhiSplitter

• SandhiJoiner

• SandhiAnalyzer

• SandhiStrategy

• SandhiResolver

• SandhiRuleSet

Examples
--------

देवोऽस्ति

रामो गच्छति

तथापि

विद्यैव

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
class SandhiContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical context supplied to every Sandhi operation.
    """

    identifier: str

    subject: Any

    source: str = ""

    language: str = "Sanskrit"

    script: str = "Devanagari"

    allow_multiple_splits: bool = True

    enable_recursive_analysis: bool = True

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Sandhi Context"

    @property
    def display_text(self) -> str:
        return str(self.subject)

    @property
    def display_description(self) -> str:
        return (
            "Canonical context for Sandhi analysis."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

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
        """
        Indicates whether recursive Sandhi resolution
        is permitted.
        """
        return self.enable_recursive_analysis

    @property
    def multiple_splits_enabled(self) -> bool:
        """
        Indicates whether multiple candidate Sandhi
        splits should be explored.
        """
        return self.allow_multiple_splits

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieves optional metadata.
        """
        return self.metadata.get(
            key,
            default,
        )

    def __str__(self) -> str:
        return self.display_text
