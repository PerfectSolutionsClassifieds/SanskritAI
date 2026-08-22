from __future__ import annotations

"""
SanskritAI
==========

Acquisition Service

Application-facing façade over the Acquisition Pipeline.

The service deliberately contains no downloading logic.

Version
-------
v0.1.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.acquisition.models.acquisition_manifest import (
    AcquisitionManifest,
)

from SanskritAI.acquisition.models.acquisition_result import (
    AcquisitionResult,
)

from SanskritAI.core.mixins.displayable import Displayable


class AcquisitionService(
    ABC,
    Displayable,
):
    """
    Application-facing acquisition service boundary.
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
            "Application-facing façade for canonical "
            "source acquisition."
        )

    # ---------------------------------------------------------
    # Acquisition
    # ---------------------------------------------------------

    @abstractmethod
    def acquire(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:
        """
        Execute acquisition for the supplied manifest.
        """
        raise NotImplementedError

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
