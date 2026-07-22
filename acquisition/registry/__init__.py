
"""
SanskritAI
==========

Acquisition Registry

Provides the central registry for all corpus sources known to
SanskritAI.

The registry subsystem is responsible for:

    • Maintaining the catalog of available corpus sources.
    • Registering and unregistering sources.
    • Looking up sources by identifier.
    • Enumerating available sources.
    • Serving as the discovery mechanism for the acquisition
      framework.

This package intentionally contains no downloading or importing
logic. It is purely a registry of metadata.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from .source_catalog import SourceCatalog
from .source_registry import SourceRegistry

__all__ = [
    "SourceCatalog",
    "SourceRegistry",
]
