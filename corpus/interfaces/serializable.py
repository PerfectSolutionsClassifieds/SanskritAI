from __future__ import annotations

"""
Serializable protocol.
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Serializable(Protocol):
    """
    Object capable of serializing itself.
    """

    def to_dict(self) -> dict[str, Any]:
        ...
