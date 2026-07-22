
from __future__ import annotations

"""
SanskritAI
==========

SARIT Provider

Concrete acquisition provider for the
Sanskrit Library / SARIT corpus.

SARIT (Search and Retrieval of Indic Texts)
is one of the highest-quality scholarly
digital Sanskrit collections and primarily
publishes TEI/XML encoded texts.

This provider specializes the generic
XmlCorpusProvider.

Responsibilities
----------------
* Discover SARIT resources
* Acquire SARIT XML/TEI documents
* Provide SARIT-specific metadata
* Select preferred XML formats

The provider intentionally delegates

    * HTTP communication
    * Repository traversal
    * Downloading

to the RepositoryClient.

Likewise, it does NOT perform

    * XML parsing
    * Metadata extraction
    * Validation
    * Normalization
    * Importing

Those stages belong to later acquisition
pipeline components.

Architecture
------------

              BaseProvider
                    │
                    ▼
          XmlCorpusProvider
                    │
                    ▼
             SaritProvider

Version
-------
v0.7.0
"""

from typing import Any

from SanskritAI.acquisition.providers.xml_corpus_provider import (
    XmlCorpusProvider,
)
from SanskritAI.acquisition.repositories.base_repository_client import (
    BaseRepositoryClient,
)


class SaritProvider(XmlCorpusProvider):
    """
    Acquisition provider for SARIT.
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

        return "sarit"

    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:

        return "SARIT Provider"

    # ---------------------------------------------------------
    # Repository Characteristics
    # ---------------------------------------------------------

    @property
    def preferred_formats(
        self,
    ) -> tuple[str, ...]:
        """
        Preferred acquisition order for SARIT.
        """

        return (

            ".tei.xml",

            ".tei",

            ".xml",

            ".txt",

            ".zip",

        )

    # ---------------------------------------------------------

    @property
    def corpus_name(
        self,
    ) -> str:

        return "SARIT"

    # ---------------------------------------------------------

    @property
    def publisher(
        self,
    ) -> str:

        return "Search and Retrieval of Indic Texts"

    # ---------------------------------------------------------

    @property
    def primary_encoding(
        self,
    ) -> str:

        return "TEI P5 XML"

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def metadata(
        self,
    ) -> dict[str, Any]:

        data = super().metadata()

        data.update(

            {

                "provider":

                    "SARIT",

                "repository":

                    self.repository.identifier,

                "corpus":

                    self.corpus_name,

                "publisher":

                    self.publisher,

                "encoding":

                    self.primary_encoding,

                "preferred_importer":

                    "tei",

                "supports_tei":

                    True,

                "supports_xml":

                    True,

                "supports_unicode":

                    True,

                "supports_versioning":

                    True,

                "supports_incremental":

                    True,

                "scholarly_corpus":

                    True,

            }

        )

        return data

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health_check(
        self,
    ) -> bool:

        return super().health_check()

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}("

            f"repository={self.repository.identifier!r})"

        )
