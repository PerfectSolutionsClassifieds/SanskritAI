from __future__ import annotations

"""
SanskritAI
==========

Token Identifier

Strongly typed identifier for Token objects.
"""

from dataclasses import dataclass

from SanskritAI.common.identifiers.base_identifier import BaseIdentifier


@dataclass(frozen=True, slots=True)
class TokenId(BaseIdentifier):
    """
    Identifier for a Token.
    """
    pass
