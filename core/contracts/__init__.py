"""
SanskritAI
==========

Core Contracts Kernel

Defines the architectural contracts that describe the core
capabilities of SanskritAI components.

Contracts are intentionally lightweight and independent of any
specific implementation. They define *what* a component must
provide, while concrete classes define *how* those capabilities
are implemented.

Typical contracts include:

- Identifiable
- Serializable
- Parsable
- Buildable
- Validatable
- Displayable
- Searchable

Architecture
------------

Contracts
      │
      ├── Identifiable
      ├── Serializable
      ├── Parsable
      ├── Buildable
      ├── Validatable
      ├── Displayable
      └── Searchable

Version
-------
v0.6.0
"""

__all__ = [
    "Identifiable",
]
