
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source
----------------------

Abstract source contract for the acquisition layer.
"""

from abc import ABC, abstractmethod


class MonierWilliamsSource(ABC):
    """
    Boundary between a physical MW source and acquisition services.
    """

    @property
    def source(self) -> str:
        return "monier-williams"

    @property
    def source_name(self) -> str:
        return "Monier-Williams"

    @property
    def identifier(self) -> str:
        return "monier-williams"

    @abstractmethod
    def acquire(self) -> str:
        """
        Acquire the complete raw source text.
        """
        raise NotImplementedError

    def read(self) -> str:
        """
        Compatibility/convenience alias for acquire().
        """
        return self.acquire()
