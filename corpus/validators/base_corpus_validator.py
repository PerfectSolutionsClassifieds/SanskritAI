from __future__ import annotations

"""
SanskritAI
==========

Base Corpus Validator

Abstract validator for Corpus domain objects.

Version
-------
v0.4.0
"""

from abc import ABC
from typing import Generic

from SanskritAI.core.typing import TObject
from SanskritAI.core.validators.validator import Validator


class BaseCorpusValidator(
    Validator[TObject],
    Generic[TObject],
    ABC,
):
    """
    Base class for all corpus validators.
    """

    pass
