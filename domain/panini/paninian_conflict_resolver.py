from __future__ import annotations

"""
SanskritAI
==========

Paninian Conflict Resolver

Canonical abstract base class for all Paninian
rule-conflict resolution strategies.

Purpose
-------

Whenever multiple executable Pāṇinian rules are
simultaneously applicable, the derivation engine
constructs a PaninianRuleConflict and delegates
resolution to one or more concrete conflict
resolvers.

This class defines the common interface.

Concrete implementations include

    • VipratisedhaResolver

    • AntarangaResolver

    • BahirangaResolver

    • NityaResolver

    • AsiddhaResolver

    • OptionalRuleResolver

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)
from SanskritAI.domain.panini.paninian_rule_conflict import (
    PaninianRuleConflict,
)


class PaninianConflictResolver(
    ValueObject,
    Immutable,
    Displayable,
    ABC,
):
    """
    Abstract Paninian conflict resolver.
    """

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
            "Paninian conflict resolution strategy"
        )

    # ---------------------------------------------------------
    # Capability
    # ---------------------------------------------------------

    @abstractmethod
    def supports(
        self,
        conflict: PaninianRuleConflict,
    ) -> bool:
        """
        Determines whether this resolver is
        applicable to the supplied conflict.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    @abstractmethod
    def resolve(
        self,
        conflict: PaninianRuleConflict,
    ) -> tuple[PaninianRule, ...]:
        """
        Resolves the supplied conflict.

        Returns
        -------
        tuple[PaninianRule, ...]

        The selected rule or rules.

        Notes
        -----
        Most resolvers return a single rule.
        Optional-rule resolvers may return
        multiple rules representing branches.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        return {
            "resolver": self.display_name,
        }

    def __str__(
        self,
    ) -> str:
        return self.display_name
