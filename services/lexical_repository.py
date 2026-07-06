"""
SanskritAI
==========

Compatibility Wrapper

Historically, SanskritAI exposed a concrete
LexicalRepository implementation directly from
this module.

Beginning with v0.3.0 Final, the repository layer
uses an abstract interface with interchangeable
storage backends.

Existing code importing

    from services.lexical_repository import LexicalRepository

will continue to function without modification.

Version:
    v0.3.0 Final
"""

from services.repositories.memory_lexical_repository import (
    MemoryLexicalRepository,
)

# ---------------------------------------------------------------------
# Backward-compatible alias
# ---------------------------------------------------------------------

LexicalRepository = MemoryLexicalRepository

__all__ = [
    "LexicalRepository",
]
