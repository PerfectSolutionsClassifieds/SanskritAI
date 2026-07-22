
from __future__ import annotations

"""
SanskritAI
==========

Source Format Detector

Determines the physical representation (SourceFormat) of a corpus
resource.

Responsibilities
----------------
* Detect file format from filename/path
* Support case-insensitive extensions
* Support compound extensions (future)
* Remain completely stateless

This detector intentionally does NOT:

    • inspect file contents
    • determine encoding
    • validate files
    • create CorpusSource objects

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from pathlib import Path

from SanskritAI.acquisition.models.source_format import SourceFormat


class SourceFormatDetector:
    """
    Detects SourceFormat from filenames or paths.
    """

    #
    # Canonical extension mapping.
    #
    _EXTENSIONS: dict[str, SourceFormat] = {
        ".txt": SourceFormat.TEXT,
        ".xml": SourceFormat.XML,
        ".tei": SourceFormat.TEI,
        ".tei.xml": SourceFormat.TEI,
        ".json": SourceFormat.JSON,
        ".csv": SourceFormat.CSV,
        ".tsv": SourceFormat.TSV,
        ".pdf": SourceFormat.PDF,
        ".zip": SourceFormat.ZIP,
        ".gz": SourceFormat.GZIP,
        ".tar": SourceFormat.TAR,
        ".tar.gz": SourceFormat.TAR_GZIP,
        ".tgz": SourceFormat.TAR_GZIP,
        ".7z": SourceFormat.SEVEN_ZIP,
        ".rar": SourceFormat.RAR,
        ".html": SourceFormat.HTML,
        ".htm": SourceFormat.HTML,
        ".md": SourceFormat.MARKDOWN,
    }

    # ---------------------------------------------------------
    # Detection API
    # ---------------------------------------------------------

    @classmethod
    def detect(
        cls,
        path: str | Path,
    ) -> SourceFormat | None:
        """
        Detect the SourceFormat of a file.

        Parameters
        ----------
        path
            File path or filename.

        Returns
        -------
        SourceFormat | None
        """

        path = Path(path)

        filename = path.name.lower()

        #
        # Match longest extension first.
        #

        for extension in sorted(
            cls._EXTENSIONS,
            key=len,
            reverse=True,
        ):
            if filename.endswith(extension):
                return cls._EXTENSIONS[extension]

        return None

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @classmethod
    def is_supported(
        cls,
        path: str | Path,
    ) -> bool:
        """
        Returns True if the file format is supported.
        """

        return cls.detect(path) is not None

    @classmethod
    def supported_extensions(
        cls,
    ) -> tuple[str, ...]:
        """
        Returns supported file extensions.
        """

        return tuple(sorted(cls._EXTENSIONS))

    @classmethod
    def register_extension(
        cls,
        extension: str,
        source_format: SourceFormat,
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Register a new extension.
        """

        extension = extension.lower()

        if not extension.startswith("."):
            extension = "." + extension

        if (
            extension in cls._EXTENSIONS
            and not overwrite
        ):
            raise ValueError(
                f"Extension '{extension}' is already registered."
            )

        cls._EXTENSIONS[extension] = source_format

    @classmethod
    def unregister_extension(
        cls,
        extension: str,
    ) -> None:
        """
        Remove a registered extension.
        """

        extension = extension.lower()

        if not extension.startswith("."):
            extension = "." + extension

        cls._EXTENSIONS.pop(extension, None)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            "SourceFormatDetector("
            f"supported={len(self._EXTENSIONS)})"
        )
