
from __future__ import annotations

"""
SanskritAI
===========

Acquisition Source Types

Defines the high-level classification of corpus sources
supported by the acquisition framework.

Version:
    v0.5.0

Author:
    SanskritAI Project
"""

from enum import Enum


class SourceType(str, Enum):
    """
    High-level category of an acquisition source.

    These values describe *what* the source fundamentally is,
    independent of its storage format or transport mechanism.
    """

    # Canonical lexical resources
    LEXICON = "lexicon"

    # Literary works
    CORPUS = "corpus"

    # Grammar treatises
    GRAMMAR = "grammar"

    # Commentaries
    COMMENTARY = "commentary"

    # Ontology / taxonomy
    ONTOLOGY = "ontology"

    # Metadata repository
    METADATA = "metadata"

    # Research dataset
    DATASET = "dataset"

    # Mixed / composite collection
    COLLECTION = "collection"

    # Unknown
    UNKNOWN = "unknown"

    @property
    def is_lexical(self) -> bool:
        """Returns True if this source primarily provides lexical knowledge."""
        return self == SourceType.LEXICON

    @property
    def is_corpus(self) -> bool:
        """Returns True if this source primarily provides literary text."""
        return self == SourceType.CORPUS

    @property
    def is_reference(self) -> bool:
        """
        Returns True for reference works that enrich lexical knowledge.
        """
        return self in {
            SourceType.LEXICON,
            SourceType.GRAMMAR,
            SourceType.COMMENTARY,
            SourceType.ONTOLOGY,
            SourceType.METADATA,
        }

    @classmethod
    def from_string(cls, value: str) -> "SourceType":
        """
        Convert a string into a SourceType.

        Unknown values return SourceType.UNKNOWN.
        """
        normalized = value.strip().lower()

        for member in cls:
            if member.value == normalized:
                return member

        return cls.UNKNOWN

    def __str__(self) -> str:
        return self.value
