from __future__ import annotations

"""
SanskritAI
==========

Search Query

Defines the canonical immutable search request used by the
SanskritAI Search Kernel.

A SearchQuery combines one or more SearchTerm objects with a
SearchOptions instance to describe a complete search request.

SearchQuery itself contains no search logic. It is a pure,
immutable value object that can be consumed by any search
engine.

Typical usages include:

- Dictionary lookup
- Corpus search
- Grammar search
- Amarakośa search
- Semantic retrieval
- AI / RAG retrieval

Architecture
------------

ValueObject
      │
      ▼
SearchQuery
      │
      ├── SearchTerm(s)
      └── SearchOptions

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.search.search_options import SearchOptions
from SanskritAI.core.search.search_term import SearchTerm
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(slots=True, frozen=True)
class SearchQuery(ValueObject):
    """
    Immutable search request.
    """

    terms: tuple[SearchTerm, ...] = field(default_factory=tuple)

    options: SearchOptions = field(default_factory=SearchOptions)

    def __post_init__(self) -> None:
        if len(self.terms) == 0:
            raise ValueError(
                "SearchQuery must contain at least one SearchTerm."
            )

    @property
    def term_count(self) -> int:
        """
        Returns the number of search terms.
        """
        return len(self.terms)

    @property
    def is_single_term(self) -> bool:
        """
        Returns True if the query contains exactly one term.
        """
        return self.term_count == 1

    @property
    def is_multi_term(self) -> bool:
        """
        Returns True if the query contains multiple terms.
        """
        return self.term_count > 1

    def append(
        self,
        term: SearchTerm,
    ) -> "SearchQuery":
        """
        Returns a new SearchQuery with the supplied term appended.
        """
        return SearchQuery(
            terms=self.terms + (term,),
            options=self.options,
        )

    def __iter__(self) -> Iterator[SearchTerm]:
        return iter(self.terms)

    def __len__(self) -> int:
        return self.term_count

    def __str__(self) -> str:
        return " ".join(str(term) for term in self.terms)
