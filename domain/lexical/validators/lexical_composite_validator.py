
from __future__ import annotations

from typing import Any, Iterable, Optional, Sequence, Type

# from core.validators.composite_validator import CompositeValidator
# from core.validators.validation_result import ValidationResult

from SanskritAI.core.validators.composite_validator import CompositeValidator
from SanskritAI.core.validators.validation_result import ValidationResult

from .dictionary_entry_validator import DictionaryEntryValidator
from .dictionary_sense_validator import DictionarySenseValidator
from .lexeme_validator import LexemeValidator
from .lexical_relation_validator import LexicalRelationValidator
from .lexical_source_validator import LexicalSourceValidator


class LexicalCompositeValidator(CompositeValidator):
    """
    Composite validator for the lexical domain.

    This validator composes the individual lexical validators and delegates
    domain-specific validation to them.

    It intentionally contains no duplicated validation rules.
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
        validators: Optional[Sequence[Any]] = None,
    ) -> None:
        """
        Create a lexical composite validator.

        Args:
            validators:
                Optional sequence of validator instances. When omitted,
                the standard lexical validators are created.
        """
        if validators is None:
            validators = tuple(
                validator_type()
                for validator_type in self.DEFAULT_VALIDATORS
            )

        super().__init__(validators)

    @property
    def validators(self) -> tuple[Any, ...]:
        """
        Return the validators participating in this composite.
        """
        return tuple(self._validators)

    def validate(self, value: Any) -> ValidationResult:
        """
        Validate a lexical value using the composed validators.

        Validators that do not apply to the supplied value are expected
        to return a valid/no-op result according to their own contract.
        """
        return super().validate(value)
