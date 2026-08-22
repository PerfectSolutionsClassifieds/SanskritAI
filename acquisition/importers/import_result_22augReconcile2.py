"""
SanskritAI
==========

Acquisition Import Result

Compatibility import for the canonical SanskritAI ImportResult.

The canonical implementation lives in:

    SanskritAI.models.imports.import_result

All acquisition importers should continue to import ImportResult
from this module for compatibility with the acquisition package.

There is intentionally no second ImportResult implementation here.

Version
-------
v0.9.0
"""

from SanskritAI.models.imports.import_result import (
    ImportResult,
)

__all__ = [
    "ImportResult",
]
