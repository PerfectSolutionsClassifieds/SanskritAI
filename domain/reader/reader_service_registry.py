from __future__ import annotations

"""
SanskritAI
==========

Reader Service Registry

Composition root for the Reader Domain.

Owns and wires together the reader-facing services.

Architecture
------------

ReaderEngine
      │
      ▼
ReaderServiceRegistry
      │
      ├── ReaderRepository
      ├── ReaderNavigator
      └── ReaderEngine

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.corpus.models.corpus import (
    Corpus,
)

from SanskritAI.domain.reader.default_reader_repository import (
    DefaultReaderRepository,
)

from SanskritAI.domain.reader.reader_repository import (
    ReaderRepository,
)

from SanskritAI.domain.reader.reader_navigator import (
    ReaderNavigator,
)


@dataclass(
    slots=True,
)
class ReaderServiceRegistry:
    """
    Composition root of the Reader Domain.
    """

    corpus: Corpus

    reader_repository: ReaderRepository = field(init=False)

    reader_navigator: ReaderNavigator = field(init=False)

    # ---------------------------------------------------------

    def __post_init__(
        self,
    ) -> None:

        self.reader_repository = (
            DefaultReaderRepository(
                corpus=self.corpus,
            )
        )

        self.reader_navigator = (
            ReaderNavigator(
                repository=self.reader_repository,
            )
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def repository(
        self,
    ) -> ReaderRepository:
        return self.reader_repository

    @property
    def navigator(
        self,
    ) -> ReaderNavigator:
        return self.reader_navigator
