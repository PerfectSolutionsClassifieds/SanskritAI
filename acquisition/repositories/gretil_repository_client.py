
from __future__ import annotations

"""
SanskritAI
==========

GRETIL Repository Client

Concrete implementation of BaseRepositoryClient for the
Göttingen Register of Electronic Texts in Indian Languages
(GRETIL).

Responsibilities
----------------
* Repository connectivity
* Catalog retrieval
* Resource URL construction
* Resource downloading

This class intentionally performs NO parsing.

Parsing belongs to:

    GretilCatalogParser

Acquisition orchestration belongs to:

    GretilProvider

Version
-------
v0.7.0
"""

from urllib.parse import urljoin

from SanskritAI.acquisition.repositories.base_repository_client import (
    BaseRepositoryClient,
)


class GretilRepositoryClient(BaseRepositoryClient):
    """
    Repository client for GRETIL.
    """

    BASE_URL = (
        "https://gretil.sub.uni-goettingen.de/"
    )

    CATALOG_URL = (
        "https://gretil.sub.uni-goettingen.de/gretil.html"
    )

    # ---------------------------------------------------------
    # Repository Identity
    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:

        return "gretil"

    # ---------------------------------------------------------

    @property
    def base_url(
        self,
    ) -> str:

        return self.BASE_URL

    # ---------------------------------------------------------

    @property
    def catalog_url(
        self,
    ) -> str:

        return self.CATALOG_URL

    # ---------------------------------------------------------
    # Repository Operations
    # ---------------------------------------------------------

    def fetch_catalog(
        self,
    ) -> str:
        """
        Download the GRETIL catalog HTML.

        Returns
        -------
        str
            HTML document.
        """

        response = self.downloader.get(
            self.catalog_url,
        )

        return response.text

    # ---------------------------------------------------------

    def resource_url(
        self,
        resource: str,
    ) -> str:
        """
        Construct an absolute repository URL.

        Parameters
        ----------
        resource
            Relative path or filename.

        Returns
        -------
        str
            Absolute URL.
        """

        return urljoin(
            self.base_url,
            resource,
        )

    # ---------------------------------------------------------

    def catalog_metadata(
        self,
    ) -> dict[str, str]:
        """
        Metadata describing this repository.
        """

        return {

            "identifier": self.identifier,

            "repository": "GRETIL",

            "homepage": self.base_url,

            "catalog": self.catalog_url,

            "organization":
                "University of Göttingen",

        }

    # ---------------------------------------------------------

    def supports_https(
        self,
    ) -> bool:

        return self.base_url.startswith(
            "https://"
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.identifier

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}("

            f"identifier={self.identifier!r}, "

            f"base_url={self.base_url!r})"

        )
