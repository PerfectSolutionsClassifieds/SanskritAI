from __future__ import annotations

"""
SanskritAI
==========

Parser Interface

Defines the canonical contract for transforming external
sources into immutable DataRecord objects.

The parser layer is the entry point into the SanskritAI
processing pipeline.

Pipeline
--------

External Source
        ↓
Parser
        ↓
DataRecord
        ↓
Validator
        ↓
RecordBuilder
        ↓
Domain Object

Version
-------
v0.6.0
"""

from abc import ABC, abstractmethod
from typing import Generic, Iterable

from SanskritAI.core.records.data_record import DataRecord
from SanskritAI.core.typing import TIdentifier


class Parser(
    Generic[TIdentifier],
    ABC,
):
    """
    Abstract parser interface.

    A parser transforms one or more external sources into
    immutable DataRecord instances.
    """

    @abstractmethod
    def parse(
        self,
        source: object,
    ) -> DataRecord[TIdentifier]:
        """
        Parse a single source into one immutable DataRecord.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_many(
        self,
        source: object,
    ) -> Iterable[DataRecord[TIdentifier]]:
        """
        Parse a source into multiple immutable DataRecord
        instances.
        """
        raise NotImplementedError

    @abstractmethod
    def supports(
        self,
        source: object,
    ) -> bool:
        """
        Returns True if this parser can process the supplied
        source.
        """
        raise NotImplementedError
