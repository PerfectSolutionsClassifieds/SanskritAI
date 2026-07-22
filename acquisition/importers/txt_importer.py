
from __future__ import annotations

"""
SanskritAI
==========

TXT Importer

Reference implementation of the SanskritAI Import Pipeline.

Responsibilities
----------------
* Import normalized UTF-8 text files
* Read plain text resources
* Extract lightweight document metadata
* Split text into logical units
* Produce a standardized ImportResult

The TxtImporter intentionally performs only lightweight parsing.
Advanced Sanskrit-aware parsing (śloka detection, chapter detection,
grammar analysis, etc.) belongs to later NLP and corpus processing
stages.

Pipeline
--------

TXT File
    │
    ▼
TxtImporter
    │
    ▼
Logical Units
    │
    ▼
ImportResult

Version
-------
v0.8.0
"""

from pathlib import Path
from typing import Any

from SanskritAI.acquisition.importers.base_importer import (
    BaseImporter,
)
from SanskritAI.acquisition.importers.import_result import (
    ImportResult,
)


class TxtImporter(BaseImporter):
    """
    Imports UTF-8 plain text files.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        return "txt"

    @property
    def display_name(self) -> str:
        return "Plain Text Importer"

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (
            ".txt",
            ".text",
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
        Import a normalized text file.
        """

        text = self.read_text(file)

        result.set_metadata(
            "filename",
            file.name,
        )

        result.set_metadata(
            "extension",
            file.suffix.lower(),
        )

        result.set_metadata(
            "encoding",
            self.encoding,
        )

        result.set_metadata(
            "size_bytes",
            file.stat().st_size,
        )

        # ------------------------------------------
        # Document registration
        # ------------------------------------------

        document_id = file.stem

        result.add_document(document_id)

        # ------------------------------------------
        # Split into logical units
        #
        # Current implementation:
        #     paragraph-based
        #
        # Future versions may delegate to:
        #
        #   VerseSegmenter
        #   ChapterDetector
        #   ŚlokaDetector
        #   ProseSegmenter
        #
        # ------------------------------------------

        paragraphs = self._split_into_units(text)

        for index, paragraph in enumerate(
            paragraphs,
            start=1,
        ):

            if not paragraph.strip():

                continue

            unit_id = (
                f"{document_id}:unit:{index}"
            )

            result.add_unit(unit_id)

        # ------------------------------------------

        result.increment(
            "characters",
            len(text),
        )

        result.increment(
            "lines",
            len(text.splitlines()),
        )

        result.increment(
            "paragraphs",
            len(paragraphs),
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _split_into_units(
        text: str,
    ) -> list[str]:
        """
        Split a text document into logical units.

        Current strategy:
            Blank-line separated paragraphs.

        This method is intentionally simple and
        serves as the foundation for future
        Sanskrit-aware segmentation.
        """

        units = []

        current = []

        for line in text.splitlines():

            if line.strip():

                current.append(line)

            else:

                if current:

                    units.append(
                        "\n".join(current)
                    )

                    current = []

        if current:

            units.append(
                "\n".join(current)
            )

        return units

    # ---------------------------------------------------------

    def metadata(self) -> dict[str, Any]:
        """
        Extended importer metadata.
        """

        data = super().metadata()

        data.update(

            {

                "description":
                    "Imports normalized UTF-8 text documents.",

                "segmentation":
                    "paragraph",

                "binary":
                    False,

            }

        )

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"{self.__class__.__name__}("

            f"extensions={self.supported_extensions})"

        )
