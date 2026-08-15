
from __future__ import annotations

from dataclasses import dataclass

from SanskritAI.core.validators.composite_validator import (
    CompositeValidator,
)
from SanskritAI.core.validators.validation_issue import (
    ValidationIssue,
    ValidationSeverity,
)
from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)
from SanskritAI.core.validators.validator import Validator


@dataclass(frozen=True)
class DummyObject:
    identifier: str


class IdentifierValidator(Validator):

    @classmethod
    def supports(cls, obj: object) -> bool:
        return isinstance(obj, DummyObject)

    def validate(
        self,
        obj: DummyObject,
    ) -> ValidationResult:

        if obj.identifier:
            return ValidationResult.success()

        return ValidationResult.from_issues(
            (
                ValidationIssue(
                    code="TEST001",
                    message="Identifier is required.",
                    severity=ValidationSeverity.ERROR,
                    field="identifier",
                ),
            )
        )


class AlwaysErrorValidator(Validator):

    @classmethod
    def supports(cls, obj: object) -> bool:
        return isinstance(obj, DummyObject)

    def validate(
        self,
        obj: DummyObject,
    ) -> ValidationResult:

        return ValidationResult.from_issues(
            (
                ValidationIssue(
                    code="TEST002",
                    message="Test validation failure.",
                    severity=ValidationSeverity.ERROR,
                    field="test",
                ),
            )
        )


class UnsupportedValidator(Validator):

    @classmethod
    def supports(cls, obj: object) -> bool:
        return False

    def validate(
        self,
        obj,
    ) -> ValidationResult:

        raise AssertionError(
            "Unsupported validator must not be executed."
        )


def test_empty_composite_is_valid():

    composite = CompositeValidator()

    result = composite.validate(
        DummyObject("राम")
    )

    assert result.is_valid
    assert result.issues == ()


def test_valid_object_passes_all_validators():

    composite = CompositeValidator(
        (
            IdentifierValidator(),
        )
    )

    result = composite.validate(
        DummyObject("राम")
    )

    assert result.is_valid
    assert result.issues == ()


def test_invalid_object_reports_issue():

    composite = CompositeValidator(
        (
            IdentifierValidator(),
        )
    )

    result = composite.validate(
        DummyObject("")
    )

    assert not result.is_valid

    assert {
        issue.code
        for issue in result.issues
    } == {
        "TEST001",
    }


def test_multiple_validators_are_aggregated():

    composite = CompositeValidator(
        (
            IdentifierValidator(),
            AlwaysErrorValidator(),
        )
    )

    result = composite.validate(
        DummyObject("")
    )

    assert {
        issue.code
        for issue in result.issues
    } == {
        "TEST001",
        "TEST002",
    }


def test_unsupported_validator_is_not_executed():

    composite = CompositeValidator(
        (
            UnsupportedValidator(),
        )
    )

    result = composite.validate(
        DummyObject("राम")
    )

    assert result.is_valid
    assert result.issues == ()


def test_validator_order_is_preserved():

    composite = CompositeValidator(
        (
            IdentifierValidator(),
            AlwaysErrorValidator(),
        )
    )

    result = composite.validate(
        DummyObject("")
    )

    assert [
        issue.code
        for issue in result.issues
    ] == [
        "TEST001",
        "TEST002",
    ]


def test_validate_many_aggregates_results():

    composite = CompositeValidator(
        (
            IdentifierValidator(),
        )
    )

    result = composite.validate_many(
        (
            DummyObject("राम"),
            DummyObject(""),
            DummyObject("नारायण"),
            DummyObject(""),
        )
    )

    assert [
        issue.code
        for issue in result.issues
    ] == [
        "TEST001",
        "TEST001",
    ]
