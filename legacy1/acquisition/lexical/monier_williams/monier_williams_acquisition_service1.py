
from __future__ import annotations

from .monier_williams_source import MonierWilliamsSource
from .monier_williams_source_record import MonierWilliamsSourceRecord


class MonierWilliamsAcquisitionService:
    """
    Coordinates acquisition of raw Monier-Williams source content.

    Parsing is intentionally delegated to MonierWilliamsSourceParser.
    """

    def __init__(
        self,
        source: MonierWilliamsSource,
    ) -> None:
        if source is None:
            raise TypeError("source must not be None")

        self.source = source

    def acquire(self) -> str:
        return self.source.acquire()

    def read(self) -> str:
        return self.acquire()

    @property
    def source_name(self) -> str:
        return self.source.source_name
