from __future__ import annotations

"""
SanskritAI
==========

Paragraph Identifier

Strongly typed identifier for Paragraph objects.
"""

from dataclasses import dataclass

from SanskritAI.common.identifiers.base_identifier import BaseIdentifier


@dataclass(frozen=True, slots=True)
class ParagraphId(BaseIdentifier):
    """
    Identifier for a Paragraph.
    """
    pass
