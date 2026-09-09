from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence, Tuple, Union

from .monier_williams_acquisition_result import (
    MonierWilliamsAcquisitionResult,
)
from .monier_williams_acquisition_service import (
    MonierWilliamsAcquisitionService,
)
from .monier_williams_source_record import MonierWilliamsSourceRecord

try:
    from .monier_williams_source_parser import MonierWilliamsSourceParser
except ImportError:
    MonierWilliamsSourceParser = None  # type: ignore


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
    parser: object | None = None

    def run(
        self,
    ) -> MonierWilliamsAcquisitionResult | Sequence[MonierWilliamsSourceRecord] | Tuple[MonierWilliamsSourceRecord, ...]:
        """Execute the acquisition step via the configured service."""
        return self.service.acquire()

    def parse(self) -> tuple[MonierWilliamsSourceRecord, ...] | list[MonierWilliamsSourceRecord]:
        """Parse acquired source content into structured MonierWilliamsSourceRecord instances."""
        return self.records()

    def records(self) -> tuple[MonierWilliamsSourceRecord, ...]:
        """Retrieve and parse acquired source records into a tuple."""
        result = self.run()

        # If result is already a collection of records
        if isinstance(result, (tuple, list)) and all(
            isinstance(r, MonierWilliamsSourceRecord) for r in result
        ):
            return tuple(result)

        # Extract text from MonierWilliamsAcquisitionResult or string
        if isinstance(result, MonierWilliamsAcquisitionResult):
            text = result.text
        elif isinstance(result, str):
            text = result
        else:
            text = str(result)

        # Delegate to MonierWilliamsSourceParser if configured or available
        parser = self.parser or (
            MonierWilliamsSourceParser()
            if MonierWilliamsSourceParser is not None
            else None
        )
        if parser is not None and hasattr(parser, "parse"):
            parsed = parser.parse(text)
            if isinstance(parsed, (tuple, list)):
                return tuple(parsed)

        # Fallback parsing for <L>...<LEND> blocks
        return self._parse_raw_text(text)

    @staticmethod
    def _parse_raw_text(text: str) -> tuple[MonierWilliamsSourceRecord, ...]:
        records: list[MonierWilliamsSourceRecord] = []
        blocks = re.findall(r"<L>(.*?)</LEND>", text, re.DOTALL)

        for idx, block in enumerate(blocks, start=1):
            raw_text = f"<L>{block}</LEND>"
            lines = [
                line.strip()
                for line in block.strip().splitlines()
                if line.strip()
            ]
            fields: dict[str, str] = {}
            seq = idx

            for line in lines:
                if line.isdigit():
                    fields["L"] = line
                    seq = int(line)
                elif line.startswith("<") and ">" in line:
                    tag = line[1 : line.index(">")]
                    val = line[line.index(">") + 1 :]
                    fields[tag] = val
                    if tag == "L" and val.isdigit():
                        seq = int(val)

            records.append(
                MonierWilliamsSourceRecord(
                    sequence=seq,
                    raw_text=raw_text,
                    fields=fields,
                )
            )

        return tuple(records)
