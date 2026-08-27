
from __future__ import annotations

import csv
from io import StringIO
from typing import Iterator

from .monier_williams_parser import MonierWilliamsParser
from .monier_williams_source_record import MonierWilliamsSourceRecord


class DelimitedMonierWilliamsParser(MonierWilliamsParser):
    """
    Parser for controlled tabular Monier-Williams source data.

    Required columns
    ----------------
    headword
    definition

    Supported optional columns
    --------------------------
    transliteration
    grammatical_label
    grammatical_category
    source_id
    source_reference
    raw_text
    homonym

    Empty or whitespace-only source is treated as an empty dataset and
    returns an empty tuple.

    Unknown headers are rejected by default when ``strict_headers=True``.
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

        if not isinstance(strict_headers, bool):
            raise TypeError(
                "strict_headers must be a boolean"
            )

        self.delimiter = delimiter
        self.strict_headers = strict_headers

    def parse(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        """
        Parse complete Monier-Williams delimited source text.

        Empty or whitespace-only input returns an empty tuple.
        """
        if not isinstance(source_text, str):
            raise TypeError(
                "source_text must be a string"
            )

        if not source_text.strip():
            return ()

        return tuple(self.iter_parse(source_text))

    def parse_lines(
        self,
        lines: tuple[str, ...] | list[str],
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        """
        Parse an iterable of source lines.

        ``None`` is rejected explicitly so callers receive a useful
        contract-level error instead of the lower-level ``join()``
        exception.
        """
        if lines is None:
            raise TypeError(
                "lines must not be None"
            )

        if not isinstance(lines, (tuple, list)):
            raise TypeError(
                "lines must be a tuple or list of strings"
            )

        if not all(isinstance(line, str) for line in lines):
            raise TypeError(
                "lines must contain only strings"
            )

        return self.parse("\n".join(lines))

    def iter_parse(
        self,
        source_text: str,
    ) -> Iterator[MonierWilliamsSourceRecord]:
        """
        Lazily parse source text into Monier-Williams source records.
        """
        if not isinstance(source_text, str):
            raise TypeError(
                "source_text must be a string"
            )

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

        known_columns = (
            set(self.REQUIRED_COLUMNS)
            | set(self.OPTIONAL_COLUMNS)
        )

        for sequence, row in enumerate(reader, start=1):

            # Ignore completely empty rows.
            if not row or not any(
                cell.strip() for cell in row
            ):
                continue

            if len(row) != len(header):
                raise ValueError(
                    "Invalid column count at source row "
                    f"{sequence + 1}: expected "
                    f"{len(header)}, got {len(row)}"
                )

            values = {
                header[index]: row[index].strip()
                for index in range(len(header))
            }

            headword = values.get("headword", "")
            definition = values.get("definition", "")

            if not headword:
                raise ValueError(
                    f"Missing headword at source row "
                    f"{sequence + 1}"
                )

            if not definition:
                raise ValueError(
                    f"Missing definition at source row "
                    f"{sequence + 1}"
                )

            # Preserve explicitly supplied raw_text.
            #
            # If raw_text is not supplied, the canonical source record
            # should expose an empty raw_text rather than silently
            # manufacturing one from the tabular row.
            raw_text = values.get("raw_text", "")

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
        """
        Validate required and optional header columns.
        """
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
            known = (
                set(self.REQUIRED_COLUMNS)
                | set(self.OPTIONAL_COLUMNS)
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
        """Normalize a source header."""
        return value.strip().lower()
