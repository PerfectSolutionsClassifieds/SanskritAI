from __future__ import annotations

"""
SanskritAI
==========

Abstract Lexical Transformer

Canonical semantic transformation contract.

Pipeline

RawLexicalEntry
        │
        ▼
AbstractLexicalTransformer
        │
        ▼
CanonicalLexicalRecord
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable

from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_lexical_record import (
    CanonicalLexicalRecord,
)


@dataclass(slots=True)
class AbstractLexicalTransformer(ABC):
    """
    Canonical semantic transformation layer.
    """

    resource_name: str

    resource_version: str = "unknown"

    @abstractmethod
    def transform(
        self,
        entry: RawLexicalEntry,
    ) -> CanonicalLexicalRecord:
        """
        Transform one lexical entry into the canonical model.
        """
        raise NotImplementedError

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
        """

        return tuple(

            self.transform(
                entry,
            )

            for entry in entries

        )

    def summary(
        self,
    ) -> dict:

        return {

            "transformer": self.__class__.__name__,

            "resource": self.resource_name,

            "version": self.resource_version,

            "target": CanonicalLexicalRecord.__name__,

        }

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
