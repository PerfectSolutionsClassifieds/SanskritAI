from __future__ import annotations

"""
SanskritAI
==========

Classification

Canonical classification model shared by all corpus entities.

Purpose
-------
Provides a reusable classification object describing the
language, script and corpus type of a corpus entity.

Rather than storing these values independently in every
metadata class, they are encapsulated here for consistency
and future extensibility.

Used By
-------
* CorpusMetadata
* DocumentMetadata
* Section (future)
* Chapter (future)
* Verse (future)

Future Extensions
-----------------
* Automatic language detection
* Automatic script detection
* Classification confidence
* Multiple candidate languages
* Mixed-script support

Version
-------
v0.1.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.common.metadata.confidence_score import (
    ConfidenceScore,
)

from SanskritAI.corpus.enums.language import Language
from SanskritAI.corpus.enums.script import Script
from SanskritAI.corpus.enums.corpus_type import CorpusType


@dataclass(slots=True)
class Classification:
    """
    Canonical classification for a corpus entity.
    """

    # ---------------------------------------------------------
    # Core Classification
    # ---------------------------------------------------------

    language: Language = Language.UNKNOWN

    script: Script = Script.UNKNOWN

    corpus_type: CorpusType = CorpusType.UNKNOWN

    # ---------------------------------------------------------
    # Detection Confidence
    # ---------------------------------------------------------

    confidence: ConfidenceScore = field(
        default_factory=lambda: ConfidenceScore(1.0)
    )

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def is_unknown(self) -> bool:
        """
        True if all classifications are unknown.
        """
        return (

            self.language is Language.UNKNOWN

            and self.script is Script.UNKNOWN

            and self.corpus_type is CorpusType.UNKNOWN

        )

    @property
    def is_mixed(self) -> bool:
        """
        True if either language or script is mixed.
        """
        return (

            self.language is Language.MIXED

            or self.script is Script.MIXED

        )

    # ---------------------------------------------------------
    # Update Helpers
    # ---------------------------------------------------------

    def set_language(
        self,
        language: Language,
        confidence: ConfidenceScore | None = None,
    ) -> None:

        self.language = language

        if confidence is not None:
            self.confidence = confidence

    def set_script(
        self,
        script: Script,
        confidence: ConfidenceScore | None = None,
    ) -> None:

        self.script = script

        if confidence is not None:
            self.confidence = confidence

    def set_corpus_type(
        self,
        corpus_type: CorpusType,
    ) -> None:

        self.corpus_type = corpus_type

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:

        return {

            "language": self.language.value,

            "script": self.script.value,

            "corpus_type": self.corpus_type.value,

            "confidence": self.confidence.to_dict(),

        }

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            "Classification("

            f"language={self.language.name}, "

            f"script={self.script.name}, "

            f"corpus_type={self.corpus_type.name}, "

            f"confidence={self.confidence})"

        )
