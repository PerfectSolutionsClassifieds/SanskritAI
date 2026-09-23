
from __future__ import annotations

"""
SanskritAI
==========

Delimited Monier-Williams Parser
---------------------------------

Parser for controlled tabular MW representations.

Required:
    headword
    definition

Optional:
    transliteration
    grammatical_label
    grammatical_category
    source_id
    source_reference
    raw_text

The parser remains acquisition-oriented and does not create
canonical lexical entities.
"""

import csv
from io import StringIO
from typing import Iterator

from .monier_williams_parser import MonierWilliamsParser
from .monier_williams_source_record import MonierWilliamsSourceRecord


class DelimitedMonierWilliamsParser(MonierWilliamsParser):

    DEFAULT_DELIMITER = "\t"

    REQUIRED_COLUMNS = (
        "headword",
        "definition",
    )

    OPTIONAL_COLUMNS = (
        "transliteration",
        "grammatical_label",
        "grammatical_category",
        "source_id",
        "source_reference",
        "raw_text",
    )

    def __init__(
        self,
        *,
        delimiter: str = DEFAULT_DELIMITER,
        strict_headers: bool = True,
    ) -> None:
        if not isinstance(delimiter, str):
            raise TypeError("delimiter must be a string")

        if len(delimiter) != 1:
            raise ValueError(
                "delimiter must contain exactly one character"
            )

        self.delimiter = delimiter
        self.strict_headers = strict_headers

    def parse(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:

        if not isinstance(source_text, str):
            raise TypeError("source_text must be a string")

        if not source_text.strip():
            raise ValueError(
                "Monier-Williams source is empty"
            )

        return tuple(self.iter_parse(source_text))

    def iter_parse(
        self,
        source_text: str,
    ) -> Iterator[MonierWilliamsSourceRecord]:

        if not isinstance(source_text, str):
            raise TypeError("source_text must be a string")

        if not source_text.strip():
            raise ValueError(
                "Monier-Williams source is empty"
            )

        reader = csv.reader(
            StringIO(source_text),
            delimiter=self.delimiter,
        )

        try:
            raw_header = next(reader)
        except StopIteration:
            raise ValueError(
                "Monier-Williams source contains no header"
            )

        header = tuple(
            item.strip()
            for item in raw_header
        )

        if not header or all(not item for item in header):
            raise ValueError(
                "Monier-Williams source requires a header"
            )

        self._validate_header(header)

        for sequence, row in enumerate(reader, start=1):

            if not row or all(not value.strip() for value in row):
                continue

            if len(row) != len(header):
                raise ValueError(
                    "Invalid Monier-Williams row "
                    f"{sequence + 1}: expected {len(header)} "
                    f"columns, received {len(row)}"
                )

            values = {
                header[index]: row[index].strip()
                for index in range(len(header))
            }

            headword = values.get("headword", "")
            definition = values.get("definition", "")

            if not headword:
                raise ValueError(
                    f"Missing headword at source row {sequence + 1}"
                )

            if not definition:
                raise ValueError(
                    f"Missing definition at source row {sequence + 1}"
                )

            if "grammatical_category" in values:
                values["grammatical_label"] = values[
                    "grammatical_category"
                ]

            if "grammatical_label" in values:
                values["grammatical_category"] = values[
                    "grammatical_label"
                ]

            if "source_reference" in values:
                values["source_id"] = values[
                    "source_reference"
                ]

            if "source_id" in values:
                values["source_reference"] = values[
                    "source_id"
                ]

            yield MonierWilliamsSourceRecord(
                sequence=sequence,
                raw_text=self.delimiter.join(row),
                fields=values,
            )

    def parse_lines(self, lines):
        return self.parse(
            "\n".join(lines)
        )

    def _validate_header(
        self,
        header: tuple[str, ...],
    ) -> None:

        missing = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in header
        ]

        if missing:
            raise ValueError(
                "Missing required columns: "
                + ", ".join(missing)
            )

        if not self.strict_headers:
            return

        known = set(self.REQUIRED_COLUMNS) | set(
            self.OPTIONAL_COLUMNS
        )

        unknown = [
            item
            for item in header
            if item not in known
        ]

        if unknown:
            raise ValueError(
                "Unknown Monier-Williams header(s): "
                + ", ".join(unknown)
            )
