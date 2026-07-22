from __future__ import annotations

"""
SanskritAI
==========

Base Knowledge Validator

Abstract validator for knowledge-layer domain objects.

Version
-------
v0.4.0
"""

from abc import ABC
from typing import Generic

from SanskritAI.core.typing import TObject
from SanskritAI.core.validators.validator import Validator


class BaseKnowledgeValidator(
    Validator[TObject],
    Generic[TObject],
    ABC,
):
    """
    Base class for all knowledge-layer validators.
    """

    pass
