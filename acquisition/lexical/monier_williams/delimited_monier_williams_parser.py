from __future__ import annotations

"""
SanskritAI
==========

Delimited Monier-Williams Parser
---------------------------------

Parses a controlled tabular representation of MW records.

Expected columns:

    headword
    transliteration
    definition
    grammatical_label
    source_id
    raw_text

The parser accepts TSV by default but also supports another
delimiter.

This is an acquisition-stage parser, not a linguistic parser.
"""

import csv
from io import StringIO

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)

from .monier_williams_parser import MonierWilliamsParser


class DelimitedMonierWilliamsParser(MonierWilliamsParser):
    """
    Parse tabular Monier-Williams source data.
    """

    DEFAULT_DELIMITER = "\t"

    REQUIRED_COLUMNS = (
        "headword",
        "definition",
    )

    OPTIONAL_COLUMNS = (
        "transliteration",
        "grammatical_label",
        "source_id",
        "raw_text",
    )

    def __init__(
        self,
        *,
        delimiter: str = DEFAULT_DELIMITER,
    ) -> None:
        if not isinstance(delimiter, str):
            raise TypeError("delimiter must be a string")

        if len(delimiter) != 1:
            raise ValueError(
                "delimiter must contain exactly one character"
            )

        self.delimiter = delimiter

    def parse(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsRecord, ...]:
        if not isinstance(source_text, str):
            raise TypeError("source_text must be a string")

        if not source_text.strip():
            return ()

        reader = csv.DictReader(
            StringIO(source_text),
            delimiter=self.delimiter,
        )

        if reader.fieldnames is None:
            raise ValueError(
                "Monier-Williams source contains no header"
            )

        fieldnames = tuple(
            name.strip()
            for name in reader.fieldnames
            if name is not None
        )

        missing = tuple(
            column
            for column in self.REQUIRED_COLUMNS
            if column not in fieldnames
        )

        if missing:
            raise ValueError(
                "Missing required columns: "
                + ", ".join(missing)
            )

        records: list[MonierWilliamsRecord] = []

        for row_number, row in enumerate(
            reader,
            start=2,
        ):
            headword = self._value(
                row,
                "headword",
            )

            definition = self._value(
                row,
                "definition",
            )

            if not headword:
                raise ValueError(
                    f"Missing headword at source row {row_number}"
                )

            if not definition:
                raise ValueError(
                    f"Missing definition at source row {row_number}"
                )

            records.append(
                MonierWilliamsRecord(
                    headword=headword,
                    transliteration=self._value(
                        row,
                        "transliteration",
                    ),
                    definition=definition,
                    grammatical_label=self._value(
                        row,
                        "grammatical_label",
                    ),
                    source=self.SOURCE,
                    source_id=self._value(
                        row,
                        "source_id",
                    ),
                    raw_text=self._value(
                        row,
                        "raw_text",
                    ),
                )
            )

        return tuple(records)

    @staticmethod
    def _value(
        row: dict[str, str | None],
        column: str,
    ) -> str:
        value = row.get(column)

        if value is None:
            return ""

        return value.strip()
