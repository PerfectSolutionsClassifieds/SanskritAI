from __future__ import annotations

"""
SanskritAI
==========

Embedding Model

Defines the abstract semantic embedding model.

An EmbeddingModel converts semantic content into numerical
vector representations.

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


class EmbeddingModel(
    ABC,
    Displayable,
):
    """
    Abstract embedding model.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract embedding model."

    @abstractmethod
    def embed(
        self,
        text: str,
    ) -> tuple[float, ...]:
        """
        Produces an embedding vector.
        """
        raise NotImplementedError
