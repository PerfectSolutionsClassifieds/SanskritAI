from __future__ import annotations

"""
Identifiable protocol.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Identifiable(Protocol):
    """
    Any object possessing a canonical identifier.
    """

    @property
    def id(self):
        ...
