from __future__ import annotations

"""
Lexical Status
==============

Lifecycle state of a lexical object.
"""

from enum import Enum


class LexicalStatus(str, Enum):

    UNKNOWN = "unknown"

    DRAFT = "draft"

    VERIFIED = "verified"

    REVIEWED = "reviewed"

    CANONICAL = "canonical"

    DEPRECATED = "deprecated"
