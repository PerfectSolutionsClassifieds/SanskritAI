
from __future__ import annotations

"""
SanskritAI
==========

Acquisition Source Formats

Defines the physical representation (serialization/storage format)
of external acquisition sources.

This enumeration is intentionally independent of SourceType.

Examples
--------
SourceType.LEXICON
    ↳ XML
    ↳ JSON
    ↳ CSV

SourceType.CORPUS
    ↳ TXT
    ↳ TEI_XML
    ↳ PDF
    ↳ EPUB

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from enum import Enum


class SourceFormat(str, Enum):
    """
    Physical storage format of an acquisition source.
    """

    # Plain Unicode text
    TEXT = "text"

    # Plain UTF-8 text
    TXT = "txt"

    # XML
    XML = "xml"

    # TEI XML
    TEI_XML = "tei_xml"

    # JSON
    JSON = "json"

    # YAML
    YAML = "yaml"

    # CSV
    CSV = "csv"

    # TSV
    TSV = "tsv"

    # Spreadsheet
    XLSX = "xlsx"

    # SQLite database
    SQLITE = "sqlite"

    # Generic SQL dump
    SQL = "sql"

    # PDF document
    PDF = "pdf"

    # EPUB
    EPUB = "epub"

    # HTML
    HTML = "html"

    # Markdown
    MARKDOWN = "markdown"

    # ZIP archive
    ZIP = "zip"

    # TAR archive
    TAR = "tar"

    # GZIP archive
    GZIP = "gzip"

    # OCR image
    IMAGE = "image"

    # JPEG
    JPEG = "jpeg"

    # PNG
    PNG = "png"

    # TIFF
    TIFF = "tiff"

    # Unknown
    UNKNOWN = "unknown"

    @property
    def is_text(self) -> bool:
        """
        Returns True if this format contains directly readable text.
        """
        return self in {
            SourceFormat.TEXT,
            SourceFormat.TXT,
            SourceFormat.XML,
            SourceFormat.TEI_XML,
            SourceFormat.JSON,
            SourceFormat.YAML,
            SourceFormat.CSV,
            SourceFormat.TSV,
            SourceFormat.MARKDOWN,
            SourceFormat.HTML,
        }

    @property
    def is_structured(self) -> bool:
        """
        Returns True if this format has an explicit structure
        suitable for direct parsing.
        """
        return self in {
            SourceFormat.XML,
            SourceFormat.TEI_XML,
            SourceFormat.JSON,
            SourceFormat.YAML,
            SourceFormat.CSV,
            SourceFormat.TSV,
            SourceFormat.SQLITE,
            SourceFormat.SQL,
            SourceFormat.XLSX,
        }

    @property
    def is_archive(self) -> bool:
        """
        Returns True if this format is an archive container.
        """
        return self in {
            SourceFormat.ZIP,
            SourceFormat.TAR,
            SourceFormat.GZIP,
        }

    @property
    def requires_ocr(self) -> bool:
        """
        Returns True if the source is typically image-based and
        requires OCR before linguistic processing.
        """
        return self in {
            SourceFormat.IMAGE,
            SourceFormat.JPEG,
            SourceFormat.PNG,
            SourceFormat.TIFF,
        }

    @property
    def is_document(self) -> bool:
        """
        Returns True if the format represents a document container.
        """
        return self in {
            SourceFormat.PDF,
            SourceFormat.EPUB,
        }

    @classmethod
    def from_extension(cls, extension: str) -> "SourceFormat":
        """
        Determine SourceFormat from a filename extension.

        Examples
        --------
        >>> SourceFormat.from_extension(".xml")
        SourceFormat.XML
        """

        ext = extension.strip().lower().lstrip(".")

        mapping = {
            "txt": cls.TXT,
            "text": cls.TEXT,
            "xml": cls.XML,
            "tei": cls.TEI_XML,
            "json": cls.JSON,
            "yaml": cls.YAML,
            "yml": cls.YAML,
            "csv": cls.CSV,
            "tsv": cls.TSV,
            "xlsx": cls.XLSX,
            "sqlite": cls.SQLITE,
            "db": cls.SQLITE,
            "sql": cls.SQL,
            "pdf": cls.PDF,
            "epub": cls.EPUB,
            "html": cls.HTML,
            "htm": cls.HTML,
            "md": cls.MARKDOWN,
            "zip": cls.ZIP,
            "tar": cls.TAR,
            "gz": cls.GZIP,
            "gzip": cls.GZIP,
            "jpg": cls.JPEG,
            "jpeg": cls.JPEG,
            "png": cls.PNG,
            "tif": cls.TIFF,
            "tiff": cls.TIFF,
        }

        return mapping.get(ext, cls.UNKNOWN)

    def __str__(self) -> str:
        return self.value
