from __future__ import annotations

"""
SanskritAI
==========

Base Parser

Provides reusable infrastructure for all SanskritAI parsers.

Responsibilities
----------------
- Parser metadata
- Source normalization
- Default batch parsing
- Common extension hooks

Pipeline
--------

External Source
        ↓
BaseParser
        ↓
Concrete Parser
        ↓
DataRecord

Version
-------
v0.6.0
"""

from abc import abstractmethod
from typing import Generic, Iterable

from SanskritAI.core.parsers.parser import Parser
from SanskritAI.core.records.data_record import DataRecord
from SanskritAI.core.typing import TIdentifier


class BaseParser(
    Parser[TIdentifier],
    Generic[TIdentifier],
):
    """
    Base implementation shared by all parsers.
    """

    def __init__(
        self,
        *,
        name: str | None = None,
        version: str = "1.0",
    ) -> None:
        self._name = name or self.__class__.__name__
        self._version = version

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def name(self) -> str:
        """
        Human-readable parser name.
        """
        return self._name

    @property
    def version(self) -> str:
        """
        Parser version.
        """
        return self._version

    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    def normalize_source(
        self,
        source: object,
    ) -> object:
        """
        Normalize an input source before parsing.

        Subclasses may override this hook.
        """
        return source

    # ---------------------------------------------------------
    # Batch parsing
    # ---------------------------------------------------------

    def parse_many(
        self,
        source: Iterable[object],
    ) -> Iterable[DataRecord[TIdentifier]]:
        """
        Parse multiple sources.

        The default implementation delegates to ``parse()`` for
        each individual source.
        """
        for item in source:
            normalized = self.normalize_source(item)
            yield self.parse(normalized)

    # ---------------------------------------------------------
    # Capability
    # ---------------------------------------------------------

    def supports(
        self,
        source: object,
    ) -> bool:
        """
        Returns True if this parser supports the supplied source.

        Subclasses may override for stricter checks.
        """
        return True

    # ---------------------------------------------------------
    # Parsing
    # ---------------------------------------------------------

    @abstractmethod
    def parse(
        self,
        source: object,
    ) -> DataRecord[TIdentifier]:
        """
        Parse a single source into a DataRecord.
        """
        raise NotImplementedError
