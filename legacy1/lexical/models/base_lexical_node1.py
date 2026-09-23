from __future__ import annotations

"""
SanskritAI
==========

Base Lexical Node

Defines the abstract foundation for all lexical objects within
the SanskritAI Lexical Layer.

Unlike the Canonical Corpus Model, lexical nodes describe
linguistic knowledge rather than textual structure.

Examples
--------

Lexeme
DictionaryEntry
DictionarySense
LexicalRelation

The class intentionally contains no dictionary-specific or
morphology-specific logic. Those responsibilities belong to
derived classes.

Version
-------
v0.3.0
"""

from abc import ABC
from typing import Generic

from SanskritAI.core.typing import (
    TIdentifier,
    TMetadata,
)
from SanskritAI.corpus.models.base_node import BaseNode


class BaseLexicalNode(
    BaseNode[
        TIdentifier,
        TMetadata,
    ],
    Generic[
        TIdentifier,
        TMetadata,
    ],
    ABC,
):
    """
    Abstract base class for all lexical objects.

    Provides a common identity and metadata model for the
    lexical subsystem while remaining independent of any
    particular dictionary or linguistic theory.
    """

    def __init__(
        self,
        identifier: TIdentifier,
        metadata: TMetadata,
    ) -> None:
        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Lexical convenience
    # ---------------------------------------------------------

    @property
    def label(self) -> str:
        """
        Human-readable label for the lexical object.

        By convention this returns the metadata title when
        available; otherwise it falls back to the identifier.
        """

        title = getattr(self.metadata, "title", "")

        if title:
            return title

        return str(self.id)
