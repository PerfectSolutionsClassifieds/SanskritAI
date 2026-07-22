from __future__ import annotations

"""
SanskritAI
==========

Amarakośa Parser

Abstract parser responsible for extracting structured
Amarakośa data from external sources.

Parsing and object construction are intentionally separated.

Version
-------
v0.4.0
"""

from abc import ABC, abstractmethod
from typing import Iterable


class AmarakoshaParser(ABC):
    """
    Base parser for Amarakośa sources.
    """

    @abstractmethod
    def parse(
        self,
        source: str,
    ) -> Iterable[dict]:
        """
        Parse a source and yield structured records.
        """
        raise NotImplementedError
