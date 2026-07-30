from __future__ import annotations

"""
SanskritAI
==========

Knowledge Retriever

Defines the abstract knowledge retrieval engine.

A KnowledgeRetriever coordinates semantic retrieval from
one or more knowledge sources.

Concrete implementations may retrieve knowledge from:

    • Vector databases
    • Knowledge graphs
    • SQL databases
    • Sanskrit lexical resources
    • Hybrid retrieval systems

Architecture
------------

KnowledgeContext
        ▲
        │
KnowledgeRetriever
        │
        ├── EmbeddingModel
        └── VectorStore

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.ai.knowledge_context import KnowledgeContext
from SanskritAI.core.mixins.displayable import Displayable


class KnowledgeRetriever(
    ABC,
    Displayable,
):
    """
    Abstract semantic knowledge retriever.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract semantic knowledge retriever."

    @abstractmethod
    def retrieve(
        self,
        query: str,
    ) -> KnowledgeContext:
        """
        Retrieves the most relevant knowledge context.
        """
        raise NotImplementedError
