
from __future__ import annotations

"""
SanskritAI
==========

PDF Importer

Reference implementation for importing PDF documents into the
SanskritAI Import Pipeline.

Design Philosophy
-----------------
The PDF importer is intentionally conservative.

It prefers extracting embedded Unicode text directly from digital PDFs.
If a page contains no extractable text (e.g., scanned image-only PDFs),
the importer records this condition and marks the document as requiring
OCR rather than attempting OCR itself.

OCR is delegated to future OCR providers, preserving separation of
concerns.

Pipeline
--------

PDF
 │
 ▼
PdfImporter
 │
 ├── Embedded Unicode Text
 │        │
 │        ▼
 │   ImportResult
 │
 └── Image-only PDF
          │
          ▼
     OCR Required
          │
          ▼
 Future OCR Pipeline

Dependencies
------------
Preferred:
    pypdf

Fallback:
    PyPDF2

If neither library is installed, an informative ImportResult is
returned instead of raising an exception.

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


class PdfImporter(BaseImporter):
    """
    Importer for PDF documents.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        return "pdf"

    @property
    def display_name(self) -> str:
        return "PDF Importer"

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (
            ".pdf",
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

        reader = self._load_reader()

        if reader is None:

            result.error(
                "Neither 'pypdf' nor 'PyPDF2' is installed."
            )

            return

        pdf = reader(file)

        document_id = file.stem

        result.add_document(document_id)

        result.set_metadata(
            "filename",
            file.name,
        )

        result.set_metadata(
            "extension",
            ".pdf",
        )

        result.set_metadata(
            "size_bytes",
            file.stat().st_size,
        )

        result.set_metadata(
            "page_count",
            len(pdf.pages),
        )

        extracted_pages = 0
        scanned_pages = 0
        total_characters = 0

        for page_number, page in enumerate(
            pdf.pages,
            start=1,
        ):

            try:

                text = page.extract_text() or ""

            except Exception:

                text = ""

            if text.strip():

                extracted_pages += 1

                total_characters += len(text)

                result.add_unit(
                    f"{document_id}:page:{page_number}"
                )

            else:

                scanned_pages += 1

                result.warning(
                    f"Page {page_number} contains no "
                    "extractable Unicode text."
                )

        result.increment(
            "pages",
            len(pdf.pages),
        )

        result.increment(
            "text_pages",
            extracted_pages,
        )

        result.increment(
            "scanned_pages",
            scanned_pages,
        )

        result.increment(
            "characters",
            total_characters,
        )

        # -------------------------------------------------
        # Metadata
        # -------------------------------------------------

        metadata = getattr(
            pdf,
            "metadata",
            None,
        )

        if metadata:

            safe_metadata = {}

            for key, value in metadata.items():

                try:

                    safe_metadata[str(key)] = (
                        str(value)
                        if value is not None
                        else ""
                    )

                except Exception:

                    continue

            result.set_metadata(
                "pdf_metadata",
                safe_metadata,
            )

        # -------------------------------------------------
        # OCR Hint
        # -------------------------------------------------

        if scanned_pages > 0:

            result.set_metadata(
                "ocr_required",
                True,
            )

            result.warning(
                "Document contains scanned pages. "
                "OCR pipeline is recommended."
            )

        else:

            result.set_metadata(
                "ocr_required",
                False,
            )

    # ---------------------------------------------------------
    # Internal Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _load_reader():
        """
        Load the first available PDF reader.
        """

        try:

            from pypdf import PdfReader

            return PdfReader

        except Exception:

            pass

        try:

            from PyPDF2 import PdfReader

            return PdfReader

        except Exception:

            pass

        return None

    # ---------------------------------------------------------

    def metadata(self) -> dict[str, Any]:

        data = super().metadata()

        data.update(

            {

                "description":
                    "PDF Importer",

                "binary": True,

                "supports_unicode_text": True,

                "supports_metadata": True,

                "supports_ocr_detection": True,

                "supports_page_import": True,

                "ocr_engine": None,

            }

        )

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(extensions={self.supported_extensions})"
        )
