
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Parser Contract
--------------------------------
"""

from abc import ABC, abstractmethod
from typing import Iterable


class MonierWilliamsParser(ABC):
    """
    Base contract for MW acquisition-stage parsers.
    """

    @abstractmethod
    def parse(self, source_text: str):
        raise NotImplementedError

    def parse_lines(self, lines: Iterable[str]):
        if lines is None:
            raise TypeError("lines must not be None")

        return self.parse("\n".join(lines))
