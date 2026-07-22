
from __future__ import annotations

"""
SanskritAI
==========

XML Corpus Provider

Abstract acquisition provider for scholarly XML/TEI repositories.

Purpose
-------
Many Sanskrit digital libraries publish their corpus primarily as
XML or TEI XML.

Examples

    • SARIT
    • Cologne Digital Sanskrit Lexicon
    • Muktabodha
    • Future TEI repositories

Rather than duplicating XML-specific acquisition logic in every
provider, this class centralizes the common behaviour.

Responsibilities
----------------
* Resource discovery
* Download orchestration
* XML-oriented format preference
* Repository health checking
* AcquisitionResponse generation

Not Responsible For
-------------------
* XML parsing
* TEI interpretation
* Metadata extraction
* Validation
* Normalization
* Importing

Those stages belong elsewhere in the acquisition pipeline.

Inheritance
-----------

            BaseProvider
                  │
                  ▼
         XmlCorpusProvider
          │      │       │
          ▼      ▼       ▼
      Sarit   Cologne  Muktabodha

Version
-------
v0.7.0
"""

from pathlib import Path
from typing import Iterable

from SanskritAI.acquisition.providers.base_provider import BaseProvider
from SanskritAI.acquisition.providers.acquisition_request import (
    AcquisitionRequest,
)
from SanskritAI.acquisition.providers.acquisition_response import (
    AcquisitionResponse,
)
from SanskritAI.acquisition.repositories.base_repository_client import (
    BaseRepositoryClient,
)


class XmlCorpusProvider(BaseProvider):
    """
    Base provider for XML/TEI scholarly repositories.
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
    # Discovery
    # ---------------------------------------------------------

    def discover(
        self,
        request: AcquisitionRequest,
    ) -> Iterable:

        return self.repository.discover(request)

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

        resources = self.discover(request)

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

                response.error(str(exc))

        response.finish()

        return response

    # ---------------------------------------------------------
    # Preferred XML formats
    # ---------------------------------------------------------

    def supported_extensions(
        self,
    ) -> tuple[str, ...]:

        return (

            ".tei.xml",

            ".tei",

            ".xml",

            ".txt",

            ".json",

            ".yaml",

            ".yml",

            ".csv",

            ".zip",

            ".gz",

        )

    # ---------------------------------------------------------

    def preferred_formats(
        self,
    ) -> tuple[str, ...]:
        """
        Preferred acquisition order.

        XML is preferred over plain text because it
        preserves scholarly markup.
        """

        return (

            ".tei.xml",

            ".tei",

            ".xml",

            ".txt",

            ".json",

            ".zip",

        )

    # ---------------------------------------------------------

    def supports_extension(
        self,
        extension: str,
    ) -> bool:

        return extension.lower() in self.supported_extensions()

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def metadata(
        self,
    ) -> dict:

        data = super().metadata()

        data.update(

            {

                "supports_xml": True,

                "supports_tei": True,

                "supports_unicode": True,

                "supports_incremental": True,

                "preferred_importer": "tei",

                "provider_type": "xml_corpus",

            }

        )

        return data

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
