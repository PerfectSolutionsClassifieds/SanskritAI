from __future__ import annotations

"""
URI

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.location.location import Location
from SanskritAI.core.location.location_kind import LocationKind


@dataclass(frozen=True, slots=True)
class URI(Location):
    """
    Immutable URI.
    """

    def __init__(self, value: str):
        super().__init__(
            value=value,
            kind=LocationKind.URI,
        )
