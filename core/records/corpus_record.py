from __future__ import annotations

"""
SanskritAI
==========

Corpus Record

Semantic base class for all Corpus transfer records.

CorpusRecord represents immutable data exchanged between
parsers, builders, repositories and importers within the
Corpus subsystem.

Concrete examples
-----------------

DocumentRecord
SectionRecord
VerseRecord
ParagraphRecord
LineRecord
TokenRecord

Version
-------
v0.4.0
"""

from dataclasses import dataclass
from typing import Generic

from SanskritAI.core.records.data_record import (
    DataRecord,
)
from SanskritAI.core.typing import TIdentifier


@dataclass(slots=True, frozen=True)
class CorpusRecord(
    DataRecord[TIdentifier],
    Generic[TIdentifier],
):
    """
    Base class for all Corpus records.

    This class intentionally introduces no additional fields.
    It exists to establish a stable type hierarchy and allow
    future corpus-wide behavior to be shared.
    """

    pass
