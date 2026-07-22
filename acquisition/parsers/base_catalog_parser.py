
from __future__ import annotations

"""
SanskritAI
==========

Base Catalog Parser

Defines the abstract interface implemented by every repository
catalog parser.

A catalog parser converts a repository-specific catalog
representation (HTML, XML, JSON, etc.) into a collection of
CorpusSource domain objects.

Responsibilities
----------------
* Parse repository catalogs
* Extract corpus metadata
* Produce CorpusSource objects
* Report parsing diagnostics

Catalog parsers intentionally do NOT:

    • perform HTTP requests
    • download corpus files
    • validate resources
    • normalize corpus text
    • import corpora

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from SanskritAI.acquisition.models.corpus_source import CorpusSource


class BaseCatalogParser(ABC):
    """
    Abstract base class for repository catalog parsers.
    """

    def __init__(self) -> None:

        self._warnings: list[str] = []
        self._errors: list[str] = []

    # ------------------------------------------------------------------
    # Primary Parsing API
    # ------------------------------------------------------------------

    @abstractmethod
    def parse(
        self,
        content: str | bytes,
    ) -> Iterable[CorpusSource]:
        """
        Parse repository catalog content.

        Parameters
        ----------
        content
            Raw catalog content (HTML, XML, JSON, etc.)

        Returns
        -------
        Iterable[CorpusSource]
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Validation Hook
    # ------------------------------------------------------------------

    def validate(
        self,
        content: str | bytes,
    ) -> bool:
        """
        Validate catalog content prior to parsing.

        Subclasses may override this method.
        """

        return bool(content)

    # ------------------------------------------------------------------
    # Convenience API
    # ------------------------------------------------------------------

    def parse_if_valid(
        self,
        content: str | bytes,
    ) -> Iterable[CorpusSource]:
        """
        Validate then parse.

        Raises
        ------
        ValueError
            If validation fails.
        """

        if not self.validate(content):
            raise ValueError(
                "Catalog content failed validation."
            )

        return self.parse(content)

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    @property
    def warnings(self) -> tuple[str, ...]:
        """
        Parser warnings.
        """
        return tuple(self._warnings)

    @property
    def errors(self) -> tuple[str, ...]:
        """
        Parser errors.
        """
        return tuple(self._errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self._warnings)

    @property
    def has_errors(self) -> bool:
        return bool(self._errors)

    def add_warning(
        self,
        message: str,
    ) -> None:

        self._warnings.append(message)

    def add_error(
        self,
        message: str,
    ) -> None:

        self._errors.append(message)

    def clear_diagnostics(self) -> None:
        """
        Clear warnings and errors.
        """

        self._warnings.clear()
        self._errors.clear()

    # ------------------------------------------------------------------
    # Optional Helpers
    # ------------------------------------------------------------------

    def metadata(self) -> dict[str, Any]:
        """
        Optional parser metadata.

        Subclasses may override to expose parser-specific
        statistics or diagnostics.
        """

        return {}

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"warnings={len(self._warnings)}, "
            f"errors={len(self._errors)})"
        )
