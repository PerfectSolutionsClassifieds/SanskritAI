from __future__ import annotations

import csv
from io import StringIO
from typing import Iterator

from .monier_williams_parser import MonierWilliamsParser
from .monier_williams_source_record import MonierWilliamsSourceRecord


class DelimitedMonierWilliamsParser(MonierWilliamsParser):
    """
    Parser for controlled tabular Monier-Williams source data.

    Required columns:
        headword
        definition

    Supported optional columns include:
        transliteration
        grammatical_label
        grammatical_category
        source_id
        source_reference
        raw_text
        homonym
    """

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
        "homonym",
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
            return ()

        return tuple(self.iter_parse(source_text))

    def parse_lines(
        self,
        lines: tuple[str, ...] | list[str],
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        return self.parse("\n".join(lines))

    def iter_parse(
        self,
        source_text: str,
    ) -> Iterator[MonierWilliamsSourceRecord]:

        if not isinstance(source_text, str):
            raise TypeError("source_text must be a string")

        if not source_text.strip():
            return

        reader = csv.reader(
            StringIO(source_text),
            delimiter=self.delimiter,
        )

        try:
            raw_header = next(reader)
        except StopIteration:
            return

        header = tuple(
            self._normalize_header(value)
            for value in raw_header
        )

        self._validate_header(header)

        known_columns = set(self.REQUIRED_COLUMNS) | set(
            self.OPTIONAL_COLUMNS
        )

        for sequence, row in enumerate(reader, start=1):

            if not row or not any(cell.strip() for cell in row):
                continue

            if len(row) != len(header):
                raise ValueError(
                    "Invalid column count at source row "
                    f"{sequence + 1}: expected {len(header)}, "
                    f"got {len(row)}"
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

            # raw_text is the source representation when supplied.
            # Otherwise preserve the complete row exactly as tabular data.
            raw_text = values.get("raw_text", "")
            if not raw_text:
                raw_text = self.delimiter.join(row)

            fields = {
                key: value
                for key, value in values.items()
                if key in known_columns
            }

            yield MonierWilliamsSourceRecord(
                sequence=sequence,
                raw_text=raw_text,
                fields=fields,
            )

    def _validate_header(
        self,
        header: tuple[str, ...],
    ) -> None:

        if not header:
            raise ValueError(
                "Monier-Williams source contains no header"
            )

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

        if self.strict_headers:
            known = set(self.REQUIRED_COLUMNS) | set(
                self.OPTIONAL_COLUMNS
            )

            unknown = [
                column
                for column in header
                if column not in known
            ]

            if unknown:
                raise ValueError(
                    "Unknown Monier-Williams header(s): "
                    + ", ".join(unknown)
                )

    @staticmethod
    def _normalize_header(value: str) -> str:
        return value.strip().lower()
