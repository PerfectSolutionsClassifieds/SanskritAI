from __future__ import annotations

"""
SanskritAI
==========

Validatable Contract

Defines the architectural contract for objects that support
validation.

This contract specifies *what* an object must provide in order
to participate in the SanskritAI validation framework, while
remaining independent of any specific validator
implementation.

Typical implementations include:

- Lexeme
- Synset
- DictionaryEntry
- Corpus
- Chapter
- Verse
- Token
- Records
- DTOs

Architecture
------------

Contract
      │
      ▼
Validatable

Version
-------
v0.6.0
"""

from abc import abstractmethod
from typing import TYPE_CHECKING

from SanskritAI.core.contracts.contract import Contract

if TYPE_CHECKING:
    from SanskritAI.core.validators.validation_result import (
        ValidationResult,
    )


class Validatable(Contract):
    """
    Architectural contract for validatable objects.
    """

    @abstractmethod
    def validate(self) -> "ValidationResult":
        """
        Validates this object and returns the validation result.

        Concrete implementations determine the validation
        strategy and delegate to the appropriate validator.
        """
        raise NotImplementedError

    @property
    def is_valid(self) -> bool:
        """
        Indicates whether this object is currently valid.

        The default implementation delegates to validate().
        """
        return self.validate().is_valid

    @property
    def can_validate(self) -> bool:
        """
        Indicates that this object supports validation.
        """
        return True
