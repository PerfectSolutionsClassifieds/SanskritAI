
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Parser
-----------------------------

Deterministic parser for the Cologne-style MW source representation.

A source record begins with <L> and terminates with <LEND>.

Example
-------

<L>1
<k1>rAma
<e>pleasing
<LEND>

The parser preserves all source fields and unknown tags.
"""

import re
from typing import Iterable

from .monier_williams_source_record import (
    MonierWilliamsSourceRecord,
)
from .monier_williams_parser import MonierWilliamsParser
from .delimited_monier_williams_parser import (
    DelimitedMonierWilliamsParser,
)


class MonierWilliamsSourceParser:

    RECORD_START = "<L>"
    RECORD_END = "<LEND>"

    FIELD_PATTERN = re.compile(
        r"<(?P<tag>[A-Za-z0-9_]+)>(?P<value>[^<]*)"
    )

    def __init__(
        self,
        acquirer=None,
        parser: MonierWilliamsParser | None = None,
    ) -> None:
        self.acquirer = acquirer
        self.parser = parser or DelimitedMonierWilliamsParser()

    def parse(self, source_text: str):
        if not isinstance(source_text, str):
            raise TypeError("source_text must be a string")

        if not source_text.strip():
            raise ValueError(
                "Monier-Williams source is empty"
            )

        if self.RECORD_START not in source_text:
            # Permit the controlled delimited acquisition format.
            return self.parser.parse(source_text)

        records = []
        current: list[str] | None = None

        for line in source_text.splitlines():

            stripped = line.rstrip()

            if stripped.startswith(self.RECORD_START):
                if current is not None:
                    raise ValueError(
                        "Unterminated Monier-Williams record"
                    )

                current = [stripped]
                continue

            if stripped.strip() == self.RECORD_END:
                if current is None:
                    raise ValueError(
                        "Orphan <LEND> in Monier-Williams source"
                    )

                current.append(stripped)

                records.append(
                    self._parse_record(
                        len(records) + 1,
                        current,
                    )
                )

                current = None
                continue

            if current is not None:
                current.append(stripped)

        if current is not None:
            raise ValueError(
                "Unterminated Monier-Williams record"
            )

        if not records:
            raise ValueError(
                "Monier-Williams source contains no records"
            )

        return tuple(records)

    def parse_lines(self, lines: Iterable[str]):
        return self.parse("\n".join(lines))

    def parse_record(self, source_text: str):
        records = self.parse(source_text)

        if len(records) != 1:
            raise ValueError(
                "Expected exactly one Monier-Williams record"
            )

        return records[0]

    def acquire_and_parse(self):
        if self.acquirer is None:
            raise ValueError(
                "No Monier-Williams acquirer configured"
            )

        if hasattr(self.acquirer, "acquire"):
            source_text = self.acquirer.acquire()
        elif hasattr(self.acquirer, "read"):
            source_text = self.acquirer.read()
        else:
            raise TypeError(
                "acquirer must provide acquire() or read()"
            )

        return self.parse(source_text)

    def _parse_record(
        self,
        sequence: int,
        lines: list[str],
    ) -> MonierWilliamsSourceRecord:

        raw_text = "\n".join(lines)

        fields: dict[str, str] = {}

        for line in lines:
            for match in self.FIELD_PATTERN.finditer(line):
                tag = match.group("tag")
                value = match.group("value").strip()

                if tag == "LEND":
                    continue

                if tag in fields and value:
                    fields[tag] = (
                        fields[tag] + " " + value
                    ).strip()
                else:
                    fields[tag] = value

        if "L" not in fields:
            raise ValueError(
                "Monier-Williams record is missing <L>"
            )

        if not fields.get("k1") and not fields.get("k2"):
            raise ValueError(
                "Monier-Williams record has no headword"
            )

        return MonierWilliamsSourceRecord(
            sequence=sequence,
            raw_text=raw_text,
            fields=fields,
        )
