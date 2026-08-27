from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Contract
-------------------------------

Defines the acquisition boundary for Monier-Williams source data.

The source layer is responsible only for obtaining source content.
It must not perform lexical normalization, repository writes, or
linguistic reasoning.
"""

from abc import ABC, abstractmethod


class MonierWilliamsSource(ABC):
    """Abstract acquisition contract for Monier-Williams data."""

    SOURCE = "monier-williams"

    @property
    def source(self) -> str:
        return self.SOURCE

    @property
    def identifier(self) -> str:
        return self.SOURCE

    @property
    def source_name(self) -> str:
        return "Monier-Williams"

    @abstractmethod
    def read(self) -> str:
        """Return the complete raw source representation."""
        raise NotImplementedError

    def acquire(self) -> str:
        """Compatibility alias for ``read()``."""
        return self.read()
