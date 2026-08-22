
from __future__ import annotations

from typing import Protocol

from .delimited_monier_williams_parser import (
    DelimitedMonierWilliamsParser,
)
from .monier_williams_source import MonierWilliamsSource
from .monier_williams_source_record import MonierWilliamsSourceRecord


class _Acquirer(Protocol):
    def acquire(self) -> str:
        ...


class MonierWilliamsSourceParser:
    """
    Acquisition + parsing boundary for Monier-Williams data.

    The parser accepts dependency injection so that:

        MonierWilliamsSourceParser(
            acquirer=source,
            parser=DelimitedMonierWilliamsParser(),
        )

    can be used in production and tests alike.
    """

    def __init__(
        self,
        acquirer: _Acquirer | MonierWilliamsSource,
        parser: DelimitedMonierWilliamsParser | None = None,
    ) -> None:
        if acquirer is None:
            raise TypeError("acquirer must not be None")

        self.acquirer = acquirer
        self.parser = (
            parser
            if parser is not None
            else DelimitedMonierWilliamsParser()
        )

    def acquire(self) -> str:
        return self.acquirer.acquire()

    def parse(
        self,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        raw = self.acquire()
        return self.parser.parse(raw)

    def parse_text(
        self,
        text: str,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        return self.parser.parse(text)

    def parse_lines(
        self,
        lines,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        return self.parser.parse_lines(lines)
