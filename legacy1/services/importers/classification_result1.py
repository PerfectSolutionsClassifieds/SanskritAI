
"""
SanskritAI
==========

Module:
    services.importers.classification_result

Description
-----------
Rich metadata value object wrapped around tokenized lexical outputs. 
Ensures the core engine evaluates strongly-typed data objects instead of raw strings.

Version
-------
v0.5.0-alpha
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from services.importers.line_classifier import LineType


@dataclass(frozen=True, slots=True)
class ClassificationResult:
    """
    Carries complete semantic and lexical classification metadata 
    extracted from a corpus line.
    """
    line_type: LineType
    content: str
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
