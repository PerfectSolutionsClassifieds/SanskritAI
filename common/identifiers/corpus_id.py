from __future__ import annotations

"""
SanskritAI
==========

Corpus Identifier

Strongly typed identifier for Corpus objects.

A CorpusId uniquely identifies a canonical Corpus within
SanskritAI. It inherits all functionality from BaseIdentifier,
including:

    * UUID generation
    * String conversion
    * JSON serialization
    * Hashability
    * Equality comparison

Using a dedicated subclass provides compile-time and runtime
type safety, preventing accidental interchange of identifiers
belonging to different domain models.

Example
-------

    corpus_id = CorpusId.generate()

    print(corpus_id)

    corpus.id == corpus_id

Version
-------
v0.1.0
"""

from dataclasses import dataclass

from SanskritAI.common.identifiers.base_identifier import (
    BaseIdentifier,
)


@dataclass(frozen=True, slots=True)
class CorpusId(BaseIdentifier):
    """
    Identifier for a Corpus.

    No additional state or behavior is required beyond what is
    provided by BaseIdentifier. This subclass exists to provide
    a distinct domain type.
    """

    pass
