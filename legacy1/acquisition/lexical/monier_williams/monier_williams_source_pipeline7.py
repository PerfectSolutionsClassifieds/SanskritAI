
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

from SanskritAI.domain.lexical.adapters.monier_williams_mapper import (
    MonierWilliamsMapper,
)

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)


@dataclass(frozen=True, slots=True)
class MonierWilliamsSourcePipeline:
    """
    Monier-Williams acquisition pipeline.

    Acquisition flow
    ----------------

        Source
          ↓
        Acquisition Service
          ↓
        Source Parser
          ↓
        MonierWilliamsSourceRecord
          ↓
        Explicit adapter boundary
          ↓
        MonierWilliamsRecord
    """

    service: MonierWilliamsAcquisitionService
    parser: MonierWilliamsSourceParser | None = None

    # =========================================================
    # Acquisition
    # =========================================================

    def run(
        self,
    ) -> (
        MonierWilliamsAcquisitionResult
        | Sequence[
            MonierWilliamsSourceRecord
            | MonierWilliamsRecord
        ]
    ):
        """
        Execute the configured acquisition service.
        """

        return self.service.acquire()

    # =========================================================
    # Source parsing
    # =========================================================

    def parse(
        self,
    ) -> tuple[
        MonierWilliamsSourceRecord
        | MonierWilliamsRecord,
        ...
    ]:
        """
        Parse acquired source content.

        This method exposes the parser result without
        silently converting its record representation.
        """

        return self.records()

    def records(
        self,
    ) -> tuple[
        MonierWilliamsSourceRecord
        | MonierWilliamsRecord,
        ...
    ]:
        """
        Retrieve and parse source records.

        Parsing remains delegated entirely to
        MonierWilliamsSourceParser.
        """

        result = self.run()

        # -----------------------------------------------------
        # Service may already have returned structured records.
        # -----------------------------------------------------

        if isinstance(
            result,
            (tuple, list),
        ):
            records = tuple(result)

            for record in records:
                if not isinstance(
                    record,
                    (
                        MonierWilliamsSourceRecord,
                        MonierWilliamsRecord,
                    ),
                ):
                    raise TypeError(
                        "Monier-Williams acquisition returned "
                        "an unsupported record type: "
                        f"{type(record).__name__}"
                    )

            return records

        # -----------------------------------------------------
        # Extract acquired source text.
        # -----------------------------------------------------

        if isinstance(
            result,
            MonierWilliamsAcquisitionResult,
        ):
            text = result.text

        elif isinstance(
            result,
            str,
        ):
            text = result

        else:
            raise TypeError(
                "Monier-Williams acquisition service must "
                "return source text or structured records"
            )

        if not isinstance(text, str):
            raise TypeError(
                "Monier-Williams acquired source must "
                "be a string"
            )

        if not text.strip():
            raise ValueError(
                "Monier-Williams acquired source is empty"
            )

        # -----------------------------------------------------
        # Single parser authority.
        # -----------------------------------------------------

        parser = (
            self.parser
            if self.parser is not None
            else MonierWilliamsSourceParser()
        )

        parsed = parser.parse(text)

        if not isinstance(
            parsed,
            (tuple, list),
        ):
            raise TypeError(
                "Monier-Williams source parser must return "
                "a tuple or list"
            )

        records = tuple(parsed)

        for record in records:
            if not isinstance(
                record,
                (
                    MonierWilliamsSourceRecord,
                    MonierWilliamsRecord,
                ),
            ):
                raise TypeError(
                    "Monier-Williams parser returned "
                    "unsupported record type: "
                    f"{type(record).__name__}"
                )

        return records

    # =========================================================
    # Explicit SourceRecord -> AdapterRecord boundary
    # =========================================================

    def normalized_records(
        self,
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Convert acquisition-stage SourceRecords into
        normalized MonierWilliamsRecord objects.

        Existing MonierWilliamsRecord instances are preserved.

        This method is the explicit normalization boundary.
        """

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
