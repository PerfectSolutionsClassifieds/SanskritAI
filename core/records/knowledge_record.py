from __future__ import annotations

"""
SanskritAI
==========

Knowledge Record

Semantic base class for immutable knowledge-layer transfer
objects.

Concrete examples
-----------------

SynsetRecord
VargaRecord
CommentaryRecord
OntologyRecord
CrossReferenceRecord

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
class KnowledgeRecord(
    DataRecord[TIdentifier],
    Generic[TIdentifier],
):
    """
    Base class for all Knowledge records.

    This abstraction unifies Amarakośa and future knowledge
    resources while remaining independent of any specific
    source.
    """

    pass
