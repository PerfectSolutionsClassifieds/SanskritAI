from __future__ import annotations

"""
SanskritAI
==========

Abstract Lexical Transformer

Purpose
-------
Defines the canonical transformation contract between

    RawLexicalEntry

and

    CanonicalLexicalRecord

The transformer performs semantic normalization while
remaining completely independent of

    • acquisition
    • parsing
    • repositories
    • databases
    • REST APIs

Architecture
------------

RawLexicalEntry

        │

        ▼

AbstractLexicalTransformer

        │

        ▼

CanonicalLexicalRecord

Concrete Implementations
------------------------

MonierWilliamsTransformer

ApteTransformer

AmarakoshaTransformer

ShabdakalpadrumaTransformer

VacaspatyamTransformer

DhatupathaTransformer

GanapathaTransformer

UnadiTransformer

Version
-------
1.0.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable

from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)

from SanskritAI.acquisition.knowledge.transformers.monier_williams_transformer import (
    CanonicalLexicalRecord,
)


@dataclass(slots=True)
class AbstractLexicalTransformer(ABC):
    """
    Canonical semantic transformation layer.
    """

    resource_name: str

    resource_version: str = "unknown"

    # ---------------------------------------------------------
    # Canonical API
    # ---------------------------------------------------------

    @abstractmethod
    def transform(
        self,
        entry: RawLexicalEntry,
    ) -> CanonicalLexicalRecord:
        """
        Converts one RawLexicalEntry into one
        CanonicalLexicalRecord.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Batch Transformation
    # ---------------------------------------------------------

    def transform_all(
        self,
        entries: Iterable[
            RawLexicalEntry,
        ],
    ) -> tuple[
        CanonicalLexicalRecord,
        ...
    ]:
        """
        Canonical batch transformation.

        Concrete transformers normally inherit this
        implementation unchanged.
        """

        return tuple(

            self.transform(
                entry,
            )

            for entry in entries

        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "transformer": self.__class__.__name__,

            "resource": self.resource_name,

            "version": self.resource_version,

            "target": "CanonicalLexicalRecord",

        }

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:

        return self.__class__.__name__

    def __str__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(resource='{self.resource_name}')"
        )
