
"""
SanskritAI
==========

Corpus Discovery Registry

The registry subsystem maintains the collection of available
discovery providers.

Responsibilities
----------------
* Register discovery providers
* Remove providers
* Enumerate providers
* Lookup providers by name

The registry intentionally does NOT:

    • execute discovery
    • download resources
    • validate files
    • normalize content
    • import corpora

Those responsibilities belong to the DiscoveryManager.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from .discovery_registry import DiscoveryRegistry

__all__ = [
    "DiscoveryRegistry",
]
