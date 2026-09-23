from __future__ import annotations

"""
Base Lexical Metadata
=====================
"""

from dataclasses import dataclass

from SanskritAI.corpus.models.base_node_metadata import (
    BaseNodeMetadata,
)

from SanskritAI.lexical.enums.lexical_status import (
    LexicalStatus,
)


@dataclass(slots=True)
class BaseLexicalMetadata(
    BaseNodeMetadata,
):
    """
    Shared metadata for lexical objects.
    """

    language: str = "sa"

    script: str = "Devanagari"

    status: LexicalStatus = LexicalStatus.UNKNOWN

    notes: str = ""
