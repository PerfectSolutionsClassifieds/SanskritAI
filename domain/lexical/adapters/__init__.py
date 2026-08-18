from __future__ import annotations

"""
SanskritAI
==========

Lexical Adapters
----------------
"""

from .in_memory_monier_williams_adapter import (
    InMemoryMonierWilliamsAdapter,
)
from .monier_williams_adapter import (
    MonierWilliamsAdapter,
)
from .monier_williams_record import (
    MonierWilliamsRecord,
)

__all__ = [
    "InMemoryMonierWilliamsAdapter",
    "MonierWilliamsAdapter",
    "MonierWilliamsRecord",
]
