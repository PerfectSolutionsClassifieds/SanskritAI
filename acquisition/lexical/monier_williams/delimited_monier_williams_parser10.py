
from __future__ import annotations

import csv
from io import StringIO
from typing import Iterable

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)

from .monier_williams_parser import MonierWilliamsParser


class DelimitedMonierWilliamsParser(MonierWilliamsParser):
    """
    Parser for delimited Monier-Williams dictionary data.

    The parser converts delimited rows into the domain-level
    MonierWilliamsRecord used by the Monier-Williams adapter/mapper layer.

    Supported formats include TSV and CSV through the configurable delimiter.

    Required columns:
        - headword
        - definition

    Optional columns:
        - transliteration
        - grammatical_label
        - grammatical_category
        - source
        - source_id
        - source_reference
        - raw_text
        - homonym
    """

    DEFAULT_DELIMITER = "\t"

    REQUIRED_COLUMNS = frozenset(
        {
            "headword",
            "definition",
        }
    )

    OPTIONAL_COLUMNS = frozenset(
        {
            "transliteration",
            "grammatical_label",
            "grammatical_category",
            "source",
            "source_id",
            "source_reference",
            "raw_text",
            "homonym",
        }
    )

    def __init__(
        self,
        delimiter: str = DEFAULT_DELIMITER,
        *,
        strict_headers: bool = True,
    ) -> None:
        if not delimiter:
            raise ValueError("delimiter must be non-empty")

        self.delimiter = delimiter
        self.strict_headers = strict_headers

    def parse(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Parse delimited source text into MonierWilliamsRecord objects.
        """
        if not isinstance(source_text, str):
            raise TypeError("source_text must be a string")

        if not source_text.strip():
            return ()

        reader = csv.DictReader(
            StringIO(source_text),
            delimiter=self.delimiter,
        )

        if reader.fieldnames is None:
            raise ValueError("Delimited source has no header row")

        headers = tuple(
            header.strip()
            for header in reader.fieldnames
            if header is not None
        )

        normalized_headers = {
            header.strip().lower()
            for header in headers
            if header.strip()
        }

        missing = self.REQUIRED_COLUMNS - normalized_headers
        if missing:
            raise ValueError(
                "Missing required columns: "
                + ", ".join(sorted(missing))
            )

        if self.strict_headers:
            allowed = self.REQUIRED_COLUMNS | self.OPTIONAL_COLUMNS
            unknown = normalized_headers - allowed

            if unknown:
                raise ValueError(
                    "Unknown columns: "
                    + ", ".join(sorted(unknown))
                )

        records: list[MonierWilliamsRecord] = []

        for row_number, row in enumerate(reader, start=2):
            values = self._normalize_row(row)

            headword = values.get("headword", "")
            definition = values.get("definition", "")

            if not headword:
                raise ValueError(
                    f"Missing headword at source row {row_number}"
                )

            if not definition:
                raise ValueError(
                    f"Missing definition at source row {row_number}"
                )

            raw_text = values.get("raw_text", "")

            if not raw_text:
                raw_text = self.delimiter.join(
                    values.get(header, "")
                    for header in headers
                )

            record = MonierWilliamsRecord(
                headword=headword,
                transliteration=values.get("transliteration", ""),
                definition=definition,
                grammatical_label=values.get(
                    "grammatical_label",
                    "",
                ),
                grammatical_category=values.get(
                    "grammatical_category",
                    "",
                ),
                source=values.get(
                    "source",
                    "monier-williams",
                )
                or "monier-williams",
                source_id=values.get("source_id", ""),
                source_reference=values.get(
                    "source_reference",
                    "",
                ),
                raw_text=raw_text,
                homonym=values.get("homonym", ""),
            )

            records.append(record)

        return tuple(records)

    def parse_lines(
        self,
        lines: Iterable[str],
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Parse an iterable of source lines.
        """
        return self.parse("".join(lines))

    def _normalize_row(
        self,
        row: dict[str | None, str | None],
    ) -> dict[str, str]:
        """
        Normalize CSV/TSV header and cell whitespace.
        """
        normalized: dict[str, str] = {}

        for key, value in row.items():
            if key is None:
                continue

            normalized_key = key.strip().lower()
            normalized_value = (
                value.strip()
                if isinstance(value, str)
                else ""
            )

            normalized[normalized_key] = normalized_value

        return normalized
