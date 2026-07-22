from __future__ import annotations

"""
SanskritAI
==========

Base Lexical Validator

Abstract base validator for all lexical domain objects.

Version
-------
v0.4.0
"""

from abc import ABC
from typing import Generic

from SanskritAI.core.typing import TObject
from SanskritAI.core.validators.validator import Validator


class BaseLexicalValidator(
    Validator[TObject],
    Generic[TObject],
    ABC,
):
    """
    Base class for lexical validators.
    """

    pass
