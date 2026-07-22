from __future__ import annotations

"""
SanskritAI
==========

Build Result

Immutable result returned by validated builders.

A BuildResult combines:

    • ValidationResult
    • Constructed object (if successful)

This avoids exception-driven control flow during normal
validation and construction.

Version
-------
v0.4.0
"""

from dataclasses import dataclass
from typing import Generic

from SanskritAI.core.typing import TObject
from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)


@dataclass(slots=True, frozen=True)
class BuildResult(Generic[TObject]):
    """
    Immutable result of a build operation.
    """

    object: TObject | None

    validation: ValidationResult

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    @property
    def is_success(self) -> bool:
        """
        True when validation succeeded and an object exists.
        """
        return (
            self.validation.is_valid
            and self.object is not None
        )

    @property
    def has_object(self) -> bool:
        """
        True if a domain object was successfully built.
        """
        return self.object is not None

    @property
    def has_errors(self) -> bool:
        """
        True if validation produced errors.
        """
        return self.validation.has_errors

    # ---------------------------------------------------------
    # Convenience constructors
    # ---------------------------------------------------------

    @classmethod
    def success(
        cls,
        obj: TObject,
    ) -> "BuildResult[TObject]":
        """
        Construct a successful build result.
        """
        return cls(
            object=obj,
            validation=ValidationResult.success(),
        )

    @classmethod
    def failure(
        cls,
        validation: ValidationResult,
    ) -> "BuildResult[TObject]":
        """
        Construct a failed build result.
        """
        return cls(
            object=None,
            validation=validation,
        )
