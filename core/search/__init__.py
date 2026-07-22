"""
SanskritAI
==========

Core Search Kernel

Provides the foundational abstractions for search operations
throughout the SanskritAI platform.

The Search Kernel supplies immutable value objects describing
search requests, search matches, search results, and search
configuration. It serves as the common vocabulary shared by
corpus management, lexical resources, grammatical analysis,
knowledge repositories, and future AI retrieval systems.

Architecture
------------

SearchMode
        │
        ▼
SearchOperator
        │
        ▼
SearchOptions
        │
        ▼
SearchQuery
        │
        ▼
SearchMatch
        │
        ▼
SearchResult

Future integrations include:

- Corpus Search
- Dictionary Search
- Amarakośa Search
- Grammar Search
- Knowledge Repository Search
- PostgreSQL Full-Text Search
- pgvector Semantic Search
- Elasticsearch
- AI Retrieval (RAG)

Version
-------
v0.6.0
"""

from .search_mode import SearchMode
from .search_operator import SearchOperator
from .search_options import SearchOptions
from .search_query import SearchQuery
from .search_match import SearchMatch
from .search_result import SearchResult

__all__ = [
    "SearchMode",
    "SearchOperator",
    "SearchOptions",
    "SearchQuery",
    "SearchMatch",
    "SearchResult",
]
