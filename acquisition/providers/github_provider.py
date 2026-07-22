
from __future__ import annotations

"""
SanskritAI
==========

GitHub Provider

Acquisition provider for GitHub-hosted Sanskrit corpora.

The GitHubProvider acquires corpus resources from public GitHub
repositories. It delegates all HTTP communication to a repository
client and focuses solely on acquisition workflow.

Typical Uses
------------
* Sanskrit corpora hosted on GitHub
* TEI/XML repositories
* TXT collections
* JSON metadata repositories
* Version-controlled research datasets

Responsibilities
----------------
* Repository discovery
* Resource discovery
* Resource acquisition
* AcquisitionResponse creation

This provider intentionally does NOT perform:

    * Parsing
    * Validation
    * Normalization
    * Importing

Those belong to later acquisition stages.

Version
-------
v0.7.0
"""

from pathlib import Path
from typing import Iterable

from SanskritAI.acquisition.providers.acquisition_request import (
    AcquisitionRequest,
)
from SanskritAI.acquisition.providers.acquisition_response import (
    AcquisitionResponse,
)
from SanskritAI.acquisition.providers.base_provider import (
    BaseProvider,
)
from SanskritAI.acquisition.repositories.base_repository_client import (
    BaseRepositoryClient,
)


class GitHubProvider(BaseProvider):
    """
    Acquisition provider for GitHub repositories.
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

        return "github"

    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:

        return "GitHub Provider"

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover(
        self,
        request: AcquisitionRequest,
    ):
        """
        Discover available resources.

        Delegates to the repository client.
        """

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
        """
        Acquire resources from GitHub.
        """

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
    # Convenience
    # ---------------------------------------------------------

    def supported_extensions(
        self,
    ) -> tuple[str, ...]:
        """
        Common corpus formats hosted on GitHub.
        """

        return (

            ".txt",

            ".xml",

            ".tei",

            ".tei.xml",

            ".json",

            ".yaml",

            ".yml",

            ".csv",

            ".tsv",

            ".html",

            ".htm",

            ".pdf",

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

            "supports_discovery":
                True,

            "supports_download":
                True,

            "supports_incremental":
                True,

            "supports_versioning":
                True,

            "source":
                "GitHub",

        }

    # ---------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Verify repository availability.
        """

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
