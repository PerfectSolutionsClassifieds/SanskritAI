from __future__ import annotations

"""
SanskritAI
==========

Search Scope

Defines the canonical search scopes supported by the
SanskritAI Search Kernel.

A SearchScope specifies *where* a query should be executed.

Architecture
------------

SearchScope
      │
      ▼
SearchQuery

Version
-------
v0.6.0
"""

from enum import Enum


class SearchScope(str, Enum):
    """
    Canonical search scopes.
    """

    # ---------------------------------------------------------
    # Global
    # ---------------------------------------------------------

    ALL = "all"

    # ---------------------------------------------------------
    # Canonical corpus
    # ---------------------------------------------------------

    CORPUS = "corpus"

    # ---------------------------------------------------------
    # Lexical resources
    # ---------------------------------------------------------

    DICTIONARY = "dictionary"

    LEXICON = "lexicon"

    AMARAKOSHA = "amarakosha"

    # ---------------------------------------------------------
    # Linguistics
    # ---------------------------------------------------------

    GRAMMAR = "grammar"

    MORPHOLOGY = "morphology"

    SYNTAX = "syntax"

    SEMANTICS = "semantics"

    # ---------------------------------------------------------
    # Knowledge layer
    # ---------------------------------------------------------

    KNOWLEDGE = "knowledge"

    ONTOLOGY = "ontology"

    # ---------------------------------------------------------
    # Infrastructure
    # ---------------------------------------------------------

    REGISTRY = "registry"

    PLUGINS = "plugins"

    CONFIGURATION = "configuration"

    # ---------------------------------------------------------
    # AI
    # ---------------------------------------------------------

    VECTOR_INDEX = "vector_index"

    EMBEDDINGS = "embeddings"

    RAG = "rag"

    @property
    def is_ai_scope(self) -> bool:
        """
        Returns True if the scope targets AI retrieval systems.
        """
        return self in {
            SearchScope.VECTOR_INDEX,
            SearchScope.EMBEDDINGS,
            SearchScope.RAG,
        }

    @property
    def is_linguistic(self) -> bool:
        """
        Returns True if the scope targets linguistic resources.
        """
        return self in {
            SearchScope.DICTIONARY,
            SearchScope.LEXICON,
            SearchScope.AMARAKOSHA,
            SearchScope.GRAMMAR,
            SearchScope.MORPHOLOGY,
            SearchScope.SYNTAX,
            SearchScope.SEMANTICS,
        }
