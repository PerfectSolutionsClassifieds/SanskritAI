
from __future__ import annotations

import pytest

from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)
from SanskritAI.core.validators.validator import Validator
from SanskritAI.core.validators.validator_registry import (
    ValidatorRegistry,
)


class DummyValidator(Validator):

    def __init__(
        self,
        supported_type: type,
    ) -> None:
        self._supported_type = supported_type

    @classmethod
    def supports(cls, obj: object) -> bool:
        return True

    def validate(
        self,
        obj,
    ) -> ValidationResult:
        return ValidationResult.success()


class StringValidator(Validator):

    @classmethod
    def supports(cls, obj: object) -> bool:
        return isinstance(obj, str)

    def validate(
        self,
        obj,
    ) -> ValidationResult:
        return ValidationResult.success()


class IntegerValidator(Validator):

    @classmethod
    def supports(cls, obj: object) -> bool:
        return isinstance(obj, int)

    def validate(
        self,
        obj,
    ) -> ValidationResult:
        return ValidationResult.success()


def test_empty_registry_is_empty():

    registry = ValidatorRegistry()

    assert registry.is_empty
    assert len(registry) == 0


def test_register_validator():

    registry = ValidatorRegistry()

    validator = StringValidator()

    registry.register_validator(
        "string",
        validator,
    )

    assert len(registry) == 1
    assert registry.get_validator("string") is validator


def test_registered_validator_can_be_retrieved():

    registry = ValidatorRegistry()

    validator = StringValidator()

    registry.register_validator(
        "string",
        validator,
    )

    assert registry.get_validator("string") == validator


def test_missing_validator_returns_none():

    registry = ValidatorRegistry()

    assert registry.get_validator(
        "missing"
    ) is None


def test_supporting_returns_matching_validators():

    registry = ValidatorRegistry()

    string_validator = StringValidator()
    integer_validator = IntegerValidator()

    registry.register_validator(
        "string",
        string_validator,
    )

    registry.register_validator(
        "integer",
        integer_validator,
    )

    validators = registry.supporting("राम")

    assert validators == (
        string_validator,
    )


def test_supporting_preserves_registration_order():

    registry = ValidatorRegistry()

    first = StringValidator()
    second = StringValidator()

    registry.register_validator(
        "first",
        first,
    )

    registry.register_validator(
        "second",
        second,
    )

    assert registry.supporting("राम") == (
        first,
        second,
    )


def test_duplicate_registration_is_rejected():

    registry = ValidatorRegistry()

    registry.register_validator(
        "string",
        StringValidator(),
    )

    with pytest.raises(Exception):
        registry.register_validator(
            "string",
            StringValidator(),
        )
