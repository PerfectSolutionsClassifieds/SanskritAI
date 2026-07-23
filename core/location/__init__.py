"""
SanskritAI
==========

Location Kernel

Provides immutable abstractions for identifying locations of
resources throughout the SanskritAI framework.

Architecture
------------

LocationKind
      │
      ▼
Location
      ├── Path
      └── URI
"""

from SanskritAI.core.location.location import Location
from SanskritAI.core.location.location_kind import LocationKind
from SanskritAI.core.location.path import Path
from SanskritAI.core.location.uri import URI

__all__ = [
    "Location",
    "LocationKind",
    "Path",
    "URI",
]
