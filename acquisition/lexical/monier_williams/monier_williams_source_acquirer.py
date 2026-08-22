
from __future__ import annotations

from abc import ABC, abstractmethod


class MonierWilliamsSourceAcquirer(ABC):
    """
    Abstract source-acquisition boundary for Monier–Williams data.

    Acquisition is deliberately separated from parsing so that the same
    parser can consume local files, downloaded archives, packaged resources,
    or future remote acquisition mechanisms.
    """

    @abstractmethod
    def acquire(self) -> str:
        """
        Acquire and return the raw Monier–Williams source as text.
        """
        raise NotImplementedError
