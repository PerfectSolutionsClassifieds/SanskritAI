
from __future__ import annotations

"""
SanskritAI
==========

GRETIL Acquisition Provider

Concrete AcquisitionProvider implementation for the
Göttingen Register of Electronic Texts in Indian Languages
(GRETIL).

Responsibilities
----------------
* Repository health check
* Catalog discovery
* Work searching
* Resource acquisition
* Metadata collection
* Integration with the downloader subsystem

This class intentionally contains very little parsing logic.
Catalog parsing is delegated to GretilCatalogParser.
Repository communication is delegated to GretilRepositoryClient.

Version
-------
v0.6.0
"""

from pathlib import Path
from typing import Iterable

from SanskritAI.acquisition.parsers.gretil_catalog_parser import (
    GretilCatalogParser,
)

from SanskritAI.acquisition.providers.acquisition_request import (
    AcquisitionRequest,
)

from SanskritAI.acquisition.providers.acquisition_response import (
    AcquisitionResponse,
)

from SanskritAI.acquisition.providers.base_provider import (
    BaseProvider,
)

from SanskritAI.acquisition.repositories.gretil_repository_client import (
    GretilRepositoryClient,
)


class GretilProvider(BaseProvider):
    """
    Acquisition provider for GRETIL.
    """

    def __init__(
        self,
        repository_client: GretilRepositoryClient | None = None,
        parser: GretilCatalogParser | None = None,
        **kwargs,
    ) -> None:

        super().__init__(**kwargs)

        self._repository = (
            repository_client
            or GretilRepositoryClient()
        )

        self._parser = (
            parser
            or GretilCatalogParser()
        )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    @property
    def identifier(self) -> str:

        return "gretil"

    @property
    def display_name(self) -> str:

        return "GRETIL"

    @property
    def homepage(self) -> str:

        return "https://gretil.sub.uni-goettingen.de"

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover(
        self,
        request: AcquisitionRequest,
    ) -> AcquisitionResponse:

        self.validate_request(request)

        response = self.create_response()

        try:

            catalog_text = self._repository.fetch_catalog()

            entries = self._parser.parse(
                catalog_text
            )

            if request.has_query:

                entries = self._filter_entries(
                    entries,
                    request.query,
                )

            for entry in entries:

                response.add_resource(
                    entry.title
                )

            response.set_metadata(
                "repository",
                self.identifier,
            )

            response.set_metadata(
                "catalog_entries",
                len(entries),
            )

        except Exception as exc:

            response.error(str(exc))

        response.finish()

        return response

    # ------------------------------------------------------------------
    # Acquisition
    # ------------------------------------------------------------------

    def acquire(
        self,
        request: AcquisitionRequest,
    ) -> AcquisitionResponse:

        self.validate_request(request)

        response = self.create_response()

        try:

            catalog = self.discover(
                request
            )

            if not catalog:

                response.error(
                    "Discovery failed."
                )

                response.finish()

                return response

            destination = (
                request.destination_directory
            )

            if destination is None:

                response.error(
                    "Destination directory required."
                )

                response.finish()

                return response

            downloaded = 0

            #
            # NOTE
            #
            # The actual download API of
            # GretilRepositoryClient may differ.
            #
            # Replace download_resource()
            # with the concrete implementation
            # when available.
            #

            for resource in catalog.discovered_resources:

                try:

                    output = (
                        self._repository
                        .download_resource(
                            resource,
                            destination,
                        )
                    )

                    if isinstance(
                        output,
                        Path,
                    ):

                        response.add_download(
                            output
                        )

                        downloaded += 1

                except Exception as exc:

                    response.warning(
                        f"{resource}: {exc}"
                    )

            response.increment(
                "downloaded",
                downloaded,
            )

            response.set_metadata(
                "repository",
                self.identifier,
            )

        except Exception as exc:

            response.error(str(exc))

        response.finish()

        return response

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:

        try:

            return (
                self._repository
                .ping()
            )

        except Exception:

            return False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _filter_entries(
        entries: Iterable,
        query: str,
    ) -> list:

        query = query.lower()

        results = []

        for entry in entries:

            title = getattr(
                entry,
                "title",
                "",
            )

            if query in title.lower():

                results.append(
                    entry
                )

        return results

    # ------------------------------------------------------------------

    @property
    def repository_client(
        self,
    ) -> GretilRepositoryClient:

        return self._repository

    @property
    def parser(
        self,
    ) -> GretilCatalogParser:

        return self._parser

    # ------------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"repository='{self.display_name}')"
        )
