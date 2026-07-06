"""
SanskritAI
==========

Module:
    services.importers.amarakosha_importer

Description
-----------
High-level importer for the Amarakośa corpus.

The importer coordinates the complete import workflow while
delegating parsing to AmarakoshaParser.

Responsibilities
----------------
    • Load source text
    • Invoke the parser
    • Optionally update repositories
    • Return ImportResult

The importer intentionally contains no parsing logic.

Future Responsibilities
-----------------------
    • Repository integration
    • Lexeme generation
    • Relation generation
    • Progress reporting
    • Import logging

Version:
    v0.4.0
"""

from __future__ import annotations

from pathlib import Path

from models.imports import (
    ImportConfiguration,
    ImportResult,
)

from .amarakosha_parser import AmarakoshaParser


class AmarakoshaImporter:
    """
    High-level Amarakośa importer.

    Examples
    --------

    >>> importer = AmarakoshaImporter()
    >>> result = importer.import_file("amarakosha.txt")
    >>> print(result.status)
    """

    def __init__(
        self,
        configuration: ImportConfiguration | None = None,
    ) -> None:

        self.configuration = (
            configuration
            if configuration is not None
            else ImportConfiguration()
        )

        self.parser = AmarakoshaParser(
            self.configuration
        )

    # ---------------------------------------------------------
    # Import API
    # ---------------------------------------------------------

    def import_file(
        self,
        file_path: str | Path,
    ) -> ImportResult:
        """
        Import an Amarakośa source file.

        Parameters
        ----------
        file_path
            UTF-8 encoded Amarakośa text file.

        Returns
        -------
        ImportResult
        """

        return self.parser.parse_file(file_path)

    def import_text(
        self,
        text: str,
    ) -> ImportResult:
        """
        Import Amarakośa directly from text.
        """

        return self.parser.parse_text(text)

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def parser_name(self) -> str:
        """
        Name of the parser implementation.
        """

        return self.parser.__class__.__name__

    def __repr__(self) -> str:

        return (
            "AmarakoshaImporter("
            f"parser='{self.parser_name}')"
        )
