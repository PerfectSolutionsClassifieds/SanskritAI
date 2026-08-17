
from __future__ import annotations

from unittest.mock import Mock

import pytest

from domain.lexical.validators.dictionary_entry_validator import (
    DictionaryEntryValidator,
)
from domain.lexical.validators.dictionary_sense_validator import (
    DictionarySenseValidator,
)
from domain.lexical.validators.lexeme_validator import LexemeValidator
from domain.lexical.validators.lexical_relation_validator import (
    LexicalRelationValidator,
)
from domain.lexical.validators.lexical_source_validator import (
    LexicalSourceValidator,
)
from domain.lexical.validators.lexical_validator_registry import (
    LexicalValidatorRegistry,
)


class TestLexicalValidatorRegistry:

    def test_registry_can_be_created(self):
        registry = LexicalValidatorRegistry()

        assert registry is not None

    def test_custom_registry_starts_with_supplied_validators(self):
        model_type = object
        validator = Mock()

        registry = LexicalValidatorRegistry(
            validators={
                model_type: validator,
            }
        )

        assert len(registry) == 1
        assert registry.get(model_type) is validator

    def test_register(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        validator = Mock()

        registry.register(
            str,
            validator,
        )

        assert registry.get(str) is validator
        assert str in registry

    def test_register_replaces_existing_validator(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        first = Mock()
        second = Mock()

        registry.register(str, first)
        registry.register(str, second)

        assert registry.get(str) is second
        assert len(registry) == 1

    def test_register_rejects_none_model_type(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        with pytest.raises(ValueError):
            registry.register(None, Mock())

    def test_register_rejects_none_validator(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        with pytest.raises(ValueError):
            registry.register(str, None)

    def test_register_rejects_invalid_validator(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        with pytest.raises(TypeError):
            registry.register(str, object())

    def test_get_returns_none_for_unknown_type(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        assert registry.get(str) is None

    def test_resolve_accepts_model_type(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        validator = Mock()

        registry.register(str, validator)

        assert registry.resolve(str) is validator

    def test_resolve_accepts_instance(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        validator = Mock()

        registry.register(str, validator)

        assert registry.resolve("sanskrit") is validator

    def test_resolve_uses_exact_type_before_base_type(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        base_validator = Mock()
        child_validator = Mock()

        class Base:
            pass

        class Child(Base):
            pass

        registry.register(Base, base_validator)
        registry.register(Child, child_validator)

        assert registry.resolve(Child()) is child_validator

    def test_resolve_falls_back_to_base_type(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        validator = Mock()

        class Base:
            pass

        class Child(Base):
            pass

        registry.register(Base, validator)

        assert registry.resolve(Child()) is validator

    def test_resolve_returns_none_when_unknown(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        assert registry.resolve(object()) is None

    def test_unregister_existing_validator(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        validator = Mock()

        registry.register(str, validator)

        assert registry.unregister(str) is True
        assert registry.get(str) is None

    def test_unregister_unknown_validator(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        assert registry.unregister(str) is False

    def test_contains(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        registry.register(str, Mock())

        assert registry.contains(str)
        assert str in registry
        assert not registry.contains(int)

    def test_clear(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        registry.register(str, Mock())
        registry.register(int, Mock())

        registry.clear()

        assert len(registry) == 0

    def test_items(self):
        registry = LexicalValidatorRegistry(
            validators={}
        )

        first = Mock()
        second = Mock()

        registry.register(str, first)
        registry.register(int, second)

        items = registry.items()

        assert (str, first) in items
        assert (int, second) in items

    def test_default_validator_classes_are_defined(self):
        registry_types = LexicalValidatorRegistry.DEFAULT_VALIDATORS

        assert DictionaryEntryValidator in registry_types
        assert DictionarySenseValidator in registry_types
        assert LexemeValidator in registry_types
        assert LexicalRelationValidator in registry_types
        assert LexicalSourceValidator in registry_types
