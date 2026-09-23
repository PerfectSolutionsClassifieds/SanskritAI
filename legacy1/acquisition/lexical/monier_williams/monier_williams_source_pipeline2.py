
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Pipeline
--------------------------------

Acquisition
    ↓
Raw source
    ↓
Source parser
    ↓
Source records

No canonical repository mutation occurs here.
"""

from .monier_williams_acquisition_service import (
    MonierWilliamsAcquisitionService,
)
from .monier_williams_source_parser import (
    MonierWilliamsSourceParser,
)


class MonierWilliamsSourcePipeline:

    def __init__(
        self,
        acquisition_service: MonierWilliamsAcquisitionService,
        parser: MonierWilliamsSourceParser | None = None,
    ) -> None:
        self.acquisition_service = acquisition_service
        self.parser = parser or MonierWilliamsSourceParser()

    def acquire(self) -> str:
        return self.acquisition_service.acquire()

    def parse(self):
        source_text = self.acquire()
        return self.parser.parse(source_text)

    def run(self):
        return self.parse()

    def parse_record(self, source_text: str):
        return self.parser.parse_record(source_text)
