
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Parser
-----------------------------

Orchestrates acquisition of Monier-Williams source text and delegates
the actual parsing to a concrete parser implementation.

The parser supports both:

* modern sources implementing ``read()``
* lightweight / legacy sources implementing ``acquire()``

When both methods are present, ``acquire()`` is preferred because some
compatibility implementations inherit ``read()`` from the abstract
source contract while intentionally implementing only ``acquire()``.

A custom parser may be injected for alternate source representations.

Version
-------
v0.6.x
"""

from typing import Protocol

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)


class _SourceProtocol(Protocol):
    """
    Structural protocol for Monier-Williams source providers.

    A source may expose either ``acquire()`` or ``read()``.
    """

    def acquire(self) -> str:
        ...

    def read(self) -> str:
        ...


class _ParserProtocol(Protocol):
    """
    Structural protocol for injected Monier-Williams parsers.
    """

    def parse(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsRecord, ...]:
        ...


class MonierWilliamsSourceParser:
    """
    Acquire Monier-Williams source text and parse it.

    Parameters
    ----------
    acquirer:
        Optional source/acquisition object.

    parser:
        Optional concrete parser implementation.

    Notes
    -----
    ``acquire()`` is preferred over ``read()`` for compatibility with
    lightweight source implementations. If ``acquire()`` is unavailable,
    ``read()`` is used.

    A source whose inherited ``read()`` raises ``NotImplementedError``
    may still provide a working ``acquire()`` implementation.
    """

    def __init__(
        self,
        acquirer: _SourceProtocol | None = None,
        parser: _ParserProtocol | None = None,
    ) -> None:
        self.acquirer = acquirer
        self.parser = parser

    def _read_source(self) -> str:
        """
        Acquire source text from the configured source.

        Returns
        -------
        str
            Complete source representation.

        Raises
        ------
        ValueError
            If no acquisition source is configured.

        TypeError
            If the source does not provide ``acquire()`` or ``read()``.

        NotImplementedError
            If the available acquisition method explicitly reports that
            it is not implemented.
        """

        if self.acquirer is None:
            raise ValueError(
                "No Monier-Williams acquisition source configured"
            )

        # Compatibility-first behavior:
        #
        # Lightweight / legacy source implementations may implement
        # acquire() while inheriting a read() method which raises
        # NotImplementedError.
        acquire = getattr(self.acquirer, "acquire", None)

        if callable(acquire):
            return acquire()

        read = getattr(self.acquirer, "read", None)

        if callable(read):
            return read()

        raise TypeError(
            "Monier-Williams acquirer must provide "
            "acquire() or read()"
        )

    def parse(
        self,
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Acquire and parse the complete Monier-Williams source.

        Returns
        -------
        tuple[MonierWilliamsRecord, ...]
            Parsed Monier-Williams records.

        Empty source
        ------------
        Empty or whitespace-only source is delegated to the configured
        parser. Parsers that treat an empty source as an empty collection
        therefore return ``()`` naturally.
        """

        source_text = self._read_source()

        if not isinstance(source_text, str):
            raise TypeError(
                "Monier-Williams acquisition source must return "
                "a string"
            )

        parser = self.parser

        if parser is None:
            from SanskritAI.acquisition.lexical.monier_williams.delimited_monier_williams_parser import (
                DelimitedMonierWilliamsParser,
            )

            parser = DelimitedMonierWilliamsParser()

        return parser.parse(source_text)
