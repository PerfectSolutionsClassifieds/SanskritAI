
from __future__ import annotations

"""
SanskritAI
==========

Cologne Provider

Concrete acquisition provider for the
Cologne Digital Sanskrit Lexicon (CDSL).

The Cologne collection contains one of the
largest collections of digitized Sanskrit
lexical resources and related XML/text
datasets.

Examples include

    • Monier-Williams
    • Apte
    • Vācaspatyam
    • Śabdakalpadruma
    • Wilson
    • Böhtlingk
    • Various lexical indices

This provider specializes XmlCorpusProvider.

Responsibilities
----------------
* Discover Cologne resources
* Acquire XML/TXT resources
* Provide Cologne-specific metadata

The provider delegates repository access to
its RepositoryClient.

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


class CologneProvider(XmlCorpusProvider):
    """
    Acquisition provider for the
    Cologne Digital Sanskrit Lexicon.
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

        return "cologne"

    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:

        return "Cologne Provider"

    # ---------------------------------------------------------
    # Repository Information
    # ---------------------------------------------------------

    @property
    def corpus_name(self) -> str:

        return "Cologne Digital Sanskrit Lexicon"

    # ---------------------------------------------------------

    @property
    def publisher(self) -> str:

        return "Cologne Digital Sanskrit Lexicon"

    # ---------------------------------------------------------

    @property
    def primary_encoding(self) -> str:

        return "XML"

    # ---------------------------------------------------------

    @property
    def preferred_formats(
        self,
    ) -> tuple[str, ...]:
        """
        Preferred download order.

        Cologne commonly provides XML together
        with plain text resources.
        """

        return (

            ".xml",

            ".tei.xml",

            ".tei",

            ".txt",

            ".json",

            ".zip",

        )

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    @property
    def supports_lexicons(self) -> bool:

        return True

    # ---------------------------------------------------------

    @property
    def supports_dictionaries(self) -> bool:

        return True

    # ---------------------------------------------------------

    @property
    def supports_word_indices(self) -> bool:

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
                    "Cologne",

                "repository":
                    self.repository.identifier,

                "corpus":
                    self.corpus_name,

                "publisher":
                    self.publisher,

                "encoding":
                    self.primary_encoding,

                "preferred_importer":
                    "xml",

                "supports_xml":
                    True,

                "supports_unicode":
                    True,

                "supports_lexicons":
                    self.supports_lexicons,

                "supports_dictionaries":
                    self.supports_dictionaries,

                "supports_word_indices":
                    self.supports_word_indices,

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
