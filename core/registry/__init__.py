"""
SanskritAI
==========

Core Registry Kernel

Provides the canonical registry framework used throughout the
SanskritAI architecture.

The Registry Kernel offers a consistent mechanism for
registering, discovering, organizing, and retrieving reusable
architectural components.

Typical registry contents include:

- Builders
- Validators
- Parsers
- Tokenizers
- Dictionaries
- Corpora
- Knowledge Bases
- Plugins
- AI Models
- Processing Engines

Architecture
------------

Registry
    ├── MutableRegistry
    ├── ImmutableRegistry
    ├── TypedRegistry
    ├── HierarchicalRegistry
    └── OrderedRegistry

Version
-------
v0.6.0
"""

__all__ = [
    "Registry",
]
