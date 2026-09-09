
from __future__ import annotations

"""
SanskritAI
==========

Delimited Monier-Williams Parser
--------------------------------

Parses controlled tabular Monier-Williams source data and converts
each source row into a normalized ``MonierWilliamsRecord``.

The parser belongs to the acquisition boundary.

It does not create DictionaryEntry or DictionarySense objects.

Version
-------
v0.6.x
"""

import csv
from io import StringIO
from typing import Iterator

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)

from .monier_williams_parser import MonierWilliamsParser


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
            raise TypeError(
                "delimiter must be a string"
            )

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
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Parse complete delimited Monier-Williams source text.

        Empty or whitespace-only source is treated as an empty
        collection.

        Parameters
        ----------
        source_text:
            Complete delimited source representation.

        Returns
        -------
        tuple[MonierWilliamsRecord, ...]
            Normalized Monier-Williams records.

        Raises
        ------
        TypeError
            If ``source_text`` is not a string.

        ValueError
            If the header or source rows are invalid.
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
    ) -> tuple[MonierWilliamsRecord, ...]:
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
    ) -> Iterator[MonierWilliamsRecord]:
        """
        Lazily parse source rows into normalized records.
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

            # Keep only recognized source fields.
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

            # ``raw_text`` is deliberately preserved only when
            # explicitly supplied by the source.
            #
            # We do NOT automatically copy the tab-delimited row
            # here because MonierWilliamsRecord.raw_text represents
            # an optional original source representation, whereas
            # this parser's primary responsibility is normalization.
            raw_text = values.get(
                "raw_text",
                "",
            )

            yield MonierWilliamsRecord(
                headword=headword,
                transliteration=values.get(
                    "transliteration",
                    "",
                ),
                definition=definition,
                grammatical_label=values.get(
                    "grammatical_label",
                    "",
                ),
                grammatical_category=values.get(
                    "grammatical_category",
                    "",
                ),
                source="monier-williams",
                source_id=values.get(
                    "source_id",
                    "",
                ),
                source_reference=values.get(
                    "source_reference",
                    "",
                ),
                raw_text=raw_text,
                homonym=values.get(
                    "homonym",
                    "",
                ),
            )

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

    @staticmethod
    def _normalize_header(
        value: str,
    ) -> str:
        """
        Normalize a source header name.
        """

        return value.strip().lower()
