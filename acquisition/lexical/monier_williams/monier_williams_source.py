from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Contract
-------------------------------

Defines the acquisition boundary for the Monier-Williams
dictionary.

The source layer is responsible only for obtaining source
content.

It must not:

* construct DictionaryEntry
* construct DictionarySense
* perform lexical reasoning
* perform Sanskrit normalization
* perform repository writes

Those responsibilities belong to later layers.
"""

from abc import ABC, abstractmethod


class MonierWilliamsSource(ABC):
    """
    Abstract source acquisition contract for Monier-Williams data.
    """

    SOURCE = "monier-williams"

    @property
    def source(self) -> str:
        """
        Return the canonical source identifier.
        """
        return self.SOURCE

    @abstractmethod
    def read(self) -> str:
        """
        Read the complete source representation.

        Returns
        -------
        str
            Raw source content.
        """
        raise NotImplementedError
