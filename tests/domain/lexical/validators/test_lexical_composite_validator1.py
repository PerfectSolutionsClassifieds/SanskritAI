from __future__ import annotations

from unittest.mock import Mock

from core.validators.validation_result import ValidationResult

from domain.lexical.validators.dictionary_entry_validator import (
    DictionaryEntryValidator,
)
from domain.lexical.validators.dictionary_sense_validator import (
    DictionarySenseValidator,
)
from domain.lexical.validators.lexeme_validator import LexemeValidator
from domain.lexical.validators.lexical_composite_validator import (
    LexicalCompositeValidator,
)
from domain.lexical.validators.lexical_relation_validator import (
    LexicalRelationValidator,
)
from domain.lexical.validators.lexical_source_validator import (
    LexicalSourceValidator,
)


class TestLexicalCompositeValidator:
    def test_creates_default_validators(self):
        validator = LexicalCompositeValidator()

        assert len(validator.validators) == 5

        assert isinstance(
            validator.validators[0],
            DictionaryEntryValidator,
        )
        assert isinstance(
            validator.validators[1],
            DictionarySenseValidator,
        )
        assert isinstance(
            validator.validators[2],
            LexemeValidator,
        )
        assert isinstance(
            validator.validators[3],
            LexicalRelationValidator,
        )
        assert isinstance(
            validator.validators[4],
            LexicalSourceValidator,
        )

    def test_accepts_custom_validators(self):
        first = Mock()
        second = Mock()

        validator = LexicalCompositeValidator(
            validators=(first, second)
        )

        assert validator.validators == (first, second)

    def test_delegates_validation_to_composite(self):
        value = object()

        first = Mock()
        second = Mock()

        first.validate.return_value = ValidationResult.valid()
        second.validate.return_value = ValidationResult.valid()

        validator = LexicalCompositeValidator(
            validators=(first, second)
        )

        result = validator.validate(value)

        assert isinstance(result, ValidationResult)
        first.validate.assert_called_once_with(value)
        second.validate.assert_called_once_with(value)

    def test_empty_composite_is_valid(self):
        validator = LexicalCompositeValidator(validators=())

        result = validator.validate(object())

        assert result.is_valid

    def test_validates_lexical_value_without_replacing_individual_rules(self):
        validator = LexicalCompositeValidator()

        # The composite owns orchestration only. Individual validators
        # remain responsible for their own domain rules.
        assert all(
            hasattr(item, "validate")
            for item in validator.validators
        )

    def test_validators_are_returned_as_immutable_tuple(self):
        validator = LexicalCompositeValidator()

        assert isinstance(validator.validators, tuple)
