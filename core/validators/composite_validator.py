
from __future__ import annotations

"""
SanskritAI
==========

Composite Validator
-------------------

Coordinates multiple validators and merges their validation
results into a single immutable ValidationResult.

The composite validator does not implement domain rules.

It only orchestrates validators.
"""

from collections.abc import Iterable

from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)
from SanskritAI.core.validators.validator import Validator


class CompositeValidator:
    """
    Executes multiple validators and aggregates their results.
    """

    def __init__(
        self,
        validators: Iterable[Validator] = (),
    ) -> None:
        self._validators = tuple(validators)

    # =========================================================
    # Inspection
    # =========================================================

    @property
    def validators(self) -> tuple[Validator, ...]:
        """
        Return the registered validators.
        """

        return self._validators

    def __len__(self) -> int:
        return len(self._validators)

    def __iter__(self):
        return iter(self._validators)

    # =========================================================
    # Validation
    # =========================================================

    def validate(
        self,
        obj: object,
    ) -> ValidationResult:
        """
        Run every supporting validator and merge the results.

        Validators that do not support the supplied object are
        skipped.

        Validation is intentionally non-short-circuiting so that
        all applicable validation issues are reported.
        """

        result = ValidationResult.success()

        for validator in self._validators:

            if not validator.supports(obj):
                continue

            result = result.merge(
                validator.validate(obj)
            )

        return result

    # =========================================================
    # Batch validation
    # =========================================================

    def validate_many(
        self,
        objects: Iterable[object],
    ) -> ValidationResult:
        """
        Validate multiple objects and merge all results.
        """

        result = ValidationResult.success()

        for obj in objects:
            result = result.merge(
                self.validate(obj)
            )

        return result
