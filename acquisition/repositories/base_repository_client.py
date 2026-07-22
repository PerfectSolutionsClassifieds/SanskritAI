
from __future__ import annotations

"""
SanskritAI
==========

Base Repository Client

Abstract base class for all remote corpus repository clients.

Responsibilities
----------------
* Repository identity
* Connectivity
* Catalog retrieval
* Resource downloading
* URL construction
* Shared downloader access

Concrete implementations
------------------------
    GretilRepositoryClient
    CologneRepositoryClient
    SaritRepositoryClient
    MuktabodhaRepositoryClient
    SanskritDocumentsRepositoryClient
    GitHubRepositoryClient
    InternetArchiveRepositoryClient

Version
-------
v0.7.0
"""

from abc import ABC, abstractmethod
from pathlib import Path

from SanskritAI.acquisition.downloaders.http_downloader import (
    HttpDownloader,
)


class BaseRepositoryClient(ABC):
    """
    Abstract base class for remote repository clients.
    """

    def __init__(
        self,
        downloader: HttpDownloader | None = None,
    ) -> None:

        self._downloader = downloader or HttpDownloader()

    # ---------------------------------------------------------
    # Repository Identity
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def identifier(self) -> str:
        """
        Unique repository identifier.

        Example
        -------
        gretil
        sarit
        github
        """
        ...

    @property
    @abstractmethod
    def base_url(self) -> str:
        """
        Repository base URL.
        """
        ...

    @property
    @abstractmethod
    def catalog_url(self) -> str:
        """
        Repository catalog URL.
        """
        ...

    # ---------------------------------------------------------
    # Connectivity
    # ---------------------------------------------------------

    def ping(self) -> bool:
        """
        Check whether the repository is reachable.
        """

        try:

            response = self._downloader.head(
                self.base_url
            )

            return response.ok

        except Exception:

            return False

    # ---------------------------------------------------------
    # Abstract Operations
    # ---------------------------------------------------------

    @abstractmethod
    def fetch_catalog(self) -> str:
        """
        Retrieve the repository catalog.
        """
        ...

    @abstractmethod
    def resource_url(
        self,
        resource: str,
    ) -> str:
        """
        Construct an absolute URL for a resource.
        """
        ...

    # ---------------------------------------------------------
    # Download
    # ---------------------------------------------------------

    def download_resource(
        self,
        resource: str,
        destination_directory: Path,
    ) -> Path:
        """
        Download a repository resource.
        """

        destination_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = (
            destination_directory
            / Path(resource).name
        )

        self._downloader.download(

            self.resource_url(resource),

            destination,

        )

        return destination

    # ---------------------------------------------------------
    # Shared Accessors
    # ---------------------------------------------------------

    @property
    def downloader(
        self,
    ) -> HttpDownloader:

        return self._downloader

    # ---------------------------------------------------------

    def metadata(
        self,
    ) -> dict[str, str]:
        """
        Repository metadata.
        """

        return {

            "identifier": self.identifier,

            "base_url": self.base_url,

            "catalog_url": self.catalog_url,

        }

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"identifier='{self.identifier}')"
        )
