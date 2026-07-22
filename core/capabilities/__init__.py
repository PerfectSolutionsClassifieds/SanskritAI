"""
SanskritAI
==========

Capabilities Kernel

Defines the canonical runtime capability model used throughout
the SanskritAI architecture.

Capabilities describe *what a component advertises*, rather than
*how it is implemented*.

Unlike Contracts, capabilities are immutable metadata that can
be queried, negotiated, discovered, and composed at runtime.

Typical examples include:

- Sandhi
- Samāsa
- Morphology
- Tokenization
- Search
- Serialization
- AI Embeddings
- Vector Retrieval

Architecture
------------

Capability
      │
      ▼
CapabilitySet
      │
      ▼
CapabilityRegistry

Version
-------
v0.6.0
"""

from .capability import Capability
from .capability_set import CapabilitySet
from .capability_registry import CapabilityRegistry
from .capability_provider import CapabilityProvider

__all__ = [
    "Capability",
    "CapabilitySet",
    "CapabilityRegistry",
    "CapabilityProvider",
]
