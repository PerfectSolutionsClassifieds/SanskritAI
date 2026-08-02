from __future__ import annotations

"""
SanskritAI
==========

Abstract Lexical Pipeline

Purpose
-------
Defines the canonical orchestration lifecycle for every
lexical knowledge acquisition pipeline.

Concrete pipelines include

    • MonierWilliamsPipeline
    • AptePipeline
    • AmarakoshaPipeline
    • ShabdakalpadrumaPipeline
    • VacaspatyamPipeline
    • DhatupathaPipeline
    • GanapathaPipeline
    • UnadiPipeline

The pipeline itself never performs

    • downloading
    • parsing
    • transformation
    • repository persistence

Those responsibilities belong to the injected
components.

Architecture
------------

Manifest

        ↓

Connector

        ↓

Parser

        ↓

Transformer

        ↓

Repository

Lifecycle
---------

before_execute()

↓

discover()

↓

acquire()

↓

parse()

↓

transform()

↓

populate_repository()

↓

after_execute()

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
class AbstractLexicalPipeline(ABC):
    """
    Canonical orchestration layer for lexical acquisition.
    """

    # ---------------------------------------------------------
    # Required Components
    # ---------------------------------------------------------

    manifest: Any

    connector: Any

    parser: Any

    transformer: Any

    repository: Any

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_execute(
        self,
    ) -> None:
        """
        Optional pre-execution hook.

        Examples

            logging

            initialization

            diagnostics

            timing
        """

        return None

    def after_execute(
        self,
        repository: Any,
    ) -> Any:
        """
        Optional post-execution hook.

        Examples

            statistics

            validation

            indexing

            exporting

        Default behaviour simply returns the repository.
        """

        return repository

    # ---------------------------------------------------------
    # Canonical Execution
    # ---------------------------------------------------------

    def execute(
        self,
        destination: Path,
    ) -> Any:
        """
        Executes the complete lexical acquisition
        pipeline.
        """

        self.before_execute()

        # ---------------------------------------------
        # Discovery
        # ---------------------------------------------

        self.connector.discover()

        # ---------------------------------------------
        # Acquisition
        # ---------------------------------------------

        source = self.connector.acquire(
            destination,
        )

        # ---------------------------------------------
        # Parsing
        # ---------------------------------------------

        raw_entries = self.parser.parse(
            source,
        )

        # ---------------------------------------------
        # Transformation
        # ---------------------------------------------

        canonical_records = self.transformer.transform_all(
            raw_entries,
        )

        # ---------------------------------------------
        # Repository population
        # ---------------------------------------------

        self.repository.add_all(
            canonical_records,
        )

        return self.after_execute(
            self.repository,
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        """
        Returns pipeline diagnostics.
        """

        return {

            "pipeline": self.__class__.__name__,

            "resource": self.manifest.resource_name,

            "manifest": self.manifest.summary(),

            "connector": self.connector.summary(),

            "parser": self.parser.summary(),

            "transformer": self.transformer.summary(),

            "repository": self.repository.summary(),

        }

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:

        return self.manifest.identifier

    @property
    def resource_name(
        self,
    ) -> str:

        return self.manifest.resource_name

    # ---------------------------------------------------------
    # String Representation
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"({self.identifier})"
        )
