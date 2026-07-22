
from __future__ import annotations

"""
SanskritAI
==========

Script Extractor

Determines the writing system (script) used by a Sanskrit corpus.

Supported scripts
-----------------
* Devanagari
* Telugu
* Kannada
* Malayalam
* Tamil
* Grantha (basic Unicode block)
* Bengali
* Gujarati
* Gurmukhi
* Oriya (Odia)
* Roman / IAST
* Unknown

The extractor is intentionally conservative. It identifies the
dominant script based on Unicode code point statistics rather than
attempting linguistic analysis.

Version
-------
v0.5.0
"""

from pathlib import Path
from typing import Any
from collections import Counter

from SanskritAI.acquisition.metadata.base_metadata_extractor import (
    BaseMetadataExtractor,
)
from SanskritAI.acquisition.metadata.extraction_result import (
    ExtractionResult,
)


class ScriptExtractor(BaseMetadataExtractor):
    """
    Detects the dominant Unicode writing system.
    """

    SCRIPT_RANGES = {
        "devanagari": (0x0900, 0x097F),
        "bengali": (0x0980, 0x09FF),
        "gurmukhi": (0x0A00, 0x0A7F),
        "gujarati": (0x0A80, 0x0AFF),
        "oriya": (0x0B00, 0x0B7F),
        "tamil": (0x0B80, 0x0BFF),
        "telugu": (0x0C00, 0x0C7F),
        "kannada": (0x0C80, 0x0CFF),
        "malayalam": (0x0D00, 0x0D7F),
        "grantha": (0x11300, 0x1137F),
    }

    LATIN_BLOCK = (0x0000, 0x007F)
    LATIN_EXT_A = (0x0100, 0x017F)
    LATIN_EXT_B = (0x0180, 0x024F)

    IAST_CHARACTERS = {
        "ā", "ī", "ū",
        "ṛ", "ṝ",
        "ḷ", "ḹ",
        "ṅ", "ñ", "ṇ",
        "ṭ", "ḍ",
        "ś", "ṣ",
        "ṃ", "ṁ",
        "ḥ",
    }

    # ---------------------------------------------------------
    # Metadata API
    # ---------------------------------------------------------

    def capabilities(self) -> tuple[str, ...]:
        return (
            "script",
            "script_confidence",
            "script_statistics",
        )

    # ---------------------------------------------------------
    # Extraction
    # ---------------------------------------------------------

    def extract(
        self,
        source: Path | str |bytes,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> ExtractionResult:

        result = ExtractionResult(
            extractor_name=self.__class__.__name__,
        )

        text = self._load_text(source)

        if not text:

            result.add_warning(
                "No textual content available."
            )

            result.confidence = 0.0
            result.finish()

            return result

        counts = self._count_scripts(text)

        if not counts:

            result.add_metadata(
                "script",
                "unknown",
            )

            result.confidence = 0.0

            result.finish()

            return result

        dominant, occurrences = counts.most_common(1)[0]

        total = sum(counts.values())

        confidence = occurrences / total

        result.add_metadata(
            "script",
            dominant,
        )

        result.add_metadata(
            "script_statistics",
            dict(counts),
        )

        result.add_metadata(
            "script_confidence",
            confidence,
        )

        result.statistics["characters_analyzed"] = total

        result.statistics["unique_scripts"] = len(counts)

        result.confidence = confidence

        if len(counts) > 1:

            result.add_warning(
                "Multiple Unicode scripts detected."
            )

        result.finish()

        return result

    # ---------------------------------------------------------
    # Text Loading
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

    # ---------------------------------------------------------
    # Script Counting
    # ---------------------------------------------------------

    def _count_scripts(
        self,
        text: str,
    ) -> Counter[str]:

        counter: Counter[str] = Counter()

        for ch in text:

            if ch.isspace():
                continue

            script = self._detect_character_script(ch)

            if script is not None:

                counter[script] += 1

        return counter

    # ---------------------------------------------------------
    # Character Detection
    # ---------------------------------------------------------

    def _detect_character_script(
        self,
        ch: str,
    ) -> str | None:

        cp = ord(ch)

        #
        # Indic scripts
        #

        for script, (start, end) in self.SCRIPT_RANGES.items():

            if start <= cp <= end:

                return script

        #
        # Roman / IAST
        #

        if ch in self.IAST_CHARACTERS:

            return "roman"

        if (
            self.LATIN_BLOCK[0]
            <= cp
            <= self.LATIN_BLOCK[1]
        ):

            if ch.isalpha():

                return "roman"

        if (
            self.LATIN_EXT_A[0]
            <= cp
            <= self.LATIN_EXT_A[1]
        ):

            return "roman"

        if (
            self.LATIN_EXT_B[0]
            <= cp
            <= self.LATIN_EXT_B[1]
        ):

            return "roman"

        return None

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return "ScriptExtractor()"
