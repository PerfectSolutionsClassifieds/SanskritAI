from __future__ import annotations

from dataclasses import dataclass

from .monier_williams_acquisition_service import (
    MonierWilliamsAcquisitionService,
)
from .monier_williams_source_record import MonierWilliamsSourceRecord


@dataclass(frozen=True, slots=True)
class MonierWilliamsSourcePipeline:
    """
    Acquisition-stage pipeline.

    Source
      ↓
    Acquisition Service
      ↓
    Source Parser
      ↓
    Raw MW Source Records
    """

    service: MonierWilliamsAcquisitionService

    def run(self):
        return self.service.acquire()

    def records(self) -> tuple[MonierWilliamsSourceRecord, ...]:
        result = self.run()

        if isinstance(result, tuple):
            return result

        return tuple(result)
