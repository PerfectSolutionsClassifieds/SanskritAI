from __future__ import annotations

"""
SanskritAI
==========

Sandhi Rule

Defines the abstract foundation for every Sandhi rule.

A SandhiRule performs one atomic Sandhi transformation or
analysis. Rules are intentionally independent and stateless,
allowing them to be composed into reusable SandhiRuleSets.

Every concrete rule receives a stable identifier derived from
its class name unless it explicitly overrides the identifier
property.

Future specializations
----------------------

• SvaraSandhiRule
• VyanjanaSandhiRule
• VisargaSandhiRule
• RecursiveSandhiRule

Version
-------
v1.1.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)


class SandhiRule(
    ABC,
    Displayable,
):
    """
    Abstract Sandhi rule.

    A SandhiRule is stateless and therefore does not own
    mutable runtime state.

    Concrete rules may override ``identifier`` when a
    canonical externally-defined identifier is required.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        """
        Stable identifier for this Sandhi rule.

        The default implementation derives a deterministic
        snake_case identifier from the concrete class name.

        Example
        -------
        SavarnaDirghaRule
            -> savarna_dirgha_rule
        """

        name = self.__class__.__name__

        if name.endswith("Rule"):
            name = name[:-4]

        characters: list[str] = []

        for index, character in enumerate(name):
            if character.isupper() and index > 0:
                characters.append("_")

            characters.append(character.lower())

        return "".join(characters) + "_rule"

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Abstract Sandhi rule."
        )

    # ---------------------------------------------------------
    # Rule Contract
    # ---------------------------------------------------------

    @abstractmethod
    def applies_to(
        self,
        context: SandhiContext,
    ) -> bool:
        """
        Determines whether this rule applies.
        """
        raise NotImplementedError

    @abstractmethod
    def apply(
        self,
        context: SandhiContext,
    ) -> tuple[str, ...]:
        """
        Applies the Sandhi rule.

        Returns
        -------
        tuple[str, ...]
            Candidate Sandhi outputs.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text

