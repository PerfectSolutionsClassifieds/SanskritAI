from __future__ import annotations

"""
SanskritAI
==========

Line Identifier

Strongly typed identifier for Line objects.
"""

from dataclasses import dataclass

from SanskritAI.common.identifiers.base_identifier import BaseIdentifier


@dataclass(frozen=True, slots=True)
class LineId(BaseIdentifier):
    """
    Identifier for a Line.
    """
    pass
