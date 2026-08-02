from __future__ import annotations

"""
SanskritAI
==========

Abstract Lexical Pipeline

Purpose
-------
Defines the canonical acquisition lifecycle for every
lexical knowledge source.

Every lexical resource should inherit this class.

Examples

    MonierWilliamsPipeline

    AptePipeline

    AmarakoshaPipeline

    SabdakalpadrumaPipeline

    VacaspatyamPipeline

    DhatuPathaPipeline

    GanaPathaPipeline

    UnadiPipeline

Pipeline Lifecycle
------------------

connect()

↓

fetch()

↓

parse()

↓

transform()

↓

validate()

↓

persist()

↓

build_manifest()

↓

report()

Only the acquisition-specific components differ;
the orchestration remains identical.

Version
-------
2.0.0
"""

from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass
from dataclasses import field

from typing import Any


@dataclass(slots=True)
class AbstractLexicalPipeline(ABC):
    """
    Canonical lexical acquisition pipeline.
    """

    connector: Any

    parser: Any

    transformer: Any

    repository: Any

    manifest: Any | None = field(
        default=None,
        init=False,
    )

    # ---------------------------------------------------------
    # High-level execution
    # ---------------------------------------------------------

    def execute(
        self,
    ) -> Any:
        """
        Executes the complete acquisition lifecycle.
        """

        self.before_pipeline()

        self.connect()

        raw_resource = self.fetch()

        raw_entries = self.parse(
            raw_resource,
        )

        canonical_records = self.transform(
            raw_entries,
        )

        validated_records = self.validate(
            canonical_records,
        )

        persisted = self.persist(
            validated_records,
        )

        self.manifest = self.build_manifest(
            persisted,
        )

        self.after_pipeline()

        return self.report()

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def before_pipeline(
        self,
    ) -> None:
        """
        Optional hook.
        """

        return

    def after_pipeline(
        self,
    ) -> None:
        """
        Optional hook.
        """

        return

    # ---------------------------------------------------------
    # Stage 1
    # ---------------------------------------------------------

    def connect(
        self,
    ) -> None:

        self.connector.connect()

    # ---------------------------------------------------------
    # Stage 2
    # ---------------------------------------------------------

    def fetch(
        self,
    ) -> Any:

        return self.connector.fetch()

    # ---------------------------------------------------------
    # Stage 3
    # ---------------------------------------------------------

    def parse(
        self,
        resource: Any,
    ):

        return self.parser.parse(
            resource,
        )

    # ---------------------------------------------------------
    # Stage 4
    # ---------------------------------------------------------

    def transform(
        self,
        raw_entries,
    ):

        return self.transformer.transform(
            raw_entries,
        )

    # ---------------------------------------------------------
    # Stage 5
    # ---------------------------------------------------------

    def validate(
        self,
        canonical_records,
    ):
        """
        Default implementation.

        Individual pipelines may override this.
        """

        return canonical_records

    # ---------------------------------------------------------
    # Stage 6
    # ---------------------------------------------------------

    def persist(
        self,
        canonical_records,
    ):

        return self.repository.store(
            canonical_records,
        )

    # ---------------------------------------------------------
    # Stage 7
    # ---------------------------------------------------------

    @abstractmethod
    def build_manifest(
        self,
        persisted_objects,
    ):
        """
        Resource-specific manifest.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Stage 8
    # ---------------------------------------------------------

    def report(
        self,
    ) -> dict:
        """
        Generic execution report.
        """

        return {

            "pipeline": self.__class__.__name__,

            "manifest": self.manifest,

        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "pipeline": self.__class__.__name__,

            "connector": self.connector.__class__.__name__,

            "parser": self.parser.__class__.__name__,

            "transformer": self.transformer.__class__.__name__,

            "repository": self.repository.__class__.__name__,

        }

    def __str__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            "("
            f"{self.connector.__class__.__name__}"
            ")"
        )
