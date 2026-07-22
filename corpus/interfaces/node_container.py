from __future__ import annotations

"""
NodeContainer protocol.
"""

from typing import Any, Iterable, Protocol, runtime_checkable


@runtime_checkable
class NodeContainer(Protocol):
    """
    Generic protocol implemented by container nodes.
    """

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterable[Any]:
        ...
