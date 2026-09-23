from __future__ import annotations

"""
SanskritAI
==========

Abstract Sūtra

Canonical executable base class for every Paninian sūtra.

Every executable sūtra follows the same life-cycle:

    supports()
        ↓
    validate()
        ↓
    before_apply()
        ↓
    _execute_rule()
        ↓
    after_apply()

Concrete subclasses NEVER override apply().

They implement only _execute_rule().
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.domain.panini.paninian_rule import PaninianRule
from SanskritAI.domain.panini.paninian_rule_metadata import (
    PaninianRuleMetadata,
)
from SanskritAI.domain.panini.paninian_sutra import (
    PaninianSutra,
)


class AbstractSutra(
    PaninianRule,
    ABC,
):
    """
    Canonical executable Paninian Sūtra.
    """

    def __init__(
        self,
        *,
        metadata: PaninianRuleMetadata,
    ) -> None:

        super().__init__(
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Canonical Sutra
    # ---------------------------------------------------------

    @property
    def sutra(self) -> PaninianSutra:
        return self.metadata.sutra

    @property
    def sutra_number(self) -> str:
        return self.sutra.sutra_number

    @property
    def sutra_text(self) -> str:
        return self.sutra.sutra_text

    @property
    def transliteration(self) -> str:
        return self.sutra.transliteration

    @property
    def translation(self) -> str:
        return self.sutra.translation

    @property
    def canonical_location(self) -> str:
        return self.sutra.canonical_location

    # ---------------------------------------------------------
    # Execution contract
    # ---------------------------------------------------------

    def supports(
        self,
        context,
    ) -> bool:
        """
        Determines whether the rule is applicable.

        Concrete subclasses may override.
        """
        return self.is_enabled

    def validate(
        self,
        context,
    ) -> bool:
        """
        Validates the context before execution.

        Default implementation accepts every context.
        """
        return True

    def before_apply(
        self,
        context,
    ):
        """
        Hook executed immediately before the rule.
        """
        return context

    @abstractmethod
    def _execute_rule(
        self,
        context,
    ) -> tuple:
        """
        Performs the actual grammatical semantics.

        Concrete subclasses MUST implement this.
        """
        raise NotImplementedError

    def after_apply(
        self,
        context,
        result,
    ):
        """
        Hook executed after successful execution.
        """
        return result

    # ---------------------------------------------------------
    # Canonical Template Method
    # ---------------------------------------------------------

    def apply(
        self,
        context,
    ) -> tuple:
        """
        Canonical execution wrapper.

        This method SHOULD NEVER be overridden.

        Life-cycle

            supports()

                ↓

            validate()

                ↓

            before_apply()

                ↓

            _execute_rule()

                ↓

            after_apply()
        """

        if not self.supports(
            context,
        ):
            return (context,)

        if not self.validate(
            context,
        ):
            return (context,)

        context = self.before_apply(
            context,
        )

        result = self._execute_rule(
            context,
        )

        result = self.after_apply(
            context,
            result,
        )

        return result

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def explain(self) -> str:
        return (
            f"{self.sutra_number}"
            " — "
            f"{self.translation}"
        )

    def trace(self) -> dict:

        trace = super().trace()

        trace.update(
            {
                "sutra_number": self.sutra_number,
                "sutra_text": self.sutra_text,
                "transliteration": self.transliteration,
                "translation": self.translation,
                "canonical_location": self.canonical_location,
            }
        )

        return trace

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.sutra_number

    @property
    def display_text(self) -> str:
        return (
            f"{self.sutra_number}"
            " — "
            f"{self.sutra_text}"
        )

    @property
    def display_description(self) -> str:
        return self.translation

    def __str__(self) -> str:
        return self.display_text
