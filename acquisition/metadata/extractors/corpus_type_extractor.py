
from __future__ import annotations

"""
SanskritAI
==========

Corpus Type Extractor

Determines the logical corpus type of a Sanskrit resource.

Unlike ScriptExtractor or LanguageExtractor, this extractor
identifies the *kind of literary work* represented by the corpus.

Examples
--------
    • Purana
    • Mahabharata
    • Ramayana
    • Veda
    • Upanishad
    • Itihasa
    • Kavya
    • Stotra
    • Sutra
    • Dictionary
    • Lexicon
    • Grammar
    • Commentary
    • Philosophy
    • Tantra
    • Unknown

Detection Sources
-----------------
1. Existing metadata
2. Title
3. Filename
4. Beginning of document
5. Repository metadata

Version
-------
v0.5.0

Author
------
SanskritAI Project
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


class CorpusTypeExtractor(BaseMetadataExtractor):
    """
    Detects the literary corpus type.
    """

    #
    # Ordered by specificity.
    #

    CORPUS_PATTERNS = {

        "dictionary": [
            "amarakosha",
            "amarakośa",
            "amarakosa",
            "vacaspatyam",
            "vācaspatyam",
            "shabdakalpadruma",
            "śabdakalpadruma",
            "lexicon",
            "dictionary",
            "kosha",
            "kośa",
        ],

        "grammar": [
            "ashtadhyayi",
            "aṣṭādhyāyī",
            "panini",
            "pāṇini",
            "vyakarana",
            "vyākaraṇa",
            "grammar",
            "laghusiddhanta",
            "siddhānta",
        ],

        "veda": [
            "rigveda",
            "ṛgveda",
            "yajurveda",
            "samaveda",
            "atharvaveda",
            "veda",
        ],

        "upanishad": [
            "upanishad",
            "upaniṣad",
        ],

        "purana": [
            "purana",
            "purāṇa",
            "bhagavata",
            "bhāgavata",
            "shivapurana",
            "śivapurāṇa",
            "skandapurana",
            "brahmapurana",
            "vishnupurana",
        ],

        "itihasa": [
            "mahabharata",
            "mahābhārata",
            "ramayana",
            "rāmāyaṇa",
            "harivamsha",
            "harivaṃśa",
        ],

        "sutra": [
            "sutra",
            "sūtra",
            "brahmasutra",
            "yogasutra",
        ],

        "kavya": [
            "kāvya",
            "kavya",
            "raghuvamsha",
            "raghuvaṃśa",
            "kumarasambhava",
            "meghaduta",
        ],

        "stotra": [
            "stotra",
            "stotra",
            "sahasranama",
            "sahasranāma",
            "ashtakam",
            "aṣṭakam",
        ],

        "commentary": [
            "bhashya",
            "bhāṣya",
            "ṭīkā",
            "tika",
            "vyakhya",
            "vyākhyā",
            "commentary",
        ],

        "tantra": [
            "tantra",
            "āgama",
            "agama",
        ],

        "philosophy": [
            "darshana",
            "darśana",
            "vedanta",
            "vedānta",
            "mimamsa",
            "mīmāṃsā",
            "nyaya",
            "nyāya",
        ],
    }

    # ---------------------------------------------------------
    # Metadata API
    # ---------------------------------------------------------

    def capabilities(self) -> tuple[str, ...]:

        return (
            "corpus_type",
            "corpus_type_confidence",
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

        searchable = self._build_search_text(
            source,
            metadata,
        )

        corpus_type = self._detect(searchable)

        if corpus_type is None:

            corpus_type = "unknown"

            confidence = 0.0

            result.add_warning(
                "Unable to determine corpus type."
            )

        else:

            confidence = 0.95

        result.add_metadata(
            "corpus_type",
            corpus_type,
        )

        result.add_metadata(
            "corpus_type_confidence",
            confidence,
        )

        result.confidence = confidence

        result.statistics["characters_examined"] = len(
            searchable
        )

        result.finish()

        return result

    # ---------------------------------------------------------
    # Internal Helpers
    # ---------------------------------------------------------

    def _build_search_text(
        self,
        source: Path | str | bytes,
        metadata: dict[str, Any] | None,
    ) -> str:

        pieces: list[str] = []

        #
        # Existing metadata
        #

        if metadata:

            for key in (
                "title",
                "description",
                "repository",
                "filename",
            ):

                value = metadata.get(key)

                if isinstance(value, str):

                    pieces.append(value)

        #
        # Source
        #

        if isinstance(source, Path):

            pieces.append(source.name)

            if source.exists():

                try:

                    text = source.read_text(
                        encoding="utf-8",
                        errors="replace",
                    )

                    #
                    # Only first 5000 chars.
                    #

                    pieces.append(text[:5000])

                except Exception:

                    pass

        elif isinstance(source, bytes):

            pieces.append(
                source.decode(
                    "utf-8",
                    errors="replace",
                )[:5000]
            )

        else:

            pieces.append(source[:5000])

        return " ".join(pieces).lower()

    def _detect(
        self,
        searchable: str,
    ) -> str | None:

        for corpus_type, keywords in (
            self.CORPUS_PATTERNS.items()
        ):

            for keyword in keywords:

                if re.search(
                    re.escape(keyword.lower()),
                    searchable,
                ):

                    return corpus_type

        return None

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return "CorpusTypeExtractor()"
