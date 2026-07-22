from __future__ import annotations

"""
SanskritAI
==========

Section Identifier

Strongly typed identifier for Section objects.
"""

from dataclasses import dataclass

from SanskritAI.common.identifiers.base_identifier import BaseIdentifier


@dataclass(frozen=True, slots=True)
class SectionId(BaseIdentifier):
    """
    Identifier for a Section.
    """
    pass
