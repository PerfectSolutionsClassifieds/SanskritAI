
from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from typing import Iterable

from .monier_williams_source_record import MonierWilliamsSourceRecord


@dataclass(frozen=True)
class DelimitedMonierWilliamsParserConfig:
    delimiter: str = "\t"

    required_headers: tuple[str, ...] = (
        "headword",
        "definition",
    )

    optional_headers: tuple[str, ...] = (
        "transliteration",
        "grammatical_label",
        "source_id",
        "raw_text",
    )

    strict_headers: bool = False


class DelimitedMonierWilliamsParser:
    """
    Parser for a normalized delimited Monier-Williams source format.

    The parser deliberately accepts a small canonical header vocabulary,
    while permitting additional source-specific columns. Unknown columns
    are therefore preserved rather than rejected.

    Public compatibility:
        - delimiter=...
        - parse(...)
        - parse_lines(...)
        - empty input -> ()
        - header validation
    """

    def __init__(
        self,
        delimiter: str = "\t",
        *,
        config: DelimitedMonierWilliamsParserConfig | None = None,
    ) -> None:
        if not delimiter:
            raise ValueError("delimiter must not be empty")

        if config is None:
            config = DelimitedMonierWilliamsParserConfig(
                delimiter=delimiter,
            )
        else:
            delimiter = config.delimiter

        if not delimiter:
            raise ValueError("delimiter must not be empty")

        self.config = config
        self.delimiter = delimiter

    def parse(
        self,
        text: str,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        if text is None:
            raise TypeError("text must not be None")

        if not text.strip():
            return ()

        reader = csv.reader(
            io.StringIO(text),
            delimiter=self.delimiter,
        )

        rows = list(reader)

        if not rows:
            return ()

        header = tuple(
            self._normalize_header(value)
            for value in rows[0]
        )

        self._validate_header(header)

        records: list[MonierWilliamsSourceRecord] = []

        for row in rows[1:]:
            if not row or not any(cell.strip() for cell in row):
                continue

            values = list(row)

            if len(values) < len(header):
                values.extend([""] * (len(header) - len(values)))

            if len(values) > len(header):
                values = values[: len(header)]

            data = dict(zip(header, values))

            records.append(
                MonierWilliamsSourceRecord(
                    headword=data.get("headword", "").strip(),
                    transliteration=data.get(
                        "transliteration",
                        "",
                    ).strip(),
                    definition=data.get(
                        "definition",
                        "",
                    ).strip(),
                    grammatical_label=data.get(
                        "grammatical_label",
                        "",
                    ).strip(),
                    source_id=data.get(
                        "source_id",
                        "",
                    ).strip(),
                    raw_text=data.get(
                        "raw_text",
                        "",
                    ).strip(),
                )
            )

        return tuple(records)

    def parse_lines(
        self,
        lines: Iterable[str],
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        if lines is None:
            raise TypeError("lines must not be None")

        return self.parse(
            "\n".join(lines)
        )

    def _normalize_header(self, value: str) -> str:
        return value.strip().lower()

    def _validate_header(
        self,
        header: tuple[str, ...],
    ) -> None:
        if not header:
            raise ValueError(
                "Monier-Williams source requires a header"
            )

        missing = [
            required
            for required in self.config.required_headers
            if required not in header
        ]

        if missing:
            raise ValueError(
                "Monier-Williams source is missing required "
                f"header(s): {', '.join(missing)}"
            )

        if self.config.strict_headers:
            known = (
                set(self.config.required_headers)
                | set(self.config.optional_headers)
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
