"""
SanskritAI
==========

Acquisition ImportResult Compatibility Module

The canonical ImportResult lives in:

    SanskritAI.models.imports.import_result

This module intentionally contains no second ImportResult
implementation.

It exists only to preserve existing acquisition-layer imports.
"""

from SanskritAI.models.imports.import_result import (
    ImportResult,
)

__all__ = [
    "ImportResult",
]
