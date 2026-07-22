from __future__ import annotations

"""
MetadataProvider protocol.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class MetadataProvider(Protocol):
    """
    Object exposing metadata.
    """

    @property
    def metadata(self):
        ...
