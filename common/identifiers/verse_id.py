from __future__ import annotations

"""
SanskritAI
==========

Verse Identifier

Strongly typed identifier for Verse objects.
"""

from dataclasses import dataclass

from SanskritAI.common.identifiers.base_identifier import BaseIdentifier


@dataclass(frozen=True, slots=True)
class VerseId(BaseIdentifier):
    """
    Identifier for a Verse.
    """
    pass
