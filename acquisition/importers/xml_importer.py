
from __future__ import annotations

"""
SanskritAI
==========

XML Importer

Imports generic XML documents into the SanskritAI import pipeline.

This importer is intentionally XML-schema agnostic. It understands
well-formed XML but does not assume TEI, SARIT, or any other specific
schema. Schema-specific logic belongs in dedicated importers.

Responsibilities
----------------
* Parse well-formed XML
* Collect document metadata
* Traverse XML tree
* Register logical XML elements
* Produce ImportResult

Future schema-specific importers
--------------------------------
    TEIImporter
    SARITImporter
    CologneXMLImporter
    MuktabodhaXMLImporter

Version
-------
v0.8.0
"""

from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

from SanskritAI.acquisition.importers.base_importer import (
    BaseImporter,
)
from SanskritAI.acquisition.importers.import_result import (
    ImportResult,
)


class XmlImporter(BaseImporter):
    """
    Generic XML importer.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        return "xml"

    @property
    def display_name(self) -> str:
        return "Generic XML Importer"

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (
            ".xml",
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
        """
        Import an XML document.
        """

        tree = ET.parse(file)
        root = tree.getroot()

        document_id = file.stem

        result.add_document(document_id)

        result.set_metadata(
            "filename",
            file.name,
        )

        result.set_metadata(
            "extension",
            file.suffix.lower(),
        )

        result.set_metadata(
            "root_tag",
            self._local_name(root.tag),
        )

        result.set_metadata(
            "namespace",
            self._namespace(root.tag),
        )

        result.set_metadata(
            "size_bytes",
            file.stat().st_size,
        )

        # ------------------------------------------
        # Traverse XML
        # ------------------------------------------

        element_count = 0

        text_nodes = 0

        attribute_count = 0

        max_depth = 0

        for depth, element in self._walk(root):

            element_count += 1

            max_depth = max(
                max_depth,
                depth,
            )

            attribute_count += len(
                element.attrib
            )

            if (
                element.text
                and element.text.strip()
            ):

                text_nodes += 1

            unit_id = (
                f"{document_id}:"
                f"{element_count}"
            )

            result.add_unit(
                unit_id
            )

        result.increment(
            "elements",
            element_count,
        )

        result.increment(
            "text_nodes",
            text_nodes,
        )

        result.increment(
            "attributes",
            attribute_count,
        )

        result.increment(
            "tree_depth",
            max_depth,
        )

    # ---------------------------------------------------------
    # XML Traversal
    # ---------------------------------------------------------

    def _walk(
        self,
        element: ET.Element,
        depth: int = 0,
    ):
        """
        Depth-first XML traversal.
        """

        yield depth, element

        for child in element:

            yield from self._walk(
                child,
                depth + 1,
            )

    # ---------------------------------------------------------
    # XML Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _namespace(
        tag: str,
    ) -> str | None:
        """
        Extract XML namespace.
        """

        if tag.startswith("{"):

            return tag.split("}")[0][1:]

        return None

    # ---------------------------------------------------------

    @staticmethod
    def _local_name(
        tag: str,
    ) -> str:
        """
        Extract local tag name.
        """

        if tag.startswith("{"):

            return tag.split("}")[-1]

        return tag

    # ---------------------------------------------------------

    def metadata(self) -> dict[str, Any]:

        data = super().metadata()

        data.update(

            {

                "description":
                    "Generic XML importer.",

                "schema":
                    "Unknown",

                "binary":
                    False,

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
