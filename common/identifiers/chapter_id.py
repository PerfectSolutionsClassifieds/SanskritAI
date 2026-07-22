from __future__ import annotations

"""
SanskritAI
==========

Chapter Identifier

Strongly typed identifier for Chapter objects.
"""

from dataclasses import dataclass

from SanskritAI.common.identifiers.base_identifier import BaseIdentifier


@dataclass(frozen=True, slots=True)
class ChapterId(BaseIdentifier):
    """
    Identifier for a Chapter.
    """
    pass
