
from __future__ import annotations

"""
SanskritAI
==========

GRETIL Catalog Parser

Parses the GRETIL repository catalog into CorpusSource objects.

Responsibilities
----------------
* Parse GRETIL HTML catalog pages
* Extract downloadable corpus entries
* Construct CorpusSource objects
* Ignore unsupported resources

Version
-------
v0.5.0
"""

from html.parser import HTMLParser
from urllib.parse import urljoin

from SanskritAI.acquisition.factories.corpus_source_factory import (
    CorpusSourceFactory,
)
from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.models.source_type import SourceType
from SanskritAI.acquisition.parsers.base_catalog_parser import (
    BaseCatalogParser,
)


class _GretilHTMLParser(HTMLParser):
    """
    Lightweight HTML parser for GRETIL catalog pages.

    Collects hyperlinks encountered while parsing.
    """

    def __init__(self) -> None:

        super().__init__()

        self.links: list[tuple[str, str]] = []

        self._href: str | None = None
        self._capture_text = False
        self._text: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs,
    ) -> None:

        if tag.lower() != "a":
            return

        attributes = dict(attrs)

        href = attributes.get("href")

        if href is None:
            return

        self._href = href
        self._capture_text = True
        self._text = []

    def handle_data(
        self,
        data: str,
    ) -> None:

        if self._capture_text:
            self._text.append(data)

    def handle_endtag(
        self,
        tag: str,
    ) -> None:

        if tag.lower() != "a":
            return

        if self._href:

            title = "".join(self._text).strip()

            self.links.append(
                (
                    self._href,
                    title,
                )
            )

        self._href = None
        self._capture_text = False
        self._text = []


class GretilCatalogParser(BaseCatalogParser):
    """
    Parses the GRETIL catalog.
    """

    SUPPORTED_EXTENSIONS = (
        ".txt",
        ".xml",
        ".tei",
        ".zip",
        ".pdf",
    )

    def __init__(
        self,
        *,
        base_url: str = (
            "https://gretil.sub.uni-goettingen.de"
        ),
    ) -> None:

        super().__init__()

        self._base_url = base_url.rstrip("/")

    # ---------------------------------------------------------
    # Parsing
    # ---------------------------------------------------------

    def parse(
        self,
        content: str | bytes,
    ) -> list[CorpusSource]:

        self.clear_diagnostics()

        if isinstance(content, bytes):
            content = content.decode(
                "utf-8",
                errors="replace",
            )

        parser = _GretilHTMLParser()

        parser.feed(content)

        sources: list[CorpusSource] = []

        for href, title in parser.links:

            if not self._is_supported(href):
                continue

            try:

                source = CorpusSourceFactory.from_url(
                    url=urljoin(
                        self._base_url,
                        href,
                    ),
                    title=title or self._title_from_href(href),
                    source_type=SourceType.GRETIL,
                )

                sources.append(source)

            except Exception as exc:

                self.add_warning(
                    f"Skipped '{href}': {exc}"
                )

        return sources

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        content: str |bytes,
    ) -> bool:

        if not content:
            return False

        if isinstance(content, bytes):
            return len(content) > 0

        return "<html" in content.lower()

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _is_supported(
        self,
        href: str,
    ) -> bool:

        href = href.lower()

        return href.endswith(
            self.SUPPORTED_EXTENSIONS
        )

    @staticmethod
    def _title_from_href(
        href: str,
    ) -> str:

        filename = href.rsplit("/", 1)[-1]

        for extension in (
            ".tei.xml",
            ".xml",
            ".txt",
            ".pdf",
            ".zip",
        ):
            if filename.endswith(extension):
                return filename[:-len(extension)]

        return filename

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def metadata(self) -> dict:

        return {
            "repository": "GRETIL",
            "base_url": self._base_url,
            "supported_extensions":
                self.SUPPORTED_EXTENSIONS,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "GretilCatalogParser("
            f"base_url='{self._base_url}')"
        )
