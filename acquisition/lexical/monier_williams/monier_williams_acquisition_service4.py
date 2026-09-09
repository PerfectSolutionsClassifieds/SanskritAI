
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Acquisition Service
------------------------------------

Coordinates acquisition of Monier-Williams source content.

Responsibilities
----------------
The service:

1. Reads content from the configured source.
2. Produces acquisition metadata.
3. Optionally delegates parsing to the configured parser.

The service does not perform lexical reasoning and does not write
to the canonical lexical repository.
"""

from dataclasses import dataclass

from .monier_williams_acquisition_result import (
    MonierWilliamsAcquisitionResult,
)
from .monier_williams_parser import MonierWilliamsParser
from .monier_williams_source import MonierWilliamsSource


@dataclass(frozen=True, slots=True)
class MonierWilliamsAcquisitionService:
    """
    Coordinates Monier-Williams source acquisition and parsing.

    Parameters
    ----------
    source:
        Source implementation responsible for reading the raw content.

    parser:
        Optional parser. When supplied, ``acquire()`` delegates the
        acquired source text to the parser and returns the parsed result.
        When omitted, ``acquire()`` returns a
        ``MonierWilliamsAcquisitionResult``.
    """

    source: MonierWilliamsSource
    parser: MonierWilliamsParser | None = None

    def read(self) -> str:
        """
        Read and return the raw source text.

        This is the low-level convenience method and deliberately
        returns the source text unchanged.
        """

        return self.source.read()

    def acquire(
        self,
    ) -> MonierWilliamsAcquisitionResult | object:
        """
        Acquire the configured Monier-Williams source.

        If a parser is configured, the acquired text is passed to
        the parser and its result is returned.

        If no parser is configured, a structured
        ``MonierWilliamsAcquisitionResult`` is returned.

        Returns
        -------
        MonierWilliamsAcquisitionResult | parsed result
        """

        source_text = self.source.read()

        if self.parser is not None:
            return self.parser.parse(source_text)

        return MonierWilliamsAcquisitionResult(
            text=source_text,
            source_identifier=self._source_identifier(),
            source_name=self._source_name(),
            character_count=len(source_text),
            line_count=self._line_count(source_text),
        )

    def count(self) -> int:
        """
        Return the number of acquired or parsed records.

        With a parser configured, this returns the number of parsed
        records.

        Without a parser, this returns the number of logical lines
        in the acquired source.
        """

        result = self.acquire()

        if isinstance(
            result,
            MonierWilliamsAcquisitionResult,
        ):
            return result.line_count

        try:
            return len(result)  # type: ignore[arg-type]
        except TypeError:
            return 0

    def _source_identifier(self) -> str:
        """
        Resolve the source identifier.

        Newer source implementations expose ``identifier``.
        The fallback keeps compatibility with older source contracts.
        """

        identifier = getattr(
            self.source,
            "identifier",
            None,
        )

        if callable(identifier):
            identifier = identifier()

        if identifier is None:
            identifier = getattr(
                self.source,
                "source",
                "",
            )

        return str(identifier)

    def _source_name(self) -> str:
        """
        Resolve the human-readable source name.

        Newer source implementations expose ``source_name``.
        """

        source_name = getattr(
            self.source,
            "source_name",
            None,
        )

        if callable(source_name):
            source_name = source_name()

        if source_name is None:
            source_name = ""

        return str(source_name)

    @staticmethod
    def _line_count(text: str) -> int:
        """
        Return the logical number of lines.

        ``str.splitlines()`` correctly handles the normal newline
        variants without introducing an artificial extra line for
        a trailing newline.

        Empty source therefore contains zero lines.
        """

        if not text:
            return 0

        return len(text.splitlines())
