from __future__ import annotations

"""
SanskritAI
==========

Search Result

Defines the canonical immutable result of a search operation.

A SearchResult encapsulates the original SearchQuery together
with the resulting SearchMatch objects and optional execution
metadata.

SearchResult is intentionally independent of any particular
search engine, allowing it to be used uniformly across:

- Corpus search
- Dictionary search
- Grammar search
- Knowledge repositories
- SQL / PostgreSQL
- Elasticsearch
- Vector databases
- AI Retrieval (RAG)

Architecture
------------

ValueObject
      │
      ▼
SearchResult
      ├── SearchQuery
      └── SearchMatch(s)

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.search.search_match import SearchMatch
from SanskritAI.core.search.search_query import SearchQuery
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(slots=True, frozen=True)
class SearchResult(ValueObject):
    """
    Immutable result of a search operation.
    """

    query: SearchQuery

    matches: tuple[SearchMatch, ...] = field(default_factory=tuple)

    execution_time_ms: float | None = None

    total_matches: int | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.execution_time_ms is not None and self.execution_time_ms < 0:
            raise ValueError(
                "Execution time cannot be negative."
            )

        if self.total_matches is not None and self.total_matches < 0:
            raise ValueError(
                "Total match count cannot be negative."
            )

    # ---------------------------------------------------------
    # Basic properties
    # ---------------------------------------------------------

    @property
    def count(self) -> int:
        """
        Number of matches contained in this result.
        """
        return len(self.matches)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if no matches were found.
        """
        return self.count == 0

    @property
    def has_matches(self) -> bool:
        """
        Returns True if one or more matches exist.
        """
        return self.count > 0

    @property
    def best_match(self) -> SearchMatch | None:
        """
        Returns the first (highest-ranked) match, if available.
        """
        return self.matches[0] if self.matches else None

    @property
    def effective_total(self) -> int:
        """
        Returns the total number of matches known.

        If the backend reports a total larger than the returned
        page, that value is used; otherwise the local count is
        returned.
        """
        return (
            self.total_matches
            if self.total_matches is not None
            else self.count
        )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def metadata_value(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieves a metadata value.
        """
        return self.metadata.get(key, default)

    # ---------------------------------------------------------
    # Collection behaviour
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator[SearchMatch]:
        return iter(self.matches)

    def __getitem__(self, index: int) -> SearchMatch:
        return self.matches[index]

    def __bool__(self) -> bool:
        return self.has_matches

    def __str__(self) -> str:
        return (
            f"SearchResult("
            f"{self.count} matches"
            f")"
        )
