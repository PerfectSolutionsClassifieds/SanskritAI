
from __future__ import annotations

"""
SanskritAI
==========

Delimited Monier-Williams Parser
--------------------------------

Parses controlled tabular Monier-Williams source data into
``MonierWilliamsSourceRecord`` objects.

Architectural boundary
----------------------

Raw MW source
    ↓
DelimitedMonierWilliamsParser
    ↓
MonierWilliamsSourceRecord
    ↓
MonierWilliamsAdapter
    ↓
MonierWilliamsRecord
    ↓
MonierWilliamsMapper
    ↓
CanonicalDictionaryEntry / CanonicalDictionarySense

The acquisition parser must not construct domain adapter records.
It preserves source-oriented information and leaves domain
normalization to the adapter boundary.

Version
-------
v0.7.0
"""

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

    Parameters
    ----------
    delimiter:
        Single-character delimiter used by the source.

    strict_headers:
        When True, unknown columns cause ``ValueError``.
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

    # =========================================================
    # Public parsing
    # =========================================================

    def parse(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        """
        Parse complete delimited Monier-Williams source text.

        Returns
        -------
        tuple[MonierWilliamsSourceRecord, ...]
            Acquisition-stage source records.
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
        Parse a collection of source lines.
        """

        if not isinstance(lines, (tuple, list)):
            raise TypeError(
                "lines must be a tuple or list of strings"
            )

        return self.parse(
            "\n".join(lines)
        )

    def iter_parse(
        self,
        source_text: str,
    ) -> Iterator[MonierWilliamsSourceRecord]:
        """
        Lazily parse source rows into acquisition records.
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
            # Ignore completely blank rows.
            if not row or not any(
                cell.strip()
                for cell in row
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

            # Preserve only recognized source fields.
            values = {
                key: value
                for key, value in values.items()
                if key in known_columns
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

            # raw_text is preserved only when explicitly
            # supplied by the source.
            raw_text = values.get(
                "raw_text",
                "",
            )

            fields = {
                "headword": headword,
                "transliteration": values.get(
                    "transliteration",
                    "",
                ),
                "definition": definition,
                "grammatical_label": values.get(
                    "grammatical_label",
                    "",
                ),
                "grammatical_category": values.get(
                    "grammatical_category",
                    "",
                ),
                "source": "monier-williams",
                "source_id": values.get(
                    "source_id",
                    "",
                ),
                "source_reference": values.get(
                    "source_reference",
                    "",
                ),
                "raw_text": raw_text,
                "homonym": values.get(
                    "homonym",
                    "",
                ),
            }

            yield MonierWilliamsSourceRecord(
                sequence=sequence,
                raw_text=(
                    raw_text
                    if raw_text
                    else "\t".join(
                        values.get(column, "")
                        for column in header
                    )
                ),
                fields=fields,
            )

    # =========================================================
    # Header validation
    # =========================================================

    def _validate_header(
        self,
        header: tuple[str, ...],
    ) -> None:
        """
        Validate source header.
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

    # =========================================================
    # Header normalization
    # =========================================================

    @staticmethod
    def _normalize_header(
        value: str,
    ) -> str:
        """
        Normalize a source header name.
        """

        return value.strip().lower()
