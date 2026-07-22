
from __future__ import annotations

"""
SanskritAI
==========

HTML Importer

Imports HTML/XHTML documents into the SanskritAI import pipeline.

Unlike the XML importer, this importer is intended for web pages and
HTML documents where the primary goal is extraction of readable corpus
content rather than preservation of presentation.

Typical sources include

* GRETIL HTML texts
* SanskritDocuments.org
* Digital library pages
* Downloaded HTML documents
* XHTML corpus exports

Responsibilities
----------------
* Parse HTML documents
* Extract document metadata
* Extract visible textual content
* Ignore presentation markup
* Produce ImportResult

This importer intentionally performs only lightweight structural
analysis. Semantic interpretation and Sanskrit-aware processing are
performed later in the NLP pipeline.

Version
-------
v0.8.0
"""

from pathlib import Path
from typing import Any
from html.parser import HTMLParser

from SanskritAI.acquisition.importers.base_importer import (
    BaseImporter,
)
from SanskritAI.acquisition.importers.import_result import (
    ImportResult,
)


class _TextExtractor(HTMLParser):
    """
    Internal HTML text extractor.
    """

    def __init__(self) -> None:

        super().__init__(convert_charrefs=True)

        self.title = ""

        self._inside_title = False

        self.text_parts: list[str] = []

        self.element_count = 0

        self.link_count = 0

        self.image_count = 0

    # ---------------------------------------------------------

    def handle_starttag(
        self,
        tag: str,
        attrs,
    ) -> None:

        self.element_count += 1

        tag = tag.lower()

        if tag == "title":

            self._inside_title = True

        elif tag == "a":

            self.link_count += 1

        elif tag == "img":

            self.image_count += 1

    # ---------------------------------------------------------

    def handle_endtag(
        self,
        tag: str,
    ) -> None:

        if tag.lower() == "title":

            self._inside_title = False

    # ---------------------------------------------------------

    def handle_data(
        self,
        data: str,
    ) -> None:

        text = data.strip()

        if not text:

            return

        if self._inside_title:

            self.title += text

        else:

            self.text_parts.append(text)

    # ---------------------------------------------------------

    @property
    def text(
        self,
    ) -> str:

        return "\n".join(self.text_parts)


class HtmlImporter(BaseImporter):
    """
    HTML document importer.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:

        return "html"

    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:

        return "HTML Importer"

    # ---------------------------------------------------------

    @property
    def supported_extensions(
        self,
    ) -> tuple[str, ...]:

        return (

            ".html",

            ".htm",

            ".xhtml",

        )

    # ---------------------------------------------------------
    # Import
    # ---------------------------------------------------------

    def _import(
        self,
        *,
        file: Path,
        result: ImportResult,
        **kwargs: Any,
    ) -> None:

        html = self.read_text(file)

        parser = _TextExtractor()

        parser.feed(html)

        parser.close()

        document_id = file.stem

        result.add_document(
            document_id
        )

        result.set_metadata(
            "filename",
            file.name,
        )

        result.set_metadata(
            "title",
            parser.title,
        )

        result.set_metadata(
            "extension",
            file.suffix.lower(),
        )

        result.set_metadata(
            "size_bytes",
            file.stat().st_size,
        )

        result.set_metadata(
            "html",
            True,
        )

        paragraphs = self._paragraphs(
            parser.text
        )

        for index, paragraph in enumerate(
            paragraphs,
            start=1,
        ):

            if not paragraph.strip():

                continue

            result.add_unit(

                f"{document_id}:paragraph:{index}"

            )

        result.increment(
            "characters",
            len(parser.text),
        )

        result.increment(
            "paragraphs",
            len(paragraphs),
        )

        result.increment(
            "elements",
            parser.element_count,
        )

        result.increment(
            "links",
            parser.link_count,
        )

        result.increment(
            "images",
            parser.image_count,
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _paragraphs(
        text: str,
    ) -> list[str]:

        paragraphs = []

        current = []

        for line in text.splitlines():

            if line.strip():

                current.append(line)

            else:

                if current:

                    paragraphs.append(
                        "\n".join(current)
                    )

                    current = []

        if current:

            paragraphs.append(
                "\n".join(current)
            )

        return paragraphs

    # ---------------------------------------------------------

    def metadata(
        self,
    ) -> dict[str, Any]:

        data = super().metadata()

        data.update(

            {

                "description":
                    "HTML/XHTML importer",

                "supports_title": True,

                "supports_links": True,

                "supports_images": True,

                "binary": False,

            }

        )

        return data

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}("

            f"extensions={self.supported_extensions})"

        )
