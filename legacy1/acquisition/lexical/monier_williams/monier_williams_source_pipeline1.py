
from __future__ import annotations

from .monier_williams_acquisition_service import (
    MonierWilliamsAcquisitionService,
)
from .monier_williams_source_parser import (
    MonierWilliamsSourceParser,
)


class MonierWilliamsSourcePipeline:
    """
    Acquisition → parsing pipeline.

    This remains below the domain layer and therefore does not know about
    DictionaryEntry, DictionarySense, repositories, or services.
    """

    def __init__(
        self,
        acquisition_service: MonierWilliamsAcquisitionService,
        parser: MonierWilliamsSourceParser | None = None,
    ) -> None:
        self._acquisition_service = acquisition_service
        self._parser = (
            parser
            if parser is not None
            else MonierWilliamsSourceParser()
        )

    @property
    def acquisition_service(
        self,
    ) -> MonierWilliamsAcquisitionService:
        return self._acquisition_service

    @property
    def parser(self) -> MonierWilliamsSourceParser:
        return self._parser

    def parse(self):
        result = self._acquisition_service.acquire()
        return self._parser.parse(result.text)
