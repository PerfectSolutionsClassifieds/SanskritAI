from __future__ import annotations

from typing import Any, Dict, Optional, Type

from .dictionary_entry_validator import DictionaryEntryValidator
from .dictionary_sense_validator import DictionarySenseValidator
from .lexeme_validator import LexemeValidator
from .lexical_relation_validator import LexicalRelationValidator
from .lexical_source_validator import LexicalSourceValidator


class LexicalValidatorRegistry:
    """
    Registry of validators for lexical domain objects.

    The registry maps a lexical model type to the validator responsible
    for validating instances of that type.
    """

    DEFAULT_VALIDATORS = (
        DictionaryEntryValidator,
        DictionarySenseValidator,
        LexemeValidator,
        LexicalRelationValidator,
        LexicalSourceValidator,
    )

    def __init__(
        self,
        validators: Optional[
            Dict[Type[Any], Any]
        ] = None,
    ) -> None:
        self._validators: Dict[Type[Any], Any] = {}

        if validators:
            for model_type, validator in validators.items():
                self.register(model_type, validator)

        else:
            self._register_defaults()

    def _register_defaults(self) -> None:
        """
        Register the standard lexical validators.
        """
        for validator_type in self.DEFAULT_VALIDATORS:
            validator = validator_type()

            model_type = self._infer_model_type(
                validator
            )

            if model_type is not None:
                self.register(model_type, validator)

    @staticmethod
    def _infer_model_type(
        validator: Any,
    ) -> Optional[Type[Any]]:
        """
        Infer the model type handled by a validator.

        Validators may expose a `model_type` attribute or property.
        """
        model_type = getattr(
            validator,
            "model_type",
            None,
        )

        if model_type is not None:
            return model_type

        return None

    def register(
        self,
        model_type: Type[Any],
        validator: Any,
    ) -> None:
        """
        Register a validator for a model type.
        """
        if model_type is None:
            raise ValueError("model_type cannot be None")

        if validator is None:
            raise ValueError("validator cannot be None")

        if not hasattr(validator, "validate"):
            raise TypeError(
                "validator must provide a validate() method"
            )

        self._validators[model_type] = validator

    def unregister(
        self,
        model_type: Type[Any],
    ) -> bool:
        """
        Remove a validator.

        Returns:
            True when a validator was removed, otherwise False.
        """
        return self._validators.pop(
            model_type,
            None,
        ) is not None

    def get(
        self,
        model_type: Type[Any],
    ) -> Optional[Any]:
        """
        Return the validator registered for an exact model type.
        """
        return self._validators.get(model_type)

    def resolve(
        self,
        value_or_type: Any,
    ) -> Optional[Any]:
        """
        Resolve a validator from either an object or a model type.

        Exact type matching is preferred. If no exact match exists,
        the MRO is searched for a registered base type.
        """
        model_type = (
            value_or_type
            if isinstance(value_or_type, type)
            else type(value_or_type)
        )

        validator = self._validators.get(model_type)

        if validator is not None:
            return validator

        for base_type in model_type.__mro__[1:]:
            validator = self._validators.get(base_type)

            if validator is not None:
                return validator

        return None

    def contains(
        self,
        model_type: Type[Any],
    ) -> bool:
        """
        Return whether a validator is registered.
        """
        return model_type in self._validators

    def clear(self) -> None:
        """
        Remove all registered validators.
        """
        self._validators.clear()

    def __len__(self) -> int:
        return len(self._validators)

    def __contains__(
        self,
        model_type: Type[Any],
    ) -> bool:
        return self.contains(model_type)

    def items(self):
        """
        Return registered model/validator pairs.
        """
        return tuple(self._validators.items())
