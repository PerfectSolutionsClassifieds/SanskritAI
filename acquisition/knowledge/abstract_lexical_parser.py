from __future__ import annotations

"""
SanskritAI
==========

Abstract Lexical Parser

Purpose
-------
Defines the canonical contract for every lexical parser.

A parser is responsible ONLY for structural extraction.

It converts an acquired lexical resource into immutable
RawLexicalEntry objects.

It NEVER

    • downloads resources

    • performs normalization

    • performs grammatical inference

    • creates canonical lexical objects

    • writes to repositories

Architecture
------------

Connector

        ↓

AbstractLexicalParser

        ↓

RawLexicalEntry

        ↓

Transformer

Concrete Implementations
------------------------

MonierWilliamsParser

ApteParser

AmarakoshaParser

ShabdakalpadrumaParser

VacaspatyamParser

DhatupathaParser

GanapathaParser

UnadiParser

Version
-------
1.0.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from typing import Iterator

from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)


@dataclass(slots=True)
class AbstractLexicalParser(ABC):
    """
    Canonical base class for every lexical parser.
    """

    source_name: str

    source_version: str = "unknown"

    encoding: str = "utf-8"

    # ---------------------------------------------------------
    # Canonical Parsing API
    # ---------------------------------------------------------

    @abstractmethod
    def parse(
        self,
        source: Path,
    ) -> tuple[
        RawLexicalEntry,
        ...
    ]:
        """
        Parses an acquired lexical resource.

        Returns immutable RawLexicalEntry objects.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Record Iteration
    # ---------------------------------------------------------

    @abstractmethod
    def iter_records(
        self,
        source: Path,
    ) -> Iterator[str]:
        """
        Iterates over raw records contained in the
        lexical resource.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Record Parsing
    # ---------------------------------------------------------

    @abstractmethod
    def parse_record(
        self,
        record: str,
    ) -> RawLexicalEntry | None:
        """
        Parses one raw record into a RawLexicalEntry.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        """
        Parser diagnostics.
        """

        return {

            "parser": self.__class__.__name__,

            "source": self.source_name,

            "version": self.source_version,

            "encoding": self.encoding,

        }

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:
        """
        Stable parser identifier.
        """

        return self.__class__.__name__

    def __str__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(source='{self.source_name}')"
        )
