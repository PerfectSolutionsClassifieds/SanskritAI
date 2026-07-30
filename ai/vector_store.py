from __future__ import annotations

"""
SanskritAI
==========

Vector Store

Defines the abstract semantic vector storage engine.

Concrete implementations may include:

    • pgvector
    • FAISS
    • ChromaDB
    • Milvus
    • Pinecone
    • Qdrant

Architecture
------------

EmbeddingModel
        │
        ▼
VectorStore

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable


class VectorStore(
    ABC,
    Displayable,
):
    """
    Abstract vector store.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract vector store."

    @abstractmethod
    def add(
        self,
        identifier: str,
        embedding: tuple[float, ...],
    ) -> None:
        """
        Stores an embedding.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        embedding: tuple[float, ...],
        limit: int = 10,
    ) -> tuple[str, ...]:
        """
        Performs semantic similarity search.
        """
        raise NotImplementedError
