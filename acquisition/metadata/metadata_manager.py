
from __future__ import annotations

"""
SanskritAI
==========

Metadata Manager

The MetadataManager orchestrates the execution of multiple metadata
extractors and merges their results into a single unified
ExtractionResult.

Responsibilities
----------------
* Register metadata extractors
* Execute extractors in order
* Aggregate extracted metadata
* Resolve metadata conflicts
* Aggregate diagnostics
* Produce a standardized ExtractionResult

The MetadataManager intentionally does NOT:

    • perform downloading
    • normalize corpus text
    • import corpora
    • persist metadata

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from pathlib import Path
from time import perf_counter
from typing import Any, Iterable

from SanskritAI.acquisition.metadata.base_metadata_extractor import (
    BaseMetadataExtractor,
)
from SanskritAI.acquisition.metadata.extraction_result import (
    ExtractionResult,
)


class MetadataManager:
    """
    Coordinates execution of multiple metadata extractors.
    """

    def __init__(self) -> None:

        self._extractors: list[BaseMetadataExtractor] = []

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        extractor: BaseMetadataExtractor,
    ) -> None:
        """
        Register a metadata extractor.

        Parameters
        ----------
        extractor
            Extractor instance.
        """

        self._extractors.append(extractor)

    def unregister(
        self,
        extractor: BaseMetadataExtractor,
    ) -> None:
        """
        Remove an extractor.
        """

        self._extractors.remove(extractor)

    def clear(self) -> None:
        """
        Remove all registered extractors.
        """

        self._extractors.clear()

    @property
    def extractors(
        self,
    ) -> tuple[BaseMetadataExtractor, ...]:
        """
        Registered extractors.
        """

        return tuple(self._extractors)

    # ---------------------------------------------------------
    # Extraction
    # ---------------------------------------------------------

    def extract(
        self,
        source: Path | str | bytes,
    ) -> ExtractionResult:
        """
        Execute all registered extractors.

        Parameters
        ----------
        source
            Corpus resource.

        Returns
        -------
        ExtractionResult
        """

        started = perf_counter()

        combined = ExtractionResult(
            extractor_name="MetadataManager",
        )

        metadata: dict[str, Any] = {}

        confidence_sum = 0.0
        confidence_count = 0

        for extractor in self._extractors:

            if not extractor.supports(source):
                continue

            result = extractor.extract_if_valid(
                source,
                metadata=metadata,
            )

            #
            # Merge metadata
            #

            for key, value in result.metadata.items():

                #
                # Current policy:
                # Last extractor wins.
                #
                metadata[key] = value

            #
            # Merge diagnostics
            #

            combined.warnings.extend(result.warnings)
            combined.errors.extend(result.errors)

            #
            # Merge statistics
            #

            for key, value in result.statistics.items():

                if isinstance(value, (int, float)):

                    combined.statistics[key] = (
                        combined.statistics.get(key, 0)
                        + value
                    )

                else:

                    combined.statistics[key] = value

            #
            # Merge provenance
            #

            combined.provenance[
                result.extractor_name
            ] = result.provenance

            confidence_sum += result.confidence
            confidence_count += 1

        combined.metadata = metadata

        if confidence_count:

            combined.confidence = (
                confidence_sum
                / confidence_count
            )

        combined.started_at = started
        combined.finish()

        return combined

    # ---------------------------------------------------------
    # Bulk Extraction
    # ---------------------------------------------------------

    def extract_many(
        self,
        sources: Iterable[
            Path | str | bytes
        ],
    ) -> list[ExtractionResult]:
        """
        Extract metadata for multiple resources.
        """

        return [
            self.extract(source)
            for source in sources
        ]

    # ---------------------------------------------------------
    # Introspection
    # ---------------------------------------------------------

    @property
    def extractor_count(self) -> int:
        """
        Number of registered extractors.
        """

        return len(self._extractors)

    def capabilities(self) -> set[str]:
        """
        Combined capabilities of all extractors.
        """

        capabilities: set[str] = set()

        for extractor in self._extractors:

            capabilities.update(
                extractor.capabilities()
            )

        return capabilities

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __len__(self) -> int:

        return len(self._extractors)

    def __iter__(self):

        return iter(self._extractors)

    def __repr__(self) -> str:

        return (
            "MetadataManager("
            f"extractors={len(self)}, "
            f"capabilities={len(self.capabilities())})"
        )
