
from __future__ import annotations

"""
SanskritAI
==========

Base Importer

Abstract foundation for every importer in the SanskritAI
Acquisition → Import Pipeline.

The purpose of an importer is to transform one normalized resource
(text, XML, TEI, HTML, PDF, etc.) into canonical SanskritAI corpus
objects.

Pipeline
--------

Normalized File
        │
        ▼
  BaseImporter
        │
        ▼
Concrete Importer
(TXT / XML / TEI / HTML / PDF)
        │
        ▼
 Parsed Document Model
        │
        ▼
 ImportResult

Responsibilities
----------------
* File validation
* Import orchestration
* Metadata extraction hook
* Statistics generation
* ImportResult creation

Concrete subclasses implement only the format-specific parsing logic.

Version
-------
v0.8.0
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from SanskritAI.acquisition.importers.import_result import (
    ImportResult,
)


class BaseImporter(ABC):
    """
    Abstract base class for every importer.
    """

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(
        self,
        *,
        encoding: str = "utf-8",
    ) -> None:

        self._encoding = encoding

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def identifier(self) -> str:
        """
        Unique importer identifier.

        Examples
        --------
        txt
        xml
        tei
        html
        pdf
        """
        ...

    # ---------------------------------------------------------

    @property
    @abstractmethod
    def display_name(self) -> str:
        """
        Human-readable importer name.
        """
        ...

    # ---------------------------------------------------------

    @property
    @abstractmethod
    def supported_extensions(
        self,
    ) -> tuple[str, ...]:
        """
        Supported filename extensions.

        Example
        -------
        (".txt",)
        """
        ...

    # ---------------------------------------------------------
    # Import
    # ---------------------------------------------------------

    def import_file(
        self,
        file: Path,
        **kwargs: Any,
    ) -> ImportResult:
        """
        Import a single file.

        This is the template method implemented by all importers.
        """

        self.validate_file(file)

        result = self.create_result(file)

        try:

            self._import(
                file=file,
                result=result,
                **kwargs,
            )

        except Exception as exc:

            result.error(str(exc))

        result.finish()

        return result

    # ---------------------------------------------------------
    # Abstract Implementation
    # ---------------------------------------------------------

    @abstractmethod
    def _import(
        self,
        *,
        file: Path,
        result: ImportResult,
        **kwargs: Any,
    ) -> None:
        """
        Format-specific implementation.

        Concrete importers implement this method.
        """
        ...

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_file(
        self,
        file: Path,
    ) -> None:
        """
        Validate the source file.
        """

        if not file.exists():

            raise FileNotFoundError(file)

        if not file.is_file():

            raise ValueError(
                f"Not a file: {file}"
            )

        extension = file.suffix.lower()

        if extension not in self.supported_extensions:

            raise ValueError(

                f"{self.display_name} "

                f"does not support "

                f"'{extension}'."

            )

    # ---------------------------------------------------------
    # Result Factory
    # ---------------------------------------------------------

    def create_result(
        self,
        file: Path,
    ) -> ImportResult:
        """
        Create a standardized ImportResult.
        """

        return ImportResult(

            importer_name=self.display_name,

            source_file=file,

        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def read_text(
        self,
        file: Path,
    ) -> str:
        """
        Read UTF-8 text.
        """

        return file.read_text(

            encoding=self.encoding,

        )

    # ---------------------------------------------------------

    def read_bytes(
        self,
        file: Path,
    ) -> bytes:
        """
        Read binary file.
        """

        return file.read_bytes()

    # ---------------------------------------------------------

    def supports(
        self,
        file: Path,
    ) -> bool:
        """
        Determine whether this importer
        supports the supplied file.
        """

        return (

            file.suffix.lower()

            in self.supported_extensions

        )

    # ---------------------------------------------------------

    @property
    def encoding(
        self,
    ) -> str:

        return self._encoding

    # ---------------------------------------------------------

    def metadata(
        self,
    ) -> dict[str, Any]:
        """
        Importer metadata.
        """

        return {

            "identifier": self.identifier,

            "display_name": self.display_name,

            "extensions":

                list(self.supported_extensions),

        }

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}("

            f"identifier={self.identifier!r}, "

            f"extensions={self.supported_extensions})"

        )
