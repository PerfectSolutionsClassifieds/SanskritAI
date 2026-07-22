from __future__ import annotations

"""
SanskritAI
==========

Search Match

Defines the canonical immutable representation of a single
search hit produced by the SanskritAI Search Kernel.

A SearchMatch represents one matching object together with
optional ranking information and metadata.

SearchMatch is intentionally generic so that it may represent
matches originating from:

- Corpus
- Dictionary
- Amarakośa
- Grammar
- Knowledge Repository
- AI Retrieval
- PostgreSQL
- Elasticsearch
- Vector Databases

Architecture
------------

ValueObject
      │
      ▼
SearchMatch
      │
      ▼
SearchResult

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(slots=True, frozen=True)
class SearchMatch(ValueObject):
    """
    Immutable representation of a single search match.
    """

    value: Any

    score: float | None = None

    rank: int | None = None

    location: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.score is not None and self.score < 0:
            raise ValueError(
                "Search score cannot be negative."
            )

        if self.rank is not None and self.rank < 1:
            raise ValueError(
                "Search rank must be greater than zero."
            )

    @property
    def has_score(self) -> bool:
        """
        Returns True if a ranking score is available.
        """
        return self.score is not None

    @property
    def has_rank(self) -> bool:
        """
        Returns True if a result rank is available.
        """
        return self.rank is not None

    @property
    def has_location(self) -> bool:
        """
        Returns True if the match has an associated location.
        """
        return self.location is not None

    @property
    def has_metadata(self) -> bool:
        """
        Returns True if metadata has been supplied.
        """
        return bool(self.metadata)

    def metadata_value(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Returns a metadata value.
        """
        return self.metadata.get(key, default)

    def __str__(self) -> str:
        return str(self.value)
