from __future__ import annotations

"""
SanskritAI
==========

Word View

Immutable reader representation of a single Sanskrit word.

WordView is the bridge between the Reader Domain and the
Resolution Kernel.

It owns exactly one ResolutionResult, which aggregates all
linguistic analyses (lexical, morphology, sandhi, samāsa,
semantic, etc.).

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.domain.reader.reader_node import ReaderNode
from SanskritAI.domain.resolution.resolution_result import ResolutionResult


@dataclass(frozen=True, slots=True)
class WordView(
    ReaderNode,
):
    """
    Immutable reader representation of one Sanskrit word.
    """

    document_identifier: str = ""

    chapter_identifier: str = ""

    sloka_identifier: str = ""

    word_index: int = 0

    surface_form: str = ""

    normalized_form: str = ""

    resolution: ResolutionResult | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    notes: str = ""

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.surface_form or f"Word {self.word_index}"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.notes

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    @property
    def has_resolution(self) -> bool:
        return self.resolution is not None

    @property
    def lexical(self):
        if self.resolution is None:
            return None
        return self.resolution.lexical

    @property
    def morphology(self):
        if self.resolution is None:
            return None
        return self.resolution.morphology

    @property
    def sandhi(self):
        if self.resolution is None:
            return None
        return self.resolution.sandhi

    @property
    def samasa(self):
        if self.resolution is None:
            return None
        return self.resolution.samasa

    @property
    def semantic(self):
        if self.resolution is None:
            return None
        return self.resolution.semantic

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
