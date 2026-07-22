from __future__ import annotations

"""
SanskritAI
==========

Search Order

Defines the canonical ordering strategies for search results.

SearchOrder specifies how search results should be ranked,
sorted, or presented after matching.

Unlike SearchMode, which determines *how* a search is
performed, SearchOrder determines *how* matching results are
ordered.

Typical usages include:

- Alphabetical ordering
- Canonical corpus order
- Dictionary order
- Relevance ranking
- Semantic similarity
- Frequency ranking
- Chronological ordering

Architecture
------------

SearchOrder
      │
      ▼
SearchOptions
      │
      ▼
SearchQuery

Version
-------
v0.6.0
"""

from enum import Enum


class SearchOrder(str, Enum):
    """
    Canonical search result ordering strategies.
    """

    # ---------------------------------------------------------
    # Natural / Canonical
    # ---------------------------------------------------------

    NATURAL = "natural"

    CANONICAL = "canonical"

    # ---------------------------------------------------------
    # Alphabetical
    # ---------------------------------------------------------

    ALPHABETICAL_ASC = "alphabetical_asc"

    ALPHABETICAL_DESC = "alphabetical_desc"

    # ---------------------------------------------------------
    # Relevance
    # ---------------------------------------------------------

    RELEVANCE = "relevance"

    SCORE = "score"

    # ---------------------------------------------------------
    # AI / Semantic
    # ---------------------------------------------------------

    SIMILARITY = "similarity"

    CONFIDENCE = "confidence"

    # ---------------------------------------------------------
    # Statistical
    # ---------------------------------------------------------

    FREQUENCY = "frequency"

    POPULARITY = "popularity"

    # ---------------------------------------------------------
    # Temporal
    # ---------------------------------------------------------

    DATE_ASC = "date_asc"

    DATE_DESC = "date_desc"

    # ---------------------------------------------------------
    # Position
    # ---------------------------------------------------------

    POSITION = "position"

    CUSTOM = "custom"

    @property
    def is_alphabetical(self) -> bool:
        """
        Returns True if this ordering is alphabetical.
        """
        return self in {
            SearchOrder.ALPHABETICAL_ASC,
            SearchOrder.ALPHABETICAL_DESC,
        }

    @property
    def is_ai_ranking(self) -> bool:
        """
        Returns True if this ordering is AI-assisted.
        """
        return self in {
            SearchOrder.SIMILARITY,
            SearchOrder.CONFIDENCE,
        }

    @property
    def is_relevance_based(self) -> bool:
        """
        Returns True if this ordering depends on computed
        ranking scores.
        """
        return self in {
            SearchOrder.RELEVANCE,
            SearchOrder.SCORE,
            SearchOrder.SIMILARITY,
            SearchOrder.CONFIDENCE,
            SearchOrder.FREQUENCY,
            SearchOrder.POPULARITY,
        }
