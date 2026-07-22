"""
SanskritAI
==========

Serialization Kernel

Provides a unified serialization infrastructure for immutable
objects throughout the SanskritAI architecture.

The Serialization Kernel is intentionally format-independent.
Concrete serializers (JSON, Dictionary, YAML, etc.) are built
on top of the common interfaces defined here.

Shared By
---------

- Records
- DTOs
- Tokenizer
- Diagnostics
- Validators
- Builders
- Corpus
- Lexical
- Amarakośa
- Morphological Engine
- Future APIs

Architecture
------------

Serializable
        │
        ▼
Serializer
        │
        ▼
SerializationResult
        │
        ▼
Concrete Serializer

Version
-------
v0.6.0
"""

from .serializable import Serializable
from .serializer import Serializer
from .serialization_format import SerializationFormat
from .serialization_result import SerializationResult

__all__ = [
    "Serializable",
    "Serializer",
    "SerializationFormat",
    "SerializationResult",
]
