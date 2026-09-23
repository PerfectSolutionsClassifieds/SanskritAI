from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Engine

The central execution engine for the Paninian Kernel.

Every linguistic kernel ultimately derives its behaviour from
Paninian grammatical rules. Rather than allowing each kernel to
implement its own execution mechanism, the Paninian Rule Engine
provides one canonical orchestration layer.

Hierarchy
---------

PaninianRule
        │
        ▼
PaninianRuleCollection
        │
        ▼
PaninianRuleSet
        │
        ▼
PaninianRuleRepository
        │
        ▼
PaninianRuleEngine
        │
        ├── Sandhi Kernel
        ├── Samāsa Kernel
        ├── Dhātu Kernel
        ├── Pratyaya Kernel
        ├── Derivation Kernel
        ├── Grammar Kernel
        ├── Vākya Kernel
        ├── Semantic Kernel
        ├── Chandas Kernel
        ├── Alaṅkāra Kernel
        └── Knowledge Graph Kernel

Future
------

Later versions may support

• Rule dependency graph
• Rule tracing
• Rule conflict resolution
• Rule explanation
• Rule diagnostics
• Multi-stage derivation pipeline
• Aṣṭādhyāyī sequencing
• Knowledge Graph integration

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.panini.default_paninian_rule_repository import (
    DefaultPaninianRuleRepository,
)
from SanskritAI.domain.panini.paninian_rule_collection import (
    PaninianRuleCollection,
)
from SanskritAI.domain.panini.paninian_rule_repository import (
    PaninianRuleRepository,
)
from SanskritAI.domain.panini.paninian_rule_set import (
    PaninianRuleSet,
)


@dataclass(frozen=True, slots=True)
class PaninianRuleEngine(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical Paninian execution engine.
    """

    repository: PaninianRuleRepository = (
        DefaultPaninianRuleRepository()
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Paninian Rule Engine"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Canonical execution engine for "
            "Paninian grammatical rules."
        )

    # ---------------------------------------------------------
    # Repository
    # ---------------------------------------------------------

    @property
    def rules(self) -> PaninianRuleCollection:
        return self.repository.all()

    @property
    def rule_count(self) -> int:
        return self.rules.count

    @property
    def enabled_rules(self) -> PaninianRuleCollection:
        return self.rules.enabled()

    # ---------------------------------------------------------
    # Rule Set
    # ---------------------------------------------------------

    def create_rule_set(
        self,
    ) -> PaninianRuleSet:
        """
        Creates an executable rule set from the repository.
        """
        return PaninianRuleSet(
            rules=self.enabled_rules,
        )

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        context: Any,
    ) -> tuple[Any, ...]:
        """
        Executes every applicable Paninian rule.
        """
        return (
            self
            .create_rule_set()
            .apply(context)
        )

    def applicable_rules(
        self,
        context: Any,
    ) -> PaninianRuleCollection:
        """
        Returns every rule applicable to the supplied context.
        """
        return (
            self
            .create_rule_set()
            .applicable_rules(context)
        )

    # ---------------------------------------------------------
    # Repository Delegation
    # ---------------------------------------------------------

    def get_rule(
        self,
        identifier: str,
    ):
        return self.repository.get_by_identifier(
            identifier
        )

    def get_sutra(
        self,
        sutra_number: str,
    ):
        return self.repository.get_by_sutra(
            sutra_number
        )

    def category(
        self,
        category: str,
    ) -> PaninianRuleCollection:
        return self.repository.by_category(
            category
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_empty(self) -> bool:
        return self.rule_count == 0

    @property
    def is_not_empty(self) -> bool:
        return not self.is_empty

    def __len__(self) -> int:
        return self.rule_count

    def __str__(self) -> str:
        return self.display_text
