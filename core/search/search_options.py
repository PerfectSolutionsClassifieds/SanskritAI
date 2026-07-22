from __future__ import annotations

"""
SanskritAI
==========

Search Options

Defines immutable configuration options controlling the
behaviour of search operations.

SearchOptions specifies *how* a search should be executed,
independent of the actual query text.

Typical usages include:

- Exact vs. fuzzy search
- Corpus-specific search
- Language filtering
- Result ordering
- Case sensitivity

Architecture
------------

ValueObject
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

from dataclasses import dataclass

from SanskritAI.core.search.search_language import SearchLanguage
from SanskritAI.core.search.search_mode import SearchMode
from SanskritAI.core.search.search_operator import SearchOperator
from SanskritAI.core.search.search_order import SearchOrder
from SanskritAI.core.search.search_scope import SearchScope
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(slots=True, frozen=True)
class SearchOptions(ValueObject):
    """
    Immutable search configuration.
    """

    mode: SearchMode = SearchMode.EXACT

    operator: SearchOperator = SearchOperator.AND

    scope: SearchScope = SearchScope.ALL

    language: SearchLanguage = SearchLanguage.AUTO

    order: SearchOrder = SearchOrder.RELEVANCE

    case_sensitive: bool = False

    diacritic_sensitive: bool = True

    whole_word: bool = False

    include_metadata: bool = False

    limit: int | None = None

    offset: int = 0

    @property
    def is_paged(self) -> bool:
        """
        Returns True if result pagination is enabled.
        """
        return self.limit is not None

    @property
    def is_exact(self) -> bool:
        """
        Returns True if exact matching is requested.
        """
        return self.mode is SearchMode.EXACT

    @property
    def is_semantic(self) -> bool:
        """
        Returns True if semantic retrieval is requested.
        """
        return self.mode.is_semantic
