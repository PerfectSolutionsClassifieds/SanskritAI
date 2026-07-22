
from __future__ import annotations

"""
SanskritAI
==========

Muktabodha Provider

Concrete acquisition provider for the
Muktabodha Digital Library.

The Muktabodha Digital Library is a major
repository of Sanskrit texts, particularly
covering Tantric, Śaiva, Śākta, and related
scriptural traditions. Resources are commonly
distributed as TEI/XML and Unicode text.

This provider specializes XmlCorpusProvider
and contributes only Muktabodha-specific
configuration and metadata.

Responsibilities
----------------
* Discover Muktabodha resources
* Acquire XML/TEI corpus files
* Advertise provider capabilities
* Supply repository metadata

The provider intentionally does NOT perform

    * XML parsing
    * Metadata extraction
    * Validation
    * Normalization
    * Importing

Those responsibilities belong to later stages
of the SanskritAI acquisition pipeline.

Architecture
------------

            BaseProvider
                  │
                  ▼
         XmlCorpusProvider
                  │
                  ▼
        MuktabodhaProvider

Version
-------
v0.7.0
"""

from __future__ import annotations

from typing import Any

from SanskritAI.acquisition.providers.xml_corpus_provider import (
    XmlCorpusProvider,
)
from SanskritAI.acquisition.repositories.base_repository_client import (
    BaseRepositoryClient,
)


class MuktabodhaProvider(XmlCorpusProvider):
    """
    Acquisition provider for the
    Muktabodha Digital Library.
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
        return "muktabodha"

    @property
    def display_name(self) -> str:
        return "Muktabodha Provider"

    # ---------------------------------------------------------
    # Repository Information
    # ---------------------------------------------------------

    @property
    def corpus_name(self) -> str:
        return "Muktabodha Digital Library"

    @property
    def publisher(self) -> str:
        return "Muktabodha"

    @property
    def primary_encoding(self) -> str:
        return "TEI/XML"

    # ---------------------------------------------------------
    # Preferred download order
    # ---------------------------------------------------------

    def preferred_formats(
        self,
    ) -> tuple[str, ...]:

        return (

            ".tei.xml",

            ".tei",

            ".xml",

            ".txt",

            ".zip",

            ".pdf",

        )

    # ---------------------------------------------------------
    # Corpus capabilities
    # ---------------------------------------------------------

    @property
    def supports_tantra(self) -> bool:
        return True

    @property
    def supports_agama(self) -> bool:
        return True

    @property
    def supports_shaiva(self) -> bool:
        return True

    @property
    def supports_shakta(self) -> bool:
        return True

    @property
    def supports_unicode(self) -> bool:
        return True

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
                    "Muktabodha",

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

                "supports_xml":
                    True,

                "supports_tei":
                    True,

                "supports_unicode":
                    self.supports_unicode,

                "supports_tantra":
                    self.supports_tantra,

                "supports_agama":
                    self.supports_agama,

                "supports_shaiva":
                    self.supports_shaiva,

                "supports_shakta":
                    self.supports_shakta,

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
