from __future__ import annotations

"""
SanskritAI
==========

Default Paninian Conflict Resolution Pipeline

Provides the canonical Paribhāṣā pipeline used by the
Paninian Derivation Engine.

Purpose
-------

Constructs the default ordered sequence of conflict
resolvers used by SanskritAI.

Current Pipeline
----------------

    1. Vipratiṣedha
    2. Antaraṅga
    3. Bāhiraṅga

Future versions may extend the pipeline with

    • NityaResolver

    • AsiddhaResolver

    • OptionalRuleResolver

    • Custom user-defined Paribhāṣā strategies

Architecture
------------

PaninianDerivationEngine
            │
            ▼
DefaultConflictPipeline
            │
            ▼
PaninianConflictResolutionPipeline
            │
            ├── VipratisedhaResolver
            ├── AntarangaResolver
            └── BahirangaResolver

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.domain.panini.paninian_conflict_resolution_pipeline import (
    PaninianConflictResolutionPipeline,
)

from SanskritAI.domain.panini.conflict_resolvers.vipratisedha_resolver import (
    VipratisedhaResolver,
)

from SanskritAI.domain.panini.conflict_resolvers.antaranga_resolver import (
    AntarangaResolver,
)

from SanskritAI.domain.panini.conflict_resolvers.bahiranga_resolver import (
    BahirangaResolver,
)


@dataclass(slots=True)
class DefaultPaninianConflictPipeline:
    """
    Factory for the canonical Paninian
    conflict-resolution pipeline.
    """

    pipeline: PaninianConflictResolutionPipeline = field(
        init=False,
    )

    def __post_init__(self) -> None:
        self.pipeline = (
            PaninianConflictResolutionPipeline(
                resolvers=(
                    VipratisedhaResolver(),
                    AntarangaResolver(),
                    BahirangaResolver(),
                )
            )
        )

    # ---------------------------------------------------------
    # Accessors
    # ---------------------------------------------------------

    def get_pipeline(
        self,
    ) -> PaninianConflictResolutionPipeline:
        """
        Returns the configured pipeline.
        """
        return self.pipeline

    @property
    def resolvers(
        self,
    ):
        """
        Returns the configured resolver sequence.
        """
        return self.pipeline.resolvers

    @property
    def resolver_count(
        self,
    ) -> int:
        return self.pipeline.resolver_count

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        """
        Returns pipeline summary.
        """
        return {
            "resolver_count": self.resolver_count,
            "pipeline": tuple(
                resolver.display_name
                for resolver in self.resolvers
            ),
        }

    def __str__(
        self,
    ) -> str:
        return (
            "DefaultPaninianConflictPipeline("
            f"{self.resolver_count} resolvers)"
        )
