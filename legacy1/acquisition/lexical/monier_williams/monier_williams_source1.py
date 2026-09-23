
from __future__ import annotations

from abc import ABC, abstractmethod


class MonierWilliamsSource(ABC):
    """
    Acquisition boundary for a Monier-Williams source.

    The primary contract is acquire().

    Metadata such as identifier and source_name are deliberately concrete
    defaults so lightweight test doubles and future acquisition providers
    do not have to implement unnecessary methods.
    """

    source: str = "monier-williams"

    @property
    def source_name(self) -> str:
        return self.source

    @property
    def identifier(self) -> str:
        return self.source

    @abstractmethod
    def acquire(self) -> str:
        """
        Return the raw source content.
        """
        raise NotImplementedError
