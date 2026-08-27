
from __future__ import annotations

from dataclasses import dataclass

from .monier_williams_source_record import (
    MonierWilliamsSourceRecord,
)


@dataclass(slots=True)
class MonierWilliamsSourceParser:
    """
    Parser for the original Monier-Williams tagged source
    representation.

    The parser can consume source content directly or obtain it
    through an injected acquisition source.

    The acquisition boundary supports both:

        source.acquire()

    and:

        source.read()

    for compatibility with existing implementations.
    """

    acquirer: object | None = None
    parser: object | None = None

    def __post_init__(self) -> None:
        if self.parser is None:
            self.parser = _TaggedMonierWilliamsParser()

    def parse(
        self,
        source_text: str | None = None,
    ):
        """
        Parse supplied source text or acquire it from the configured
        source.
        """
        if source_text is None:

            if self.acquirer is None:
                raise ValueError(
                    "No source text or acquisition source supplied"
                )

            # Prefer acquire() because it is the stable compatibility
            # acquisition boundary and is implemented by lightweight
            # test doubles.
            acquire = getattr(
                self.acquirer,
                "acquire",
                None,
            )

            if callable(acquire):
                source_text = acquire()

            else:
                read = getattr(
                    self.acquirer,
                    "read",
                    None,
                )

                if callable(read):
                    source_text = read()

                else:
                    raise TypeError(
                        "acquirer must provide read() or acquire()"
                    )

        if not isinstance(source_text, str):
            raise TypeError(
                "source_text must be a string"
            )

        parser = self.parser

        if parser is None:
            raise RuntimeError(
                "MonierWilliamsSourceParser has no parser"
            )

        return parser.parse(source_text)

    def parse_record(
        self,
        source_text: str,
    ) -> MonierWilliamsSourceRecord:
        """
        Parse exactly one Monier-Williams record.
        """
        records = self.parse(source_text)

        if len(records) != 1:
            raise ValueError(
                "parse_record requires exactly one record"
            )

        return records[0]


class _TaggedMonierWilliamsParser:
    """Internal parser for MW tagged source records."""

    START = "<L>"
    END = "<LEND>"

    def parse(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:

        if not isinstance(source_text, str):
            raise TypeError(
                "source_text must be a string"
            )

        if not source_text.strip():
            raise ValueError(
                "Monier-Williams source is empty"
            )

        records: list[MonierWilliamsSourceRecord] = []
        current: list[str] = []
        inside = False

        for line in source_text.splitlines():

            stripped = line.strip()

            if not stripped:
                if inside:
                    current.append(line)
                continue

            if stripped == self.END:

                if not inside:
                    raise ValueError(
                        "Orphan <LEND> encountered"
                    )

                current.append(line)

                records.append(
                    self._build_record(
                        len(records) + 1,
                        current,
                    )
                )

                current = []
                inside = False
                continue

            if stripped.startswith(self.START):

                if inside:
                    raise ValueError(
                        "Unterminated MW record before next <L>"
                    )

                inside = True
                current = [line]
                continue

            if not inside:
                raise ValueError(
                    "Source content encountered outside "
                    "an MW record"
                )

            current.append(line)

        if inside:
            raise ValueError(
                "Unterminated Monier-Williams record"
            )

        if not records:
            raise ValueError(
                "Monier-Williams source contains no records"
            )

        return tuple(records)

    def _build_record(
        self,
        sequence: int,
        lines: list[str],
    ) -> MonierWilliamsSourceRecord:

        raw_text = "\n".join(lines)

        fields: dict[str, str] = {}

        for line in lines:

            stripped = line.strip()

            if not stripped.startswith("<"):
                continue

            close = stripped.find(">")

            if close <= 1:
                continue

            key = stripped[1:close]
            value = stripped[close + 1:].strip()

            fields[key] = value

        # Canonical convenience aliases.
        if "k1" in fields:
            fields["headword"] = fields["k1"]

        if "e" in fields:
            fields["definition"] = fields["e"]

        if "L" in fields:
            fields["homonym"] = fields["L"]

        return MonierWilliamsSourceRecord(
            sequence=sequence,
            raw_text=raw_text,
            fields=fields,
        )
