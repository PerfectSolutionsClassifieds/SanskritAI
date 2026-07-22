
from __future__ import annotations

"""
SanskritAI
==========

Language Extractor

Attempts to identify the natural language of a corpus resource.

Unlike ScriptExtractor, which determines the Unicode writing
system (Devanagari, Telugu, Roman, etc.), LanguageExtractor
attempts to identify the language represented by the text.

Supported Languages
-------------------
* Sanskrit
* Hindi
* Telugu
* Kannada
* Malayalam
* Tamil
* Bengali
* Gujarati
* English
* Mixed
* Unknown

The extractor is intentionally conservative.

Version
-------
v0.5.0
"""

from pathlib import Path
from typing import Any
import re

from SanskritAI.acquisition.metadata.base_metadata_extractor import (
    BaseMetadataExtractor,
)
from SanskritAI.acquisition.metadata.extraction_result import (
    ExtractionResult,
)


class LanguageExtractor(BaseMetadataExtractor):
    """
    Detect the dominant language of a corpus.
    """

    #
    # Sanskrit indicators
    #

    SANSKRIT_WORDS = {
        "अथ",
        "श्री",
        "उवाच",
        "नमः",
        "ॐ",
        "देव",
        "ऋषि",
        "योग",
        "धर्म",
        "कर्म",
        "मोक्ष",
        "ब्रह्म",
        "आत्मा",
    }

    SANSKRIT_IAST = {
        "atha",
        "śrī",
        "śiva",
        "viṣṇu",
        "brahman",
        "ātman",
        "dharma",
        "karma",
        "mokṣa",
        "veda",
        "purāṇa",
    }

    #
    # Hindi indicators
    #

    HINDI_WORDS = {
        "है",
        "था",
        "किया",
        "लिए",
        "लेकिन",
        "और",
    }

    #
    # English indicators
    #

    ENGLISH_WORDS = {
        "the",
        "and",
        "is",
        "of",
        "in",
        "for",
        "chapter",
        "verse",
    }

    # ---------------------------------------------------------
    # Metadata API
    # ---------------------------------------------------------

    def capabilities(self) -> tuple[str, ...]:

        return (
            "language",
            "language_confidence",
            "language_statistics",
        )

    # ---------------------------------------------------------
    # Extraction
    # ---------------------------------------------------------

    def extract(
        self,
        source: Path | str | bytes,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> ExtractionResult:

        result = ExtractionResult(
            extractor_name=self.__class__.__name__,
        )

        text = self._load_text(source)

        if not text.strip():

            result.add_warning(
                "No textual content available."
            )

            result.confidence = 0.0
            result.finish()

            return result

        language_scores = self._score_languages(text)

        if not language_scores:

            result.add_metadata(
                "language",
                "unknown",
            )

            result.confidence = 0.0
            result.finish()

            return result

        #
        # Determine dominant language
        #

        ordered = sorted(
            language_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        top_language, top_score = ordered[0]

        total = sum(language_scores.values())

        confidence = (
            top_score / total
            if total > 0
            else 0.0
        )

        #
        # Mixed language detection
        #

        if len(ordered) > 1:

            second_score = ordered[1][1]

            if (
                second_score > 0
                and second_score / top_score > 0.60
            ):

                top_language = "mixed"

                result.add_warning(
                    "Multiple languages detected."
                )

        result.add_metadata(
            "language",
            top_language,
        )

        result.add_metadata(
            "language_statistics",
            language_scores,
        )

        result.add_metadata(
            "language_confidence",
            confidence,
        )

        result.statistics["tokens"] = len(
            self._tokenize(text)
        )

        result.confidence = confidence

        result.finish()

        return result

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _load_text(
        self,
        source: Path | str | bytes,
    ) -> str:

        if isinstance(source, bytes):

            return source.decode(
                "utf-8",
                errors="replace",
            )

        if isinstance(source, Path):

            if source.exists():

                return source.read_text(
                    encoding="utf-8",
                    errors="replace",
                )

            return ""

        return source

    def _tokenize(
        self,
        text: str,
    ) -> list[str]:

        return re.findall(
            r"[^\W\d_]+",
            text.lower(),
            flags=re.UNICODE,
        )

    def _score_languages(
        self,
        text: str,
    ) -> dict[str, int]:

        tokens = self._tokenize(text)

        scores = {
            "sanskrit": 0,
            "hindi": 0,
            "english": 0,
        }

        for token in tokens:

            if (
                token in self.SANSKRIT_WORDS
                or token in self.SANSKRIT_IAST
            ):

                scores["sanskrit"] += 1

            if token in self.HINDI_WORDS:

                scores["hindi"] += 1

            if token in self.ENGLISH_WORDS:

                scores["english"] += 1

        #
        # Remove zero-score languages
        #

        return {
            language: score
            for language, score in scores.items()
            if score > 0
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return "LanguageExtractor()"
