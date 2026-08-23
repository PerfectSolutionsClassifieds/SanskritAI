
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Source Definition

Defines the canonical Monier-Williams Sanskrit-English Dictionary
source used by SanskritAI.

Important
---------
This module describes the source.

It does NOT:
    - download the source
    - parse MW records
    - normalize dictionary entries
    - persist lexical data

Those responsibilities belong to the acquisition and lexical
processing layers respectively.
"""

from dataclasses import dataclass

from SanskritAI.domain.acquisition.source_format import SourceFormat
from SanskritAI.domain.acquisition.source_type import SourceType


@dataclass(frozen=True)
class MonierWilliamsSource:
    """
    Canonical description of the Monier-Williams dictionary source.
    """

    source_id: str = "monier-williams"

    name: str = (
        "Monier Monier-Williams Sanskrit-English Dictionary"
    )

    source_type: SourceType = SourceType.CORPUS

    source_format: SourceFormat = SourceFormat.TEXT

    encoding: str = "slp1"

    language: str = "sa"

    year: int = 1899

    author: str = "Monier Monier-Williams"

    title: str = (
        "A Sanskrit-English Dictionary"
    )

    publisher: str = (
        "Clarendon Press, Oxford"
    )

    def identity(self) -> str:
        """
        Return the stable source identifier.
        """

        return self.source_id
