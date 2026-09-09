
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .monier_williams_acquisition_result import (
    MonierWilliamsAcquisitionResult,
)

from .monier_williams_acquisition_service import (
    MonierWilliamsAcquisitionService,
)

from .monier_williams_source_parser import (
    MonierWilliamsSourceParser,
)

from .monier_williams_source_record import (
    MonierWilliamsSourceRecord,
)

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)


@dataclass(frozen=True, slots=True)
class MonierWilliamsSourcePipeline:
    """
    Acquisition-stage Monier-Williams pipeline.

    Responsibility
    --------------

        Source
          ↓
        Acquisition Service
          ↓
        Raw source text
          ↓
        MonierWilliamsSourceParser
          ↓
        MonierWilliamsSourceRecord
          ↓
        explicit normalization boundary
          ↓
        MonierWilliamsRecord

    Important
    ---------

    The acquisition pipeline does not import the
    MonierWilliamsMapper at module import time.

    This prevents the dependency cycle:

        MonierWilliamsMapper
            ↓
        acquisition.monier_williams
            ↓
        MonierWilliamsSourcePipeline
            ↓
        MonierWilliamsMapper

    The mapper is imported lazily only when the explicit
    normalization operation is requested.
    """

    service: MonierWilliamsAcquisitionService
    parser: MonierWilliamsSourceParser | None = None

    # =========================================================
    # Acquisition
    # =========================================================

    def run(
        self,
    ) -> MonierWilliamsAcquisitionResult | object:
        """
        Execute the configured acquisition service.

        This method preserves the existing acquisition-service API.
        """

        return self.service.acquire()

    # =========================================================
    # Parsing
    # =========================================================

    def parse(
        self,
    ) -> tuple[
        MonierWilliamsSourceRecord
        | MonierWilliamsRecord,
        ...,
    ]:
        """
        Acquire and parse the Monier-Williams source.
        """

        return self.records()

    def records(
        self,
    ) -> tuple[
        MonierWilliamsSourceRecord
        | MonierWilliamsRecord,
        ...,
    ]:
        """
        Acquire source text and delegate parsing to
        MonierWilliamsSourceParser.

        The pipeline does not implement parsing logic itself.

        The parser remains the single parsing authority.
        """

        source_text = self._read_source()

        parser = self.parser

        if parser is None:
            parser = MonierWilliamsSourceParser()

        records = parser.parse(source_text)

        if not isinstance(
            records,
            (tuple, list),
        ):
            raise TypeError(
                "Monier-Williams parser must return "
                "a tuple or list of records"
            )

        normalized = tuple(records)

        for record in normalized:

            if isinstance(
                record,
                (
                    MonierWilliamsSourceRecord,
                    MonierWilliamsRecord,
                ),
            ):
                continue

            raise TypeError(
                "Monier-Williams source parser returned "
                "unsupported record type: "
                f"{type(record).__name__}"
            )

        return normalized

    # =========================================================
    # Explicit normalization boundary
    # =========================================================

    def normalized_records(
        self,
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Convert acquisition-stage SourceRecords into
        normalized MonierWilliamsRecord objects.

        Existing MonierWilliamsRecord instances are preserved.

        This is the explicit:

            SourceRecord
                ↓
            MonierWilliamsRecord

        boundary.

        The mapper import is intentionally local to this
        method so the acquisition package does not create
        a module-level dependency cycle with the domain
        adapter.
        """

        # IMPORTANT:
        # This local import breaks the circular dependency
        # between the acquisition package __init__ and the
        # domain MonierWilliamsMapper.
        from SanskritAI.domain.lexical.adapters.monier_williams_mapper import (
            MonierWilliamsMapper,
        )

        records = self.records()

        normalized: list[MonierWilliamsRecord] = []

        for record in records:

            if isinstance(
                record,
                MonierWilliamsRecord,
            ):
                normalized.append(record)
                continue

            if isinstance(
                record,
                MonierWilliamsSourceRecord,
            ):
                normalized.append(
                    MonierWilliamsMapper.from_source_record(
                        record
                    )
                )
                continue

            raise TypeError(
                "Unsupported Monier-Williams record at "
                "normalization boundary: "
                f"{type(record).__name__}"
            )

        return tuple(normalized)

    # =========================================================
    # Source reading
    # =========================================================

    def _read_source(self) -> str:
        """
        Read raw source text directly from the acquisition service.

        Parsing belongs to MonierWilliamsSourceParser.
        """

        source_text = self.service.read()

        if not isinstance(
            source_text,
            str,
        ):
            raise TypeError(
                "Monier-Williams acquisition service "
                "must return source text as str"
            )

        if not source_text.strip():
            raise ValueError(
                "Monier-Williams source is empty"
            )

        return source_text
