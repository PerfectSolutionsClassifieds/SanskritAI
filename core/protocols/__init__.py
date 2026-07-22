"""
SanskritAI
==========

Core Protocols

Defines structural typing protocols (PEP 544) used throughout
the SanskritAI architecture.

Protocols differ from Contracts:

- Contracts describe semantic capabilities.
- Protocols describe structural compatibility.

Protocols enable dependency inversion and loose coupling
without requiring inheritance.

Version
-------
v0.6.0
"""

from .protocol import Protocol

from .supports_lookup import SupportsLookup
from .supports_processing import SupportsProcessing
from .supports_registry import SupportsRegistry
from .supports_search import SupportsSearch
from .supports_serialization import SupportsSerialization

__all__ = [
    "Protocol",
    "SupportsLookup",
    "SupportsProcessing",
    "SupportsRegistry",
    "SupportsSearch",
    "SupportsSerialization",
]
