
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

    Empty input is treated as an empty source and returns ``()``.
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
        Parse complete delimited Monier-Williams source text.

        Empty or whitespace-only input returns an empty tuple.
        """
        if not isinstance(source_text, str):
            raise TypeError(
                "source_text must be a string"
            )

        if not source_text.strip():
            return ()

        return tuple(
            self.iter_parse(source_text)
        )

    def parse_lines(
        self,
        lines: tuple[str, ...] | list[str],
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        """
        Parse a sequence of source lines.
        """
        if lines is None:
            raise TypeError(
                "lines must not be None"
            )

        if not isinstance(lines, (tuple, list)):
            raise TypeError(
                "lines must be a list or tuple"
            )

        return self.parse(
            "\n".join(lines)
        )

    def iter_parse(
        self,
        source_text: str,
    ) -> Iterator[MonierWilliamsSourceRecord]:
        """
        Lazily parse delimited source text.
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

        for sequence, row in enumerate(
            reader,
            start=1,
        ):
            if (
                not row
                or not any(
                    cell.strip()
                    for cell in row
                )
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

            headword = values.get(
                "headword",
                "",
            )

            definition = values.get(
                "definition",
                "",
            )

            if not headword:
                raise ValueError(
                    "Missing headword at source row "
                    f"{sequence + 1}"
                )

            if not definition:
                raise ValueError(
                    "Missing definition at source row "
                    f"{sequence + 1}"
                )

            fields = {
                key: value
                for key, value in values.items()
                if key in known_columns
            }

            # ``raw_text`` is a semantic field in the MW record.
            #
            # If explicitly supplied, preserve it.
            # Otherwise leave it empty. The source record's
            # raw_text is intentionally distinct from the
            # physical TSV row.
            raw_text = values.get(
                "raw_text",
                "",
            )

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
    def _normalize_header(
        value: str,
    ) -> str:
        return value.strip().lower()
