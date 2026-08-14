import pytest

from SanskritAI.core.validators.validation_issue import (
    ValidationIssue,
    ValidationSeverity,
)
from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)
from SanskritAI.core.validators.validator import (
    Validator,
)


# =============================================================
# Test implementation
# =============================================================


class StubValidator(Validator[str]):
    """
    Minimal concrete validator used to test the base contract.
    """

    def validate(self, obj: str) -> ValidationResult:
        if not obj:
            return ValidationResult.from_issues(
                [
                    ValidationIssue(
                        code="EMPTY",
                        message="Object must not be empty.",
                        severity=ValidationSeverity.ERROR,
                    )
                ]
            )

        return ValidationResult.success()


class RecordingValidator(Validator[str]):
    """
    Validator used to verify validation order and calls.
    """

    def __init__(self):
        self.validated = []

    def validate(self, obj: str) -> ValidationResult:
        self.validated.append(obj)
        return ValidationResult.success()


class SelectiveValidator(Validator[int]):
    """
    Validator producing different results for different inputs.
    """

    def validate(self, obj: int) -> ValidationResult:
        if obj < 0:
            return ValidationResult.from_issues(
                [
                    ValidationIssue(
                        code="NEGATIVE",
                        message="Value must not be negative.",
                        severity=ValidationSeverity.ERROR,
                    )
                ]
            )

        if obj == 0:
            return ValidationResult.from_issues(
                [
                    ValidationIssue(
                        code="ZERO",
                        message="Value is zero.",
                        severity=ValidationSeverity.WARNING,
                    )
                ]
            )

        return ValidationResult.success()


# =============================================================
# Abstract contract
# =============================================================


def test_validator_is_abstract():
    assert Validator.__abstractmethods__


def test_validator_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        Validator()


def test_validate_is_abstract():
    assert "validate" in Validator.__abstractmethods__


def test_concrete_validator_can_be_instantiated():
    validator = StubValidator()

    assert isinstance(validator, Validator)


# =============================================================
# Single-object validation
# =============================================================


def test_validate_returns_validation_result():
    validator = StubValidator()

    result = validator.validate("rama")

    assert isinstance(result, ValidationResult)


def test_valid_object_returns_success():
    validator = StubValidator()

    result = validator.validate("rama")

    assert result.is_valid is True
    assert result.issues == ()


def test_invalid_object_returns_error():
    validator = StubValidator()

    result = validator.validate("")

    assert result.is_valid is False
    assert result.has_errors is True
    assert result.error_count == 1


# =============================================================
# validate_many
# =============================================================


def test_validate_many_with_empty_iterable_returns_success():
    validator = StubValidator()

    result = validator.validate_many([])

    assert isinstance(result, ValidationResult)
    assert result.is_valid is True
    assert result.issues == ()


def test_validate_many_validates_all_objects():
    validator = RecordingValidator()

    objects = ["a", "b", "c"]

    result = validator.validate_many(objects)

    assert result.is_valid is True
    assert validator.validated == objects


def test_validate_many_accepts_generator():
    validator = RecordingValidator()

    objects = (value for value in ["a", "b", "c"])

    result = validator.validate_many(objects)

    assert result.is_valid is True
    assert validator.validated == ["a", "b", "c"]


def test_validate_many_merges_validation_results():
    validator = SelectiveValidator()

    result = validator.validate_many(
        [-1, 0, 1]
    )

    assert result.is_valid is False
    assert result.error_count == 1
    assert result.warning_count == 1


def test_validate_many_preserves_validation_order():
    validator = RecordingValidator()

    validator.validate_many(
        ["first", "second", "third"]
    )

    assert validator.validated == [
        "first",
        "second",
        "third",
    ]


def test_validate_many_calls_validate_once_per_object():
    validator = RecordingValidator()

    objects = ["a", "b", "c", "d"]

    validator.validate_many(objects)

    assert len(validator.validated) == len(objects)


def test_validate_many_returns_single_merged_result():
    validator = SelectiveValidator()

    result = validator.validate_many(
        [-1, -2, -3]
    )

    assert result.error_count == 3
    assert len(result) == 3


def test_validate_many_preserves_issue_order():
    validator = SelectiveValidator()

    result = validator.validate_many(
        [-1, 0, -2]
    )

    assert [issue.code for issue in result.issues] == [
        "NEGATIVE",
        "ZERO",
        "NEGATIVE",
    ]


# =============================================================
# supports
# =============================================================


def test_default_supports_returns_true():
    assert StubValidator.supports("rama") is True


def test_supports_is_class_method():
    assert isinstance(
        Validator.__dict__["supports"],
        classmethod,
    )


def test_supports_accepts_arbitrary_object():
    assert Validator.supports(object()) is True


def test_concrete_validator_inherits_default_supports():
    validator = StubValidator()

    assert validator.supports("rama") is True


def test_supports_can_be_overridden():
    class IntegerValidator(Validator[int]):
        def validate(self, obj: int) -> ValidationResult:
            return ValidationResult.success()

        @classmethod
        def supports(cls, obj: object) -> bool:
            return isinstance(obj, int)

    assert IntegerValidator.supports(10) is True
    assert IntegerValidator.supports("10") is False


# =============================================================
# Generic behavior
# =============================================================


def test_validator_generic_contract_accepts_typed_objects():
    validator = SelectiveValidator()

    result = validator.validate(10)

    assert isinstance(result, ValidationResult)
    assert result.is_valid is True
