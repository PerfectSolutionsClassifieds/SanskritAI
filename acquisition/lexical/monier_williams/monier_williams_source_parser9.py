
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Parser
-----------------------------

Acquisition-layer parser for Monier-Williams source data.

Canonical acquisition-layer flow:

    source
        ↓
    raw source text
        ↓
    MonierWilliamsSourceParser
        ↓
    tuple[MonierWilliamsSourceRecord, ...]

Supported source representations
--------------------------------

1. Native tagged Monier-Williams source

       <L>1
       <k1>rAma
       <k2>1
       <h>m.
       <e>pleasing, beautiful
       <LEND>

2. Delimited / compatibility source

       headword<TAB>definition

3. Explicit parser injection

The injected parser is used exactly as supplied.

Source compatibility
--------------------

Source providers exposing either ``acquire()`` or ``read()`` are
supported. ``acquire()`` is preferred when both are available.

Canonical return contract
-------------------------

All parsing performed through this class returns:

    tuple[MonierWilliamsSourceRecord, ...]

This establishes ``MonierWilliamsSourceRecord`` as the acquisition-layer
boundary object.

Conversion into the domain-level ``MonierWilliamsRecord`` belongs to the
subsequent adapter/mapping boundary and is intentionally not performed
here.
"""

from typing import Protocol

from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source_record import (
    MonierWilliamsSourceRecord,
)


class _SourceProtocol(Protocol):
    """
    Structural protocol for Monier-Williams source providers.

    A compatible provider may expose ``acquire()`` or ``read()``.
    """

    def acquire(self) -> str:
        ...

    def read(self) -> str:
        ...


class _ParserProtocol(Protocol):
    """
    Structural protocol for acquisition-layer parser implementations.

    Every parser injected into MonierWilliamsSourceParser must produce
    acquisition-layer SourceRecord objects.
    """

    def parse(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        ...


class MonierWilliamsSourceParser:
    """
    Acquire and parse Monier-Williams source text.

    Responsibilities
    ----------------

    This class is responsible for:

    1. acquiring source text when required,
    2. detecting the source representation,
    3. selecting the appropriate parser,
    4. enforcing the acquisition-layer parser contract.

    It does not convert SourceRecord objects into domain lexical records.
    """

    def __init__(
        self,
        acquirer: _SourceProtocol | None = None,
        parser: _ParserProtocol | None = None,
    ) -> None:
        self.acquirer = acquirer
        self.parser = parser

    # ------------------------------------------------------------------
    # Source acquisition
    # ------------------------------------------------------------------

    def _read_source(self) -> str:
        """
        Acquire complete source text from the configured source.

        ``acquire()`` is preferred over ``read()`` for compatibility with
        legacy source implementations.
        """

        if self.acquirer is None:
            raise ValueError(
                "No Monier-Williams acquisition source configured"
            )

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

            if not callable(read):
                raise TypeError(
                    "Monier-Williams acquirer must provide "
                    "acquire() or read()"
                )

            source_text = read()

        if not isinstance(source_text, str):
            raise TypeError(
                "Monier-Williams acquisition source "
                "must return source text as str"
            )

        return source_text

    # ------------------------------------------------------------------
    # Source representation detection
    # ------------------------------------------------------------------

    @staticmethod
    def _is_tagged_source(
        source_text: str,
    ) -> bool:
        """
        Determine whether source text uses native MW tagged records.

        Native tagged input normally begins with ``<L>`` after optional
        leading whitespace.
        """

        stripped = source_text.lstrip()

        return (
            stripped.startswith("<L>")
            or stripped.startswith("<LEND>")
        )

    # ------------------------------------------------------------------
    # Default parser selection
    # ------------------------------------------------------------------

    def _create_default_parser(
        self,
        source_text: str,
    ) -> _ParserProtocol:
        """
        Select the parser appropriate for the supplied source text.
        """

        if self._is_tagged_source(source_text):
            return _TaggedMonierWilliamsParser()

        from SanskritAI.acquisition.lexical.monier_williams.delimited_monier_williams_parser import (
            DelimitedMonierWilliamsParser,
        )

        return DelimitedMonierWilliamsParser()

    # ------------------------------------------------------------------
    # Result validation
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_records(
        records: object,
    ) -> tuple[MonierWilliamsSourceRecord, ...]:
        """
        Validate and normalize parser output.

        The public parser contract is always a tuple of
        MonierWilliamsSourceRecord objects.
        """

        if not isinstance(records, (tuple, list)):
            raise TypeError(
                "Monier-Williams parser must return "
                "a tuple or list of MonierWilliamsSourceRecord"
            )

        normalized = tuple(records)

        if not all(
            isinstance(
                record,
                MonierWilliamsSourceRecord,
            )
            for record in normalized
        ):
            raise TypeError(
                "Monier-Williams parser must return only "
                "MonierWilliamsSourceRecord instances"
            )

        return normalized

    # ------------------------------------------------------------------
    # Parsing
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
            Optional source text.

            If supplied, it is parsed directly.

            If omitted, source text is acquired through ``self.acquirer``.

        Returns
        -------
        tuple[MonierWilliamsSourceRecord, ...]
            Canonical acquisition-layer records.
        """

        if source_text is None:
            source_text = self._read_source()

        if not isinstance(source_text, str):
            raise TypeError(
                "Monier-Williams source must be a string"
            )

        if not source_text.strip():
            raise ValueError(
                "Monier-Williams source is empty"
            )

        # Explicit parser injection always wins.
        if self.parser is not None:
            return self._validate_records(
                self.parser.parse(source_text)
            )

        # Automatic source representation detection.
        parser = self._create_default_parser(
            source_text
        )

        return self._validate_records(
            parser.parse(source_text)
        )

    # ------------------------------------------------------------------
    # Single-record parsing
    # ------------------------------------------------------------------

    def parse_record(
        self,
        source_text: str,
    ) -> MonierWilliamsSourceRecord:
        """
        Parse exactly one Monier-Williams source record.
        """

        if not isinstance(source_text, str):
            raise TypeError(
                "source_text must be a string"
            )

        records = self.parse(source_text)

        if len(records) != 1:
            raise ValueError(
                "parse_record() requires exactly one "
                "Monier-Williams record"
            )

        return records[0]


# ======================================================================
# Tagged Monier-Williams parser
# ======================================================================


class _TaggedMonierWilliamsParser:
    """
    Parser for native Monier-Williams tagged records.

    Example:

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
                        "Unterminated MW record before "
                        "next <L>"
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
        # Unterminated final record.
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
        Construct a MonierWilliamsSourceRecord from one tagged record.
        """

        fields: dict[str, str] = {}

        for line in lines:

            stripped = line.strip()

            if not stripped:
                continue

            # ----------------------------------------------------------
            # <L> is the sequence/tag identifier.
            # ----------------------------------------------------------

            if stripped.startswith("<L>"):

                value = stripped[len("<L>"):].strip()

                if value:
                    fields["L"] = value

                continue

            # ----------------------------------------------------------
            # <LEND> has no field value.
            # ----------------------------------------------------------

            if stripped == self.END:
                continue

            # ----------------------------------------------------------
            # Generic MW tag:
            #
            # <k1>rAma
            # <h>m.
            # <e>meaning
            # ----------------------------------------------------------

            if stripped.startswith("<"):

                close = stripped.find(">")

                if close > 1:

                    tag = stripped[1:close]
                    value = stripped[close + 1:].strip()

                    fields[tag] = value

                    continue

        return MonierWilliamsSourceRecord(
            sequence=sequence,
            raw_text="\n".join(lines),
            fields=fields,
        )
