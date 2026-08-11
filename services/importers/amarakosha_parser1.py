"""
SanskritAI
==========

Module:
    services.importers.amarakosha_parser

Description
-----------
Parser for Amarakośa source text.

This parser converts raw textual input into the canonical
Amarakosha domain model.

Responsibilities
----------------
• Parse source text
• Build Amarakosha object hierarchy
• Collect import statistics
• Report parsing errors
• Return ImportResult

The parser intentionally does NOT perform:

    • Repository updates
    • Lexeme generation
    • Database persistence

Those responsibilities belong to higher-level import services.

Version:
    v0.4.0
"""

from __future__ import annotations

from pathlib import Path

from models.amarakosha import (
    Amarakosha,
    Kanda,
    Varga,
    Verse,
)

from models.imports import (
    ImportConfiguration,
    ImportError,
    ImportResult,
    ImportStatus,
)


class AmarakoshaParser:
    """
    Parser for Amarakośa source files.
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

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def parse_file(
        self,
        file_path: str | Path,
    ) -> ImportResult:
        """
        Parse a UTF-8 Amarakośa text file.
        """

        path = Path(file_path)

        text = path.read_text(
            encoding="utf-8"
        )

        result = self.parse_text(text)

        result.add_metadata(
            "source_file",
            str(path),
        )

        return result

    def parse_text(
        self,
        text: str,
    ) -> ImportResult:
        """
        Parse Amarakośa text.
        """

        result = ImportResult()

        result.status = ImportStatus.RUNNING

        result.statistics.start()

        try:

            amarakosha = self._parse(text, result)

            result.imported_object = amarakosha

        except Exception as exc:

            result.add_error(

                ImportError(

                    message=str(exc),

                    severity="FATAL",

                    exception=type(exc).__name__,

                )

            )

        result.statistics.stop()

        result.finalize()

        return result

    # ---------------------------------------------------------
    # Internal Parser
    # ---------------------------------------------------------

    def _parse(
        self,
        text: str,
        result: ImportResult,
    ) -> Amarakosha:
        """
        Internal parsing routine.

        Current implementation builds an empty Amarakośa model.

        Commit 4 will introduce complete parsing logic.
        """

        book = Amarakosha()

        #
        # Future implementation
        #
        # Detect Kāṇḍa
        # Detect Varga
        # Detect Verse
        # Populate statistics
        #

        result.statistics.books = 1

        return book

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _create_kanda(
        self,
        number: int,
        name: str,
    ) -> Kanda:

        return Kanda(

            number=number,

            name=name,

        )

    def _create_varga(
        self,
        number: int,
        name: str,
    ) -> Varga:

        return Varga(

            number=number,

            name=name,

        )

    def _create_verse(
        self,
        number: int,
        text: str,
    ) -> Verse:

        return Verse(

            number=number,

            text=text,

        )
