from __future__ import annotations

"""
SanskritAI
==========

Validated Builder

Coordinates validation and object construction.

Pipeline
--------

Record
    ↓
Validator
    ↓
ValidationResult
    ↓
ValidatedBuilder
    ↓
BuildResult

Version
-------
v0.4.0
"""

from abc import ABC, abstractmethod
from typing import Generic, Iterable

from SanskritAI.core.builders.build_result import (
    BuildResult,
)
from SanskritAI.core.records.data_record import (
    DataRecord,
)
from SanskritAI.core.typing import TObject, TIdentifier
from SanskritAI.core.validators.validator import (
    Validator,
)


class ValidatedBuilder(
    Generic[TIdentifier, TObject],
    ABC,
):
    """
    Abstract builder that validates records before building
    domain objects.
    """

    def __init__(
        self,
        validator: Validator[DataRecord[TIdentifier]],
    ) -> None:
        self._validator = validator

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        record: DataRecord[TIdentifier],
    ):
        """
        Validate a record.
        """
        return self._validator.validate(record)

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    @abstractmethod
    def build(
        self,
        record: DataRecord[TIdentifier],
    ) -> TObject:
        """
        Build a domain object from a validated record.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Orchestration
    # ---------------------------------------------------------

    def build_validated(
        self,
        record: DataRecord[TIdentifier],
    ) -> BuildResult[TObject]:
        """
        Validate the record before building.
        """

        validation = self.validate(record)

        if not validation.is_valid:
            return BuildResult.failure(validation)

        obj = self.build(record)

        return BuildResult.success(obj)

    # ---------------------------------------------------------
    # Batch construction
    # ---------------------------------------------------------

    def build_many(
        self,
        records: Iterable[DataRecord[TIdentifier]],
    ) -> list[BuildResult[TObject]]:
        """
        Build multiple records.
        """
        return [
            self.build_validated(record)
            for record in records
        ]
