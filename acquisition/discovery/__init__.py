
"""
SanskritAI
==========

Corpus Discovery Framework

The discovery subsystem is responsible for locating available
Sanskrit corpus resources from local repositories and remote
providers.

Responsibilities
----------------
* Discover available corpus sources
* Enumerate downloadable resources
* Produce discovery metadata
* Build acquisition manifests

Discovery intentionally does NOT perform:

    • downloading
    • validation
    • normalization
    • importing
    • parsing

Those responsibilities belong to subsequent acquisition stages.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from .base_discovery_provider import BaseDiscoveryProvider
from .discovery_manager import DiscoveryManager
from .discovery_result import DiscoveryResult

__all__ = [
    "BaseDiscoveryProvider",
    "DiscoveryManager",
    "DiscoveryResult",
]
