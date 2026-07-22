from __future__ import annotations

"""
SanskritAI
==========

Search Mode

Defines the canonical search modes supported by the SanskritAI
Search Kernel.

SearchMode specifies *how* a query should be interpreted,
independent of the underlying search engine.

The enumeration is intentionally future-proof, supporting both
traditional lexical search and modern AI-assisted retrieval.

Typical usages include:

- Dictionary lookup
- Corpus search
- Grammar search
- Knowledge retrieval
- Semantic search (RAG)
- Vector database search

Architecture
------------

SearchMode
      │
      ▼
SearchQuery
      │
      ▼
SearchResult

Version
-------
v0.6.0
"""

from enum import Enum


class SearchMode(str, Enum):
    """
    Canonical search modes.
    """

    # ---------------------------------------------------------
    # Exact lexical matching
    # ---------------------------------------------------------

    EXACT = "exact"

    # ---------------------------------------------------------
    # Prefix matching
    # ---------------------------------------------------------

    PREFIX = "prefix"

    # ---------------------------------------------------------
    # Suffix matching
    # ---------------------------------------------------------

    SUFFIX = "suffix"

    # ---------------------------------------------------------
    # Substring matching
    # ---------------------------------------------------------

    CONTAINS = "contains"

    # ---------------------------------------------------------
    # Regular expression search
    # ---------------------------------------------------------

    REGEX = "regex"

    # ---------------------------------------------------------
    # Approximate / fuzzy search
    # ---------------------------------------------------------

    FUZZY = "fuzzy"

    # ---------------------------------------------------------
    # Wildcard search
    # ---------------------------------------------------------

    WILDCARD = "wildcard"

    # ---------------------------------------------------------
    # Full-text search
    # ---------------------------------------------------------

    FULL_TEXT = "full_text"

    # ---------------------------------------------------------
    # Semantic (embedding-based) search
    # ---------------------------------------------------------

    SEMANTIC = "semantic"

    # ---------------------------------------------------------
    # Pure vector similarity search
    # ---------------------------------------------------------

    VECTOR = "vector"

    # ---------------------------------------------------------
    # Hybrid lexical + semantic search
    # ---------------------------------------------------------

    HYBRID = "hybrid"

    @property
    def is_lexical(self) -> bool:
        """
        Returns True if this is a lexical search mode.
        """
        return self in {
            SearchMode.EXACT,
            SearchMode.PREFIX,
            SearchMode.SUFFIX,
            SearchMode.CONTAINS,
            SearchMode.REGEX,
            SearchMode.FUZZY,
            SearchMode.WILDCARD,
            SearchMode.FULL_TEXT,
        }

    @property
    def is_semantic(self) -> bool:
        """
        Returns True if this mode uses semantic representations.
        """
        return self in {
            SearchMode.SEMANTIC,
            SearchMode.VECTOR,
            SearchMode.HYBRID,
        }

    @property
    def is_ai_ready(self) -> bool:
        """
        Returns True if this mode is intended for AI-assisted
        retrieval.
        """
        return self in {
            SearchMode.SEMANTIC,
            SearchMode.VECTOR,
            SearchMode.HYBRID,
        }
