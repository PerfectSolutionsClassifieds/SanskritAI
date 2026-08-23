
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Raw Record Parser

Parses the structural boundaries of MW records.

This parser deliberately performs NO semantic interpretation.

It only identifies:
    <L> ... <LEND>

and extracts basic header fields.

The parser must preserve the original source text.
"""

import re
from collections.abc import Iterable, Iterator

from SanskritAI.lexical.monier_williams.record import (
    MonierWilliamsRecord,
)


_FIELD_PATTERN = re.compile(
    r"<(?P<tag>[A-Za-z0-9_]+)>(?P<value>[^<\r\n]*)"
)


class MonierWilliamsParser:
    """
    Deterministic parser for raw MW records.
    """

    START_MARKER = "<L>"
    END_MARKER = "<LEND>"

    def parse(
        self,
        lines: Iterable[str],
    ) -> Iterator[MonierWilliamsRecord]:
        """
        Parse an MW source stream into records.
        """

        current: list[str] = []

        for line in lines:
            line = line.rstrip("\r\n")

            if line.startswith(self.START_MARKER):
                if current:
                    yield self._build_record(current)

                current = [line]
                continue

            if current:
                current.append(line)

                if self.END_MARKER in line:
                    yield self._build_record(current)
                    current = []

        if current:
            yield self._build_record(current)

    def _build_record(
        self,
        lines: list[str],
    ) -> MonierWilliamsRecord:
        """
        Construct one record while preserving raw source text.
        """

        header = lines[0]

        fields = {
            match.group("tag"): match.group("value")
            for match in _FIELD_PATTERN.finditer(header)
        }

        return MonierWilliamsRecord(
            line_id=fields.get("L"),
            page=fields.get("pc"),
            key1=fields.get("k1"),
            key2=fields.get("k2"),
            homonym=fields.get("h"),
            entry_number=fields.get("e"),
            body=lines[1:],
            raw_text="\n".join(lines),
        )
