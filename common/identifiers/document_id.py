
from __future__ import annotations

"""
SanskritAI
==========

Document Identifier

Strongly typed identifier for Document objects.

A DocumentId uniquely identifies a Document within a Corpus.

Inheritance
-----------

    BaseIdentifier
          │
          ▼
     DocumentId

Features
--------
* Immutable
* UUID-based
* Hashable
* Comparable
* JSON serializable
* Type-safe

Version
-------
v0.1.0
"""

from dataclasses import dataclass

from SanskritAI.common.identifiers.base_identifier import (
    BaseIdentifier,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentId(BaseIdentifier):
    """
    Identifier for a Document.

    This class intentionally contains no additional logic.
    All behavior is inherited from BaseIdentifier.

    The dedicated type prevents accidental interchange with
    identifiers belonging to other domain models such as
    CorpusId, VerseId, or TokenId.
    """

    pass
