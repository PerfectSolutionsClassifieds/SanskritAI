from __future__ import annotations

"""
SanskritAI
==========

Default Acquisition Service

Canonical default implementation of AcquisitionService.

The implementation is intentionally thin.

Version
-------
v0.1.0
"""

from dataclasses import dataclass

from SanskritAI.acquisition.models.acquisition_manifest import (
    AcquisitionManifest,
)

from SanskritAI.acquisition.models.acquisition_result import (
    AcquisitionResult,
)

from SanskritAI.acquisition.pipelines.acquisition_pipeline import (
    AcquisitionPipeline,
)

from SanskritAI.acquisition.services.acquisition_service import (
    AcquisitionService,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultAcquisitionService(
    AcquisitionService,
):
    """
    Canonical default acquisition service.

    Acquisition logic remains delegated to the configured
    AcquisitionPipeline.
    """

    pipeline: AcquisitionPipeline

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Default Acquisition Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Canonical application service over the "
            "acquisition pipeline."
        )

    # ---------------------------------------------------------
    # Acquisition
    # ---------------------------------------------------------

    def acquire(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:
        """
        Execute the acquisition pipeline.
        """

        return self.pipeline.acquire(
            manifest,
        )

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
