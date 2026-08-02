from __future__ import annotations

"""
SanskritAI
==========

Abstract Lexical Connector

Purpose
-------
Defines the canonical acquisition lifecycle for every
lexical knowledge source integrated into the Canonical
Sanskrit Knowledge Repository.

Examples
--------

    • Monier–Williams
    • Apte
    • Amarakośa
    • Śabdakalpadruma
    • Vācaspatyam
    • Dhātupāṭha
    • Gaṇapāṭha
    • Uṇādi

The connector itself never performs parsing or
normalization. Those responsibilities are delegated
to dedicated parser / transformer components.

Canonical Lifecycle
-------------------

discover()

↓

acquire()

↓

parse()

↓

transform()

↓

validate()

↓

publish()

Each stage may be overridden independently.

Version
-------
1.0.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class AbstractLexicalConnector(ABC):
    """
    Base class for all lexical acquisition connectors.
    """

    source_name: str

    source_version: str = "unknown"

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    @abstractmethod
    def discover(
        self,
    ) -> Any:
        """
        Discovers the resource.

        Examples

            local files

            downloadable archive

            online repository

            REST endpoint

        Returns implementation-specific discovery metadata.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Acquisition
    # ---------------------------------------------------------

    @abstractmethod
    def acquire(
        self,
        destination: Path,
    ) -> Path:
        """
        Acquires the raw source.

        Returns

            Path to acquired resource.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Parsing
    # ---------------------------------------------------------

    @abstractmethod
    def parse(
        self,
        source: Path,
    ) -> Any:
        """
        Parses the acquired resource.

        Returns parser-specific intermediate model.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Transformation
    # ---------------------------------------------------------

    @abstractmethod
    def transform(
        self,
        parsed: Any,
    ) -> Any:
        """
        Converts parser output into the canonical
        SanskritAI lexical model.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        transformed: Any,
    ) -> Any:
        """
        Optional validation hook.

        Default implementation simply returns the object.
        """

        return transformed

    # ---------------------------------------------------------
    # Publishing
    # ---------------------------------------------------------

    @abstractmethod
    def publish(
        self,
        transformed: Any,
    ) -> Any:
        """
        Publishes the canonical knowledge.

        Examples

            JSON

            PostgreSQL

            MongoDB

            Redis

            REST API

        Concrete connectors decide the publishing target.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Pipeline
    # ---------------------------------------------------------

    def execute(
        self,
        destination: Path,
    ) -> Any:
        """
        Executes the complete acquisition pipeline.

            discover()

            acquire()

            parse()

            transform()

            validate()

            publish()
        """

        self.discover()

        source = self.acquire(
            destination,
        )

        parsed = self.parse(
            source,
        )

        transformed = self.transform(
            parsed,
        )

        transformed = self.validate(
            transformed,
        )

        return self.publish(
            transformed,
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        """
        Connector metadata.
        """

        return {
            "source_name": self.source_name,
            "source_version": self.source_version,
            "connector": self.__class__.__name__,
        }

    def __str__(
        self,
    ) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(source='{self.source_name}', "
            f"version='{self.source_version}')"
        )
