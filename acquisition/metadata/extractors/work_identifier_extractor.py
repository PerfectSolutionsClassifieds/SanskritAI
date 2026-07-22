
from __future__ import annotations

"""
SanskritAI
==========

Work Identifier Extractor

Identifies the canonical Sanskrit work represented by an acquired
resource.

Unlike earlier implementations, this extractor contains no embedded
knowledge of individual works. All canonical work definitions are
loaded through WorkRegistry, making the extractor independent of the
underlying storage format (JSON today, YAML/SQL tomorrow).

Responsibilities
----------------
* Build searchable text from the acquisition source
* Query the WorkRegistry
* Return canonical work metadata
* Report confidence
* Remain completely stateless

Version
-------
v0.5.0
"""

from pathlib import Path
from typing import Any

from SanskritAI.acquisition.metadata.base_metadata_extractor import (
    BaseMetadataExtractor,
)

from SanskritAI.acquisition.metadata.extraction_result import (
    ExtractionResult,
)

from SanskritAI.acquisition.metadata.registries.work_registry import (
    WorkRegistry,
    WorkDefinition,
)


class WorkIdentifierExtractor(BaseMetadataExtractor):
    """
    Identifies the canonical work represented by a corpus resource.
    """

    def __init__(
        self,
        registry: WorkRegistry | None = None,
    ) -> None:
        super().__init__()

        self._registry = registry or WorkRegistry()

    # ---------------------------------------------------------
    # Metadata API
    # ---------------------------------------------------------

    def capabilities(self) -> tuple[str, ...]:

        return (
            "work_identifier",
            "canonical_title",
            "work_metadata",
            "work_confidence",
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

        searchable = self._build_searchable_text(
            source,
            metadata,
        )

        work = self._registry.find_work(
            searchable,
        )

        if work is None:

            result.add_warning(
                "Canonical work could not be identified."
            )

            result.add_metadata(
                "work_identifier",
                "unknown",
            )

            result.add_metadata(
                "canonical_title",
                None,
            )

            result.add_metadata(
                "work_metadata",
                {},
            )

            result.confidence = 0.0

            result.finish()

            return result

        self._populate_result(
            result,
            work,
        )

        result.finish()

        return result

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------

    def _populate_result(
        self,
        result: ExtractionResult,
        work: WorkDefinition,
    ) -> None:

        result.add_metadata(
            "work_identifier",
            work.identifier,
        )

        result.add_metadata(
            "canonical_title",
            work.title,
        )

        result.add_metadata(
            "work_metadata",
            work.metadata,
        )

        result.add_metadata(
            "work_confidence",
            0.99,
        )

        result.statistics[
            "alias_count"
        ] = len(work.aliases)

        result.confidence = 0.99

    # ---------------------------------------------------------

    def _build_searchable_text(
        self,
        source: Path | str | bytes,
        metadata: dict[str, Any] | None,
    ) -> str:

        parts: list[str] = []

        #
        # Existing metadata
        #

        if metadata:

            for key in (
                "title",
                "filename",
                "description",
                "repository",
                "work",
            ):

                value = metadata.get(key)

                if isinstance(value, str):

                    parts.append(value)

        #
        # Source
        #

        if isinstance(source, Path):

            parts.append(source.name)

            if source.exists():

                try:

                    parts.append(

                        source.read_text(
                            encoding="utf-8",
                            errors="replace",
                        )[:5000]

                    )

                except Exception:

                    pass

        elif isinstance(source, bytes):

            parts.append(

                source.decode(
                    "utf-8",
                    errors="replace",
                )[:5000]

            )

        elif isinstance(source, str):

            parts.append(source[:5000])

        return "\n".join(parts)

    # ---------------------------------------------------------

    @property
    def registry(
        self,
    ) -> WorkRegistry:
        """
        Expose registry for diagnostics/testing.
        """

        return self._registry

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(works={len(self._registry)})"
        )
