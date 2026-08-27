
from __future__ import annotations

from dataclasses import dataclass

from .delimited_monier_williams_parser import (
    DelimitedMonierWilliamsParser,
)
from .monier_williams_source_record import (
    MonierWilliamsSourceRecord,
)


@dataclass(slots=True)
class MonierWilliamsSourceParser:
    """
    Unified parser for Monier-Williams source representations.

    Supported source formats
    ------------------------
    1. Original tagged MW representation::

           <L>1
           <k1>rAma
           <e>pleasing
           <LEND>

    2. Canonical delimited representation::

           headword    definition
           rāma        pleasing

    The parser supports:

    * direct source text
    * injected acquisition sources
    * injected custom parsers
    * ``read()`` based sources
    * ``acquire()`` based sources
    """

    acquirer: object | None = None
    parser: object | None = None

    def __post_init__(self) -> None:
        # Do not eagerly select a concrete parser when none was
        # injected. The source representation is determined when
        # parse() receives the actual source text.
        pass

    def parse(
        self,
        source_text: str | None = None,
    ):
        """
        Parse Monier-Williams source data.
        """
        if source_text is None:
            if self.acquirer is None:
                raise ValueError(
                    "No source text or acquisition source supplied"
                )

            if hasattr(
                self.acquirer,
                "read",
            ):
                source_text = self.acquirer.read()

            elif hasattr(
                self.acquirer,
                "acquire",
            ):
                source_text = self.acquirer.acquire()

            else:
                raise TypeError(
                    "acquirer must provide read() or acquire()"
                )

        if not isinstance(source_text, str):
            raise TypeError(
                "source_text must be a string"
            )

        # Explicit parser injection always wins.
        if self.parser is not None:
            return self.parser.parse(
                source_text
            )

        # Empty source is handled consistently by the
        # canonical delimited parser.
        if not source_text.strip():
            return ()

        # Tagged MW representation.
        if self._looks_like_tagged_source(
            source_text
        ):
            return _TaggedMonierWilliamsParser().parse(
                source_text
            )

        # Otherwise attempt canonical delimited input.
        return DelimitedMonierWilliamsParser().parse(
            source_text
        )

    def parse_record(
        self,
        source_text: str,
    ) -> MonierWilliamsSourceRecord:
        """
        Parse exactly one Monier-Williams record.
        """
        records = self.parse(
            source_text
        )

        if len(records) != 1:
            raise ValueError(
                "parse_record requires exactly one record"
            )

        return records[0]

    @staticmethod
    def _looks_like_tagged_source(
        source_text: str,
    ) -> bool:
        """
        Determine whether the source uses original MW tags.
        """
        for line in source_text.splitlines():
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith("<L>"):
                return True

            if stripped.startswith("<k1>"):
                return True

            if stripped.startswith("<e>"):
                return True

            if stripped == "<LEND>":
                return True

            # The first meaningful line is not tagged.
            return False

        return False


class _TaggedMonierWilliamsParser:
    """
    Internal parser for original MW tagged source records.
    """

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
            return ()

        records: list[
            MonierWilliamsSourceRecord
        ] = []

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
                        "Unterminated MW record "
                        "before next <L>"
                    )

                inside = True
                current = [line]
                continue

            if not inside:
                raise ValueError(
                    "Source content encountered "
                    "outside an MW record"
                )

            current.append(line)

        if inside:
            raise ValueError(
                "Unterminated Monier-Williams record"
            )

        if not records:
            raise ValueError(
                "Monier-Williams source contains "
                "no records"
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
            value = stripped[
                close + 1:
            ].strip()

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
