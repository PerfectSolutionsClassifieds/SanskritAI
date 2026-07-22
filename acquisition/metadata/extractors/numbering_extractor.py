
from __future__ import annotations

"""
SanskritAI
==========

Numbering Extractor

Extracts structural numbering metadata from Sanskrit corpora.

Unlike TitleExtractor or CorpusTypeExtractor, this extractor
identifies the hierarchical organization of a work.

Examples
--------
Purana
    Skandha -> Adhyaya -> Sloka

Ramayana
    Kanda -> Sarga -> Sloka

Mahabharata
    Parva -> Adhyaya -> Sloka

Veda
    Mandala -> Sukta -> Mantra

Upanishad
    Chapter -> Mantra

Dictionary
    Varga -> Entry

The extractor intentionally performs only metadata discovery.
It does NOT parse the complete document hierarchy.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

import re
from collections import Counter
from pathlib import Path
from typing import Any

from SanskritAI.acquisition.metadata.base_metadata_extractor import (
    BaseMetadataExtractor,
)
from SanskritAI.acquisition.metadata.extraction_result import (
    ExtractionResult,
)


class NumberingExtractor(BaseMetadataExtractor):
    """
    Detects structural numbering systems used by a corpus.
    """

    #
    # Hierarchy keywords
    #

    LEVEL_PATTERNS: dict[str, tuple[str, ...]] = {

        "mandala": (
            "मण्डल",
            "maṇḍala",
            "mandala",
        ),

        "kanda": (
            "काण्ड",
            "kāṇḍa",
            "kanda",
        ),

        "parva": (
            "पर्व",
            "parva",
        ),

        "skandha": (
            "स्कन्ध",
            "skandha",
        ),

        "adhyaya": (
            "अध्याय",
            "adhyāya",
            "adhyaya",
        ),

        "sarga": (
            "सर्ग",
            "sarga",
        ),

        "sukta": (
            "सूक्त",
            "sūkta",
            "sukta",
        ),

        "mantra": (
            "मन्त्र",
            "mantra",
        ),

        "sloka": (
            "श्लोक",
            "śloka",
            "sloka",
            "verse",
        ),

        "varga": (
            "वर्ग",
            "varga",
        ),

        "entry": (
            "entry",
            "headword",
        ),
    }

    #
    # Generic numeric patterns
    #

    NUMERIC_PATTERNS = (

        r"\d+\.\d+\.\d+",

        r"\d+\.\d+",

        r"\d+",

    )

    def capabilities(self) -> tuple[str, ...]:

        return (

            "hierarchy",

            "numbering_scheme",

            "numbering_statistics",

        )

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

        if metadata:

            title = metadata.get("title")

            if isinstance(title, str):

                text = title + "\n" + text

        hierarchy = self._detect_levels(text)

        numbering = self._detect_numbering(text)

        result.add_metadata(
            "hierarchy",
            hierarchy,
        )

        result.add_metadata(
            "numbering_scheme",
            numbering,
        )

        result.add_metadata(
            "numbering_statistics",
            {

                "levels_detected": len(hierarchy),

                "numeric_patterns": len(numbering),

            },
        )

        confidence = min(
            1.0,
            (
                len(hierarchy) * 0.20
                + len(numbering) * 0.05
            ),
        )

        result.confidence = confidence

        if not hierarchy:

            result.add_warning(
                "No structural hierarchy detected."
            )

        result.statistics["characters_examined"] = len(text)

        result.finish()

        return result

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

    def _detect_levels(
        self,
        text: str,
    ) -> list[str]:

        text = text.lower()

        detected: list[str] = []

        for level, keywords in self.LEVEL_PATTERNS.items():

            for keyword in keywords:

                if keyword.lower() in text:

                    detected.append(level)

                    break

        return detected

    # ---------------------------------------------------------

    def _detect_numbering(
        self,
        text: str,
    ) -> dict[str, int]:

        counter: Counter[str] = Counter()

        for pattern in self.NUMERIC_PATTERNS:

            matches = re.findall(pattern, text)

            if matches:

                counter[pattern] += len(matches)

        return dict(counter)

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "NumberingExtractor("
            f"levels={len(self.LEVEL_PATTERNS)})"
        )
