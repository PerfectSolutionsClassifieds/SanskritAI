from __future__ import annotations

"""
SanskritAI
==========

Validator

Defines the abstract validation contract shared across the
entire SanskritAI platform.

Validators are responsible for validating domain objects or
records and returning immutable ValidationResult objects.

Typical validation pipeline
---------------------------

Parser
    ↓
Record
    ↓
Validator
    ↓
Builder
    ↓
Repository / Registry

Version
-------
v0.4.0
"""

from abc import ABC, abstractmethod
from typing import Generic, Iterable

from SanskritAI.core.typing import TObject
from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)


class Validator(
    Generic[TObject],
    ABC,
):
    """
    Abstract validator.
    """

    # ---------------------------------------------------------
    # Single-object validation
    # ---------------------------------------------------------

    @abstractmethod
    def validate(
        self,
        obj: TObject,
    ) -> ValidationResult:
        """
        Validate a single object.

        Parameters
        ----------
        obj
            Object to validate.

        Returns
        -------
        ValidationResult
            Immutable validation report.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Batch validation
    # ---------------------------------------------------------

    def validate_many(
        self,
        objects: Iterable[TObject],
    ) -> ValidationResult:
        """
        Validate multiple objects and merge the results.
        """

        result = ValidationResult.success()

        for obj in objects:
            result = result.merge(
                self.validate(obj)
            )

        return result

    # ---------------------------------------------------------
    # Capability
    # ---------------------------------------------------------

    @classmethod
    def supports(
        cls,
        obj: object,
    ) -> bool:
        """
        Indicates whether this validator supports the given
        object.

        Concrete validators may override this method.
        """
        return True
