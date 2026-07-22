
from __future__ import annotations

"""
SanskritAI
==========

TEI Importer

Concrete importer for TEI (Text Encoding Initiative) XML documents.

Unlike the generic XmlImporter, this importer understands the
high-level structure of TEI documents and extracts useful corpus
metadata while remaining independent of any database layer.

Supported TEI Concepts
----------------------
* teiHeader
* fileDesc
* titleStmt
* publicationStmt
* sourceDesc
* text
* front
* body
* back
* div
* lg (line group)
* l (line / verse)

This importer is intentionally conservative.

It parses document structure but does not attempt:

* Sanskrit NLP
* grammar analysis
* sandhi splitting
* verse metre identification
* semantic annotation

Those belong to later NLP stages.

Version
-------
v0.8.0
"""

from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

from SanskritAI.acquisition.importers.import_result import (
    ImportResult,
)
from SanskritAI.acquisition.importers.xml_importer import (
    XmlImporter,
)


class TeiImporter(XmlImporter):
    """
    Importer for TEI XML documents.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        return "tei"

    @property
    def display_name(self) -> str:
        return "TEI Importer"

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (
            ".tei",
            ".tei.xml",
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

        tree = ET.parse(file)
        root = tree.getroot()

        document_id = file.stem

        result.add_document(document_id)

        result.set_metadata(
            "filename",
            file.name,
        )

        result.set_metadata(
            "tei",
            True,
        )

        result.set_metadata(
            "root_tag",
            self._local_name(root.tag),
        )

        result.set_metadata(
            "namespace",
            self._namespace(root.tag),
        )

        # -----------------------------------------------------
        # TEI Header
        # -----------------------------------------------------

        title = self._find_first_text(
            root,
            "title",
        )

        if title:

            result.set_metadata(
                "title",
                title,
            )

        author = self._find_first_text(
            root,
            "author",
        )

        if author:

            result.set_metadata(
                "author",
                author,
            )

        publisher = self._find_first_text(
            root,
            "publisher",
        )

        if publisher:

            result.set_metadata(
                "publisher",
                publisher,
            )

        # -----------------------------------------------------
        # Structural statistics
        # -----------------------------------------------------

        divisions = 0
        verse_groups = 0
        verses = 0
        paragraphs = 0
        elements = 0

        for _, element in self._walk(root):

            elements += 1

            tag = self._local_name(
                element.tag
            )

            if tag == "div":
                divisions += 1

            elif tag == "lg":
                verse_groups += 1

            elif tag == "l":
                verses += 1

            elif tag == "p":
                paragraphs += 1

            result.add_unit(
                f"{document_id}:{elements}"
            )

        result.increment(
            "elements",
            elements,
        )

        result.increment(
            "divisions",
            divisions,
        )

        result.increment(
            "verse_groups",
            verse_groups,
        )

        result.increment(
            "verses",
            verses,
        )

        result.increment(
            "paragraphs",
            paragraphs,
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _find_first_text(
        self,
        root: ET.Element,
        tag_name: str,
    ) -> str | None:
        """
        Find the first occurrence of a local tag name
        regardless of namespace.
        """

        for element in root.iter():

            if (
                self._local_name(element.tag)
                == tag_name
            ):

                if (
                    element.text
                    and element.text.strip()
                ):

                    return element.text.strip()

        return None

    # ---------------------------------------------------------

    def metadata(self) -> dict[str, Any]:

        data = super().metadata()

        data.update(

            {

                "schema": "TEI",

                "description":
                    "TEI XML Importer",

                "supports_namespaces": True,

                "supports_header": True,

                "supports_divisions": True,

                "supports_line_groups": True,

                "supports_verse_lines": True,

            }

        )

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(extensions={self.supported_extensions})"
        )
