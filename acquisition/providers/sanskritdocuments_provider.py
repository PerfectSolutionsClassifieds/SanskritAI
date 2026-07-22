
from __future__ import annotations

"""
SanskritAI
==========

SanskritDocuments Provider

Acquisition provider for SanskritDocuments.org.

This provider orchestrates acquisition of Sanskrit texts hosted on
SanskritDocuments.org while delegating all HTTP communication,
catalog traversal and downloading to a dedicated repository client.

Typical Resources
-----------------
* Stotra collections
* Veda texts
* Puranas
* Upanishads
* Gita editions
* Kavya
* Tantra
* Sahasranama
* HTML pages
* Plain text files
* PDF documents

Responsibilities
----------------
* Resource discovery
* Resource acquisition
* Download orchestration
* AcquisitionResponse generation

This provider intentionally DOES NOT perform

    * HTML parsing
    * Metadata extraction
    * Unicode normalization
    * Importing
    * NLP processing

Those belong to later pipeline stages.

Version
-------
v0.7.0
"""

from pathlib import Path
from typing import Iterable

from SanskritAI.acquisition.providers.base_provider import (
    BaseProvider,
)
from SanskritAI.acquisition.providers.acquisition_request import (
    AcquisitionRequest,
)
from SanskritAI.acquisition.providers.acquisition_response import (
    AcquisitionResponse,
)
from SanskritAI.acquisition.repositories.base_repository_client import (
    BaseRepositoryClient,
)


class SanskritDocumentsProvider(BaseProvider):
    """
    Acquisition provider for SanskritDocuments.org.
    """

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(
        self,
        repository: BaseRepositoryClient,
    ) -> None:

        super().__init__(repository)

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:

        return "sanskritdocuments"

    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:

        return "Sanskrit Documents Provider"

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover(
        self,
        request: AcquisitionRequest,
    ) -> Iterable:

        return self.repository.discover(
            request
        )

    # ---------------------------------------------------------
    # Acquisition
    # ---------------------------------------------------------

    def acquire(
        self,
        request: AcquisitionRequest,
    ) -> AcquisitionResponse:

        response = AcquisitionResponse(
            provider_name=self.display_name,
        )

        resources = self.discover(
            request
        )

        for resource in resources:

            try:

                destination = self.repository.download(
                    resource,
                    destination=request.destination,
                )

                response.add_download(
                    Path(destination)
                )

            except Exception as exc:

                response.error(
                    str(exc)
                )

        response.finish()

        return response

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def supported_extensions(
        self,
    ) -> tuple[str, ...]:

        return (

            ".html",
            ".htm",

            ".txt",

            ".xml",

            ".pdf",

            ".zip",

        )

    # ---------------------------------------------------------

    def preferred_formats(
        self,
    ) -> tuple[str, ...]:
        """
        Preferred acquisition order.
        """

        return (

            ".txt",

            ".html",

            ".xml",

            ".pdf",

            ".zip",

        )

    # ---------------------------------------------------------

    def supports_extension(
        self,
        extension: str,
    ) -> bool:

        return (

            extension.lower()

            in self.supported_extensions()

        )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def metadata(
        self,
    ) -> dict:

        return {

            "identifier":
                self.identifier,

            "display_name":
                self.display_name,

            "repository":
                self.repository.identifier,

            "source":
                "SanskritDocuments.org",

            "supports_discovery":
                True,

            "supports_download":
                True,

            "supports_html":
                True,

            "supports_plain_text":
                True,

            "supports_pdf":
                True,

            "supports_incremental":
                True,

        }

    # ---------------------------------------------------------

    def health_check(
        self,
    ) -> bool:

        try:

            return self.repository.ping()

        except Exception:

            return False

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}("

            f"repository={self.repository.identifier!r})"

        )
