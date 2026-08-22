from __future__ import annotations

"""
SanskritAI
==========

Acquisition Pipeline

Coordinates execution of an AcquisitionManifest through a
configured SourceAcquirer.

Architecture
------------

AcquisitionService
        │
        ▼
AcquisitionPipeline
        │
        ▼
SourceAcquirer
        │
        ▼
AcquisitionManifest
        │
        ▼
AcquisitionResult

The pipeline owns orchestration only.

Version
-------
v0.1.0
"""

from dataclasses import dataclass

from SanskritAI.acquisition.acquirers.source_acquirer import (
    SourceAcquirer,
)

from SanskritAI.acquisition.models.acquisition_manifest import (
    AcquisitionManifest,
)

from SanskritAI.acquisition.models.acquisition_result import (
    AcquisitionResult,
)

from SanskritAI.core.mixins.displayable import Displayable


@dataclass(
    frozen=True,
    slots=True,
)
class AcquisitionPipeline(
    Displayable,
):
    """
    Canonical acquisition orchestration boundary.

    The pipeline delegates the actual acquisition operation
    to the configured SourceAcquirer.
    """

    acquirer: SourceAcquirer

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Acquisition Pipeline"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Coordinates execution of acquisition manifests "
            "through a configured source acquirer."
        )

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def acquire(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:
        """
        Execute the supplied acquisition manifest.
        """

        return self.acquirer.acquire(
            manifest,
        )

    # ---------------------------------------------------------
    # Alias
    # ---------------------------------------------------------

    def run(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:
        """
        Terminology-neutral alias for acquire().
        """

        return self.acquire(
            manifest,
        )

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
