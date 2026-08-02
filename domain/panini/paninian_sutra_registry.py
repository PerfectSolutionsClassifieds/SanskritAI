from __future__ import annotations

"""
SanskritAI
==========

Paninian Sutra Registry

Canonical registry for executable Paninian Sūtras.

Responsibilities
----------------

• exposes registered sūtras

• performs lookup

• instantiates rule objects

• provides immutable query interface

Discovery is NOT performed here.

Discovery belongs to

    PaninianSutraLoader

Registration belongs to

    register_paninian_sutra()

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from typing import Iterator

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)

from SanskritAI.domain.panini.paninian_sutra_registration import (
    get_registry,
)

from SanskritAI.domain.panini.paninian_sutra_registration import (
    get_registered_class,
)


@dataclass(slots=True)
class PaninianSutraRegistry:
    """
    Canonical executable sūtra registry.
    """

    registry_name: str = "panini"

    # ---------------------------------------------------------
    # Internal registry
    # ---------------------------------------------------------

    @property
    def registry(
        self,
    ) -> dict[str, type[PaninianRule]]:

        return get_registry(
            self.registry_name,
        )

    # ---------------------------------------------------------
    # Basic information
    # ---------------------------------------------------------

    @property
    def size(
        self,
    ) -> int:

        return len(
            self.registry,
        )

    @property
    def is_empty(
        self,
    ) -> bool:

        return self.size == 0

    @property
    def sutra_numbers(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            sorted(
                self.registry.keys(),
            )
        )

    # ---------------------------------------------------------
    # Membership
    # ---------------------------------------------------------

    def contains(
        self,
        sutra_number: str,
    ) -> bool:

        return sutra_number in self.registry

    def __contains__(
        self,
        sutra_number: str,
    ) -> bool:

        return self.contains(
            sutra_number,
        )

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get_rule_class(
        self,
        sutra_number: str,
    ) -> type[PaninianRule]:

        rule_cls = get_registered_class(
            sutra_number,
            self.registry_name,
        )

        if rule_cls is None:

            raise KeyError(
                f"Unknown Paninian Sūtra "
                f"{sutra_number}"
            )

        return rule_cls

    def create(
        self,
        sutra_number: str,
    ) -> PaninianRule:
        """
        Instantiates one executable rule.
        """

        rule_cls = self.get_rule_class(
            sutra_number,
        )

        return rule_cls()

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def rule_classes(
        self,
    ) -> tuple[type[PaninianRule], ...]:

        return tuple(
            self.registry.values(),
        )

    def instances(
        self,
    ) -> tuple[PaninianRule, ...]:

        return tuple(

            rule_cls()

            for rule_cls

            in self.rule_classes()

        )

    def __iter__(
        self,
    ) -> Iterator[PaninianRule]:

        yield from self.instances()

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "registry": self.registry_name,

            "sutra_count": self.size,

            "registered_sutras": self.sutra_numbers,

        }

    def __len__(
        self,
    ) -> int:

        return self.size

    def __str__(
        self,
    ) -> str:

        return (
            "PaninianSutraRegistry("
            f"{self.registry_name}, "
            f"{self.size} sūtras)"
        )
