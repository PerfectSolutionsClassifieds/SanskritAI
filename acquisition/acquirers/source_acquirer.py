from __future__ import annotations

"""
SanskritAI
==========

Source Acquirer

Defines the abstraction responsible for acquiring a CorpusSource
according to an AcquisitionManifest.

The SourceAcquirer performs the acquisition operation itself.

It does NOT:
    - define CorpusSource identity
    - define acquisition policy
    - own the acquisition pipeline
    - own higher-level service orchestration

Concrete implementations may later provide:
    - HTTP acquisition
    - local-file acquisition
    - archive acquisition
    - repository-specific acquisition
    - authenticated acquisition

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


class SourceAcquirer(
    ABC,
    Displayable,
):
    """
    Strategy boundary for acquiring a configured source.

    A concrete acquirer receives an AcquisitionManifest and
    returns an AcquisitionResult.
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
            "Acquisition strategy for obtaining a configured "
            "corpus source."
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
        Acquire the source described by the manifest.

        Concrete implementations own the actual acquisition
        mechanism.
        """
        raise NotImplementedError

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
