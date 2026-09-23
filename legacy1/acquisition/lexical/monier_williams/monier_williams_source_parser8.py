
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Parser
-----------------------------

Orchestrates acquisition and parsing of Monier-Williams source data.

The source parser supports three usage modes:

1. Explicit parser injection
   -------------------------
   A caller may provide a concrete parser implementation. In this case
   the supplied parser is always used.

2. Tagged Monier-Williams source
   ------------------------------
   Native MW tagged records such as:

       <L>1
       <k1>rAma
       <k2>1
       <h>m.
       <e>pleasing, beautiful
       <LEND>

   are parsed by the internal tagged parser.

3. Delimited / compatibility source
   ---------------------------------
   Lightweight representations such as:

       headword<TAB>definition
       rāma<TAB>pleasing

   are delegated to ``DelimitedMonierWilliamsParser``.

The class also supports lightweight / legacy source providers exposing
``acquire()`` instead of ``read()``.

Version
-------
v0.6.x
"""

from typing import Protocol

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)

from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source_record import (
    MonierWilliamsSourceRecord,
)


class _SourceProtocol(Protocol):
    """
    Structural protocol for Monier-Williams source providers.

    A provider may expose ``acquire()`` or ``read()``.
    """

    def acquire(self) -> str:
        ...

    def read(self) -> str:
        ...


class _ParserProtocol(Protocol):
    """
    Structural protocol for injected parser implementations.
    """

    def parse(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsRecord, ...]:
        ...


class MonierWilliamsSourceParser:
    """
    Acquire and parse Monier-Williams source text.

    Parameters
    ----------
    acquirer:
        Optional source/acquisition object.

    parser:
        Optional concrete parser implementation.

    Behavior
    --------
    If ``parser`` is supplied, it is always used.

    Otherwise the source representation is detected automatically:

    * tagged MW source -> tagged parser
    * delimited source -> DelimitedMonierWilliamsParser

    ``acquire()`` is preferred over ``read()`` when both are available.
    This preserves compatibility with lightweight source implementations
    that inherit a ``read()`` method but implement only ``acquire()``.
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

        Returns
        -------
        str
            Complete source representation.

        Raises
        ------
        ValueError
            If no source has been configured.

        TypeError
            If the configured source exposes neither ``acquire()``
            nor ``read()``.
        """

        if self.acquirer is None:
            raise ValueError(
                "No Monier-Williams acquisition source configured"
            )

        # --------------------------------------------------------------
        # Compatibility-first behavior.
        #
        # Some lightweight implementations inherit ``read()`` but
        # intentionally implement only ``acquire()``.
        # --------------------------------------------------------------
        acquire = getattr(
            self.acquirer,
            "acquire",
            None,
        )

        if callable(acquire):
            return acquire()

        read = getattr(
            self.acquirer,
            "read",
            None,
        )

        if callable(read):
            return read()

        raise TypeError(
            "Monier-Williams acquirer must provide "
            "acquire() or read()"
        )

    # ------------------------------------------------------------------
    # Source representation detection
    # ------------------------------------------------------------------

    @staticmethod
    def _is_tagged_source(
        source_text: str,
    ) -> bool:
        """
        Determine whether source text uses native MW tagged records.

        A tagged source normally begins with ``<L>`` after optional
        whitespace.

        Parameters
        ----------
        source_text:
            Complete source representation.

        Returns
        -------
        bool
            ``True`` for tagged MW input, otherwise ``False``.
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
    ) -> object:
        """
        Select an appropriate parser for the supplied source.

        Tagged MW records are handled by the internal tagged parser.

        All other source representations are delegated to the
        compatibility-friendly delimited parser.
        """

        if self._is_tagged_source(source_text):
            return _TaggedMonierWilliamsParser()

        from SanskritAI.acquisition.lexical.monier_williams.delimited_monier_williams_parser import (
            DelimitedMonierWilliamsParser,
        )

        return DelimitedMonierWilliamsParser()

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def parse(
        self,
        source_text: str | None = None,
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Parse Monier-Williams source text.

        Parameters
        ----------
        source_text:
            Optional source text.

            If supplied, the supplied text is parsed directly.

            If omitted, text is acquired from ``self.acquirer``.

        Returns
        -------
        tuple[MonierWilliamsRecord, ...]
            Parsed records.

        Raises
        ------
        TypeError
            If source text is not a string.

        ValueError
            If source text is empty or invalid.

        Notes
        -----
        The optional ``source_text`` parameter is intentional.

        It preserves two valid APIs:

        ``parser.parse(text)``

        and

        ``parser.parse()``

        where the latter acquires source text through the configured
        acquisition object.
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

        # --------------------------------------------------------------
        # Explicit parser injection always wins.
        # --------------------------------------------------------------
        if self.parser is not None:
            return self.parser.parse(source_text)

        # --------------------------------------------------------------
        # Automatic representation detection.
        # --------------------------------------------------------------
        parser = self._create_default_parser(
            source_text
        )

        return parser.parse(source_text)

    # ------------------------------------------------------------------
    # Single-record parsing
    # ------------------------------------------------------------------

    def parse_record(
        self,
        source_text: str,
    ) -> MonierWilliamsRecord | MonierWilliamsSourceRecord:
        """
        Parse exactly one Monier-Williams record.

        Parameters
        ----------
        source_text:
            Text containing exactly one record.

        Returns
        -------
        MonierWilliamsRecord | MonierWilliamsSourceRecord
            Parsed record.

        Raises
        ------
        TypeError
            If source text is not a string.

        ValueError
            If zero or multiple records are present.
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

    Record structure
    ----------------
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
        Construct a ``MonierWilliamsSourceRecord`` from one tagged
        record.
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
                value = stripped[len("<L>") :].strip()

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
                    value = stripped[close + 1 :].strip()

                    fields[tag] = value

                    continue

        return MonierWilliamsSourceRecord(
            sequence=sequence,
            raw_text="\n".join(lines),
            fields=fields,
        )
