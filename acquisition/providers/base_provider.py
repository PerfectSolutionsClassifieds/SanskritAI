
from __future__ import annotations

"""
SanskritAI
==========

Base Acquisition Provider

Defines the abstract foundation for every corpus acquisition provider.

Concrete providers include

    • GretilProvider
    • CologneProvider
    • SaritProvider
    • MuktabodhaProvider
    • SanskritDocumentsProvider
    • GitHubProvider
    • InternetArchiveProvider

Responsibilities
----------------
* Repository capability declaration
* Discovery interface
* Acquisition interface
* Health checking
* Request validation
* Common metadata
* Provider lifecycle

Version
-------
v0.6.0
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from SanskritAI.acquisition.providers.acquisition_request import (
    AcquisitionRequest,
)

from SanskritAI.acquisition.providers.acquisition_response import (
    AcquisitionResponse,
)


class BaseProvider(ABC):
    """
    Abstract base class for every acquisition provider.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        *,
        cache_directory: Path | None = None,
        timeout: float = 60.0,
    ) -> None:

        self._cache_directory = cache_directory

        self._timeout = timeout

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def identifier(self) -> str:
        """
        Unique provider identifier.

        Example
        -------
        gretil
        """

    @property
    @abstractmethod
    def display_name(self) -> str:
        """
        Human readable provider name.
        """

    @property
    @abstractmethod
    def homepage(self) -> str:
        """
        Repository homepage.
        """

    # ------------------------------------------------------------------
    # Capabilities
    # ------------------------------------------------------------------

    @property
    def supports_discovery(self) -> bool:

        return True

    @property
    def supports_download(self) -> bool:

        return True

    @property
    def supports_search(self) -> bool:

        return True

    @property
    def supports_metadata(self) -> bool:

        return True

    @property
    def supports_incremental_updates(self) -> bool:

        return False

    # ------------------------------------------------------------------
    # Main Operations
    # ------------------------------------------------------------------

    @abstractmethod
    def discover(
        self,
        request: AcquisitionRequest,
    ) -> AcquisitionResponse:
        """
        Discover available resources.
        """

    @abstractmethod
    def acquire(
        self,
        request: AcquisitionRequest,
    ) -> AcquisitionResponse:
        """
        Acquire resources from the repository.
        """

    # ------------------------------------------------------------------
    # Repository Information
    # ------------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Returns True if the provider appears operational.

        Concrete providers should override this with
        network connectivity checks.
        """

        return True

    # ------------------------------------------------------------------

    def capabilities(
        self,
    ) -> dict[str, bool]:

        return {

            "discovery": self.supports_discovery,

            "download": self.supports_download,

            "search": self.supports_search,

            "metadata": self.supports_metadata,

            "incremental_updates":
                self.supports_incremental_updates,

        }

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_request(
        self,
        request: AcquisitionRequest,
    ) -> None:
        """
        Validate an acquisition request.

        Providers may extend this method.
        """

        if request.has_destination:

            destination = request.destination_directory

            if destination is not None:

                if (
                    not destination.exists()
                    and request.create_directory
                ):

                    destination.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

    # ------------------------------------------------------------------

    def create_response(
        self,
    ) -> AcquisitionResponse:
        """
        Create a provider response.
        """

        return AcquisitionResponse(

            provider_name=self.display_name,

        )

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    @property
    def timeout(
        self,
    ) -> float:

        return self._timeout

    @property
    def cache_directory(
        self,
    ) -> Path | None:

        return self._cache_directory

    # ------------------------------------------------------------------

    def provider_metadata(
        self,
    ) -> dict[str, Any]:
        """
        Metadata describing the provider.
        """

        return {

            "identifier": self.identifier,

            "display_name": self.display_name,

            "homepage": self.homepage,

            "capabilities": self.capabilities(),

        }

    # ------------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}("

            f"identifier='{self.identifier}', "

            f"display_name='{self.display_name}')"

        )
