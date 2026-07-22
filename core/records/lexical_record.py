from __future__ import annotations

"""
SanskritAI
==========

Lexical Record

Semantic base class for immutable lexical transfer objects.

Concrete examples
-----------------

LexemeRecord
DictionaryEntryRecord
DictionarySenseRecord
LexicalRelationRecord

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
class LexicalRecord(
    DataRecord[TIdentifier],
    Generic[TIdentifier],
):
    """
    Base class for all Lexical records.

    Reserved for future lexical-wide functionality.
    """

    pass
