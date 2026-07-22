
from __future__ import annotations

"""
SanskritAI
==========

Import Manager

High-level orchestration layer for the SanskritAI Import Pipeline.

Responsibilities
----------------
* Importer registration
* Importer selection
* Batch importing
* Recursive directory importing
* ImportResult aggregation
* Import statistics

The ImportManager is intentionally independent of any particular
file format. Concrete importers are selected automatically based
on the file extension.

Architecture
------------

                ImportManager
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   TxtImporter   XmlImporter   PdfImporter
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                ImportResult

Version
-------
v0.8.0
"""

from pathlib import Path
from typing import Iterable

from SanskritAI.acquisition.importers.base_importer import (
    BaseImporter,
)

from SanskritAI.acquisition.importers.import_result import (
    ImportResult,
)


class ImportManager:
    """
    Coordinates all importers.
    """

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(self) -> None:

        self._importers: dict[
            str,
            BaseImporter,
        ] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        importer: BaseImporter,
        *,
        replace: bool = False,
    ) -> None:
        """
        Register an importer.

        One importer may support multiple extensions.
        """

        for extension in importer.supported_extensions:

            extension = extension.lower()

            if (
                extension in self._importers
                and not replace
            ):

                raise ValueError(

                    f"Importer already registered "

                    f"for extension '{extension}'."

                )

            self._importers[
                extension
            ] = importer

    # ---------------------------------------------------------

    def unregister(
        self,
        extension: str,
    ) -> bool:

        extension = extension.lower()

        if extension not in self._importers:

            return False

        del self._importers[
            extension
        ]

        return True

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def importer_for(
        self,
        file: Path,
    ) -> BaseImporter:

        extension = file.suffix.lower()

        if extension not in self._importers:

            raise ValueError(

                f"No importer registered "

                f"for '{extension}'."

            )

        return self._importers[
            extension
        ]

    # ---------------------------------------------------------
    # Single File
    # ---------------------------------------------------------

    def import_file(
        self,
        file: Path,
        **kwargs,
    ) -> ImportResult:
        """
        Import a single file.
        """

        importer = self.importer_for(
            file
        )

        return importer.import_file(
            file,
            **kwargs,
        )

    # ---------------------------------------------------------
    # Multiple Files
    # ---------------------------------------------------------

    def import_files(
        self,
        files: Iterable[Path],
        **kwargs,
    ) -> ImportResult:
        """
        Import multiple files.
        """

        aggregate = ImportResult(

            importer_name="ImportManager",

            source_file=Path("<batch>"),

        )

        for file in files:

            result = self.import_file(

                file,

                **kwargs,

            )

            aggregate.merge(
                result
            )

        aggregate.finish()

        return aggregate

    # ---------------------------------------------------------
    # Directory Import
    # ---------------------------------------------------------

    def import_directory(
        self,
        directory: Path,
        *,
        recursive: bool = True,
        **kwargs,
    ) -> ImportResult:
        """
        Import every supported file
        from a directory.
        """

        if not directory.exists():

            raise FileNotFoundError(
                directory
            )

        if recursive:

            iterator = directory.rglob("*")

        else:

            iterator = directory.glob("*")

        files = [

            path

            for path in iterator

            if (
                path.is_file()
                and self.supports(path)
            )

        ]

        return self.import_files(

            files,

            **kwargs,

        )

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def supports(
        self,
        file: Path,
    ) -> bool:

        return (

            file.suffix.lower()

            in self._importers

        )

    # ---------------------------------------------------------

    @property
    def supported_extensions(
        self,
    ) -> tuple[str, ...]:

        return tuple(

            sorted(

                self._importers.keys()

            )

        )

    # ---------------------------------------------------------

    @property
    def importer_count(
        self,
    ) -> int:

        return len(

            {

                id(importer)

                for importer

                in self._importers.values()

            }

        )

    # ---------------------------------------------------------

    def importers(
        self,
    ) -> tuple[
        BaseImporter,
        ...
    ]:

        unique = {}

        for importer in self._importers.values():

            unique[id(importer)] = importer

        return tuple(

            unique.values()

        )

    # ---------------------------------------------------------

    def metadata(
        self,
    ) -> dict:

        return {

            "supported_extensions":

                list(

                    self.supported_extensions

                ),

            "importer_count":

                self.importer_count,

        }

    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:

        self._importers.clear()

    # ---------------------------------------------------------

    def __contains__(
        self,
        extension: str,
    ) -> bool:

        return (

            extension.lower()

            in self._importers

        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.importer_count

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}("

            f"importers={self.importer_count}, "

            f"extensions={len(self._importers)})"

        )
