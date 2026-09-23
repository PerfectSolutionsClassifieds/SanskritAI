
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

    The pipeline orchestrates acquisition and parsing.

    It deliberately does not implement parsing logic itself.
    MonierWilliamsSourceParser is the single parsing authority.
    """

    service: MonierWilliamsAcquisitionService
    parser: MonierWilliamsSourceParser | None = None

    def run(
        self,
    ) -> MonierWilliamsAcquisitionResult | object:
        """
        Execute the configured acquisition service.

        This method preserves the existing acquisition-service API.
        """
        return self.service.acquire()

    def parse(
        self,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        """
        Acquire and parse the Monier-Williams source.
        """
        return self.records()

    def records(
        self,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        """
        Acquire source text and delegate parsing to
        MonierWilliamsSourceParser.

        The pipeline does not contain a second tagged-source parser.
        """
        source_text = self._read_source()

        parser = self.parser

        if parser is None:
            parser = MonierWilliamsSourceParser()

        records = parser.parse(source_text)

        if not isinstance(records, (tuple, list)):
            raise TypeError(
                "Monier-Williams parser must return "
                "a tuple or list of records"
            )

        source_records = tuple(records)

        if not all(
            isinstance(
                record,
                MonierWilliamsSourceRecord,
            )
            for record in source_records
        ):
            raise TypeError(
                "Monier-Williams source parser must return "
                "MonierWilliamsSourceRecord instances"
            )

        return source_records

    def _read_source(self) -> str:
        """
        Read raw source text directly from the acquisition service.

        Parsing belongs to this pipeline, not to the acquisition service.
        """
        source_text = self.service.read()

        if not isinstance(source_text, str):
            raise TypeError(
                "Monier-Williams acquisition service "
                "must return source text as str"
            )

        if not source_text.strip():
            raise ValueError(
                "Monier-Williams source is empty"
            )

        return source_text
