
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Parser
-----------------------------

Parses the original Monier-Williams tagged source representation and
supports injected acquisition sources and custom parsers.

Supported usage
---------------

1. Direct parsing::

       parser = MonierWilliamsSourceParser()
       records = parser.parse(source_text)

2. Parsing from an injected source::

       parser = MonierWilliamsSourceParser(
           acquirer=source,
       )
       records = parser.parse()

3. Parsing with a custom parser::

       parser = MonierWilliamsSourceParser(
           acquirer=source,
           parser=DelimitedMonierWilliamsParser(delimiter=","),
       )

4. Parsing exactly one record::

       record = parser.parse_record(source_text)

The class intentionally supports both direct source-text parsing and
acquirer-based parsing so that the acquisition layer remains backward
compatible while the parser remains independently testable.

Version
-------
v0.6.x
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source_record import (
    MonierWilliamsSourceRecord,
)


@dataclass(slots=True)
class MonierWilliamsSourceParser:
    """
    Parser for the original MW tagged source representation.

    Parameters
    ----------
    acquirer:
        Optional acquisition/source object.

        The source may expose either:

        * ``acquire()``
        * ``read()``

        ``acquire()`` is preferred for compatibility with lightweight
        acquisition implementations.

    parser:
        Optional custom parser.

        When omitted, the native tagged Monier-Williams parser is used.
    """

    acquirer: object | None = None
    parser: object | None = None

    def __post_init__(self) -> None:
        if self.parser is None:
            self.parser = _TaggedMonierWilliamsParser()

    # ------------------------------------------------------------------
    # Source acquisition
    # ------------------------------------------------------------------

    def _read_source(self) -> str:
        """
        Acquire source text from the configured acquisition source.

        Returns
        -------
        str
            Complete source representation.

        Raises
        ------
        ValueError
            If no acquisition source is configured.

        TypeError
            If the configured source does not provide ``acquire()``
            or ``read()``.

        NotImplementedError
            If the source explicitly reports that its available
            acquisition method is not implemented.
        """

        if self.acquirer is None:
            raise ValueError(
                "No source text or acquisition source supplied"
            )

        # --------------------------------------------------------------
        # Compatibility-first behavior.
        #
        # Lightweight/legacy implementations often provide acquire()
        # while inheriting a read() method which raises NotImplementedError.
        #
        # Therefore acquire() must be attempted first.
        # --------------------------------------------------------------
        acquire = getattr(self.acquirer, "acquire", None)

        if callable(acquire):
            try:
                source_text = acquire()
            except NotImplementedError:
                # Fall through to read() if acquire() explicitly reports
                # that it is not implemented.
                pass
            else:
                return source_text

        # --------------------------------------------------------------
        # Modern source API.
        # --------------------------------------------------------------
        read = getattr(self.acquirer, "read", None)

        if callable(read):
            return read()

        raise TypeError(
            "acquirer must provide read() or acquire()"
        )

    # ------------------------------------------------------------------
    # Public parsing API
    # ------------------------------------------------------------------

    def parse(
        self,
        source_text: str | None = None,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        """
        Parse Monier-Williams source text.

        Parameters
        ----------
        source_text:
            Optional complete source text.

            If supplied, the text is parsed directly.

            If omitted, the configured ``acquirer`` is used.

        Returns
        -------
        tuple[MonierWilliamsSourceRecord, ...]
            Parsed records.

        Raises
        ------
        TypeError
            If the supplied/acquired source is not a string.

        ValueError
            If no source text or acquisition source is available, or
            if the source representation is invalid.
        """

        # --------------------------------------------------------------
        # Direct parsing mode.
        #
        # This is required by the parser unit tests:
        #
        #     parser.parse(MW_SAMPLE)
        # --------------------------------------------------------------
        if source_text is not None:

            if not isinstance(source_text, str):
                raise TypeError(
                    "source_text must be a string"
                )

            return self._parse_text(source_text)

        # --------------------------------------------------------------
        # Acquisition mode.
        #
        # This is required by the compatibility tests:
        #
        #     parser = MonierWilliamsSourceParser(acquirer=source)
        #     parser.parse()
        # --------------------------------------------------------------
        source_text = self._read_source()

        if not isinstance(source_text, str):
            raise TypeError(
                "Monier-Williams acquisition source must return "
                "a string"
            )

        return self._parse_text(source_text)

    # ------------------------------------------------------------------
    # Internal parser dispatch
    # ------------------------------------------------------------------

    def _parse_text(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        """
        Delegate source text to the configured parser.
        """

        parser = self.parser

        if parser is None:
            # Defensive fallback. Normally __post_init__ guarantees
            # that parser is initialized.
            parser = _TaggedMonierWilliamsParser()

        parse_method = getattr(parser, "parse", None)

        if not callable(parse_method):
            raise TypeError(
                "Monier-Williams parser must provide parse()"
            )

        return parse_method(source_text)

    # ------------------------------------------------------------------
    # Single-record API
    # ------------------------------------------------------------------

    def parse_record(
        self,
        source_text: str,
    ) -> MonierWilliamsSourceRecord:
        """
        Parse exactly one Monier-Williams record.

        Parameters
        ----------
        source_text:
            Source text containing exactly one record.

        Returns
        -------
        MonierWilliamsSourceRecord

        Raises
        ------
        ValueError
            If the source contains zero or multiple records.
        """

        records = self.parse(source_text)

        if len(records) != 1:
            raise ValueError(
                "parse_record requires exactly one record"
            )

        return records[0]


class _TaggedMonierWilliamsParser:
    """
    Internal parser for the original MW tagged representation.

    Example
    -------

    <L>1
    <k1>rAma
    <k2>1
    <h>m.
    <e>pleasing, beautiful
    <LEND>
    """

    START = "<L>"
    END = "<LEND>"

    def parse(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        """
        Parse complete tagged Monier-Williams source text.
        """

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

            # ----------------------------------------------------------
            # Preserve blank lines inside records.
            # ----------------------------------------------------------
            if not stripped:
                if inside:
                    current.append(line)
                continue

            # ----------------------------------------------------------
            # Record termination.
            # ----------------------------------------------------------
            if stripped == self.END:

                if not inside:
                    raise ValueError(
                        "Orphan <LEND> encountered"
                    )

                current.append(line)

                records.append(
                    self._build_record(
                        sequence=len(records) + 1,
                        lines=current,
                    )
                )

                current = []
                inside = False

                continue

            # ----------------------------------------------------------
            # Record start.
            # ----------------------------------------------------------
            if stripped.startswith(self.START):

                if inside:
                    raise ValueError(
                        "Unterminated MW record before next <L>"
                    )

                inside = True
                current = [line]

                continue

            # ----------------------------------------------------------
            # Content outside a record is invalid.
            # ----------------------------------------------------------
            if not inside:
                raise ValueError(
                    "Source content encountered outside "
                    "an MW record"
                )

            current.append(line)

        # --------------------------------------------------------------
        # EOF while still inside a record.
        # --------------------------------------------------------------
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
        """
        Build one raw acquisition-stage source record.
        """

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

        # --------------------------------------------------------------
        # Canonical convenience aliases.
        # --------------------------------------------------------------

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
