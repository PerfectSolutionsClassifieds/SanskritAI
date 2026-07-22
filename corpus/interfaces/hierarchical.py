from __future__ import annotations

"""
Hierarchical protocol.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Hierarchical(Protocol):
    """
    Object participating in a parent-child hierarchy.
    """

    @property
    def parent(self):
        ...

    @parent.setter
    def parent(
        self,
        value,
    ) -> None:
        ...
