
from __future__ import annotations

"""
SanskritAI
==========

Canonical Work Registry

Loads and manages the canonical Sanskrit work registry.

Responsibilities
----------------
* Load work_registry.json
* Validate registry
* Convert JSON into domain objects
* Cache registry
* Lookup works
* Provide repository-style access

The registry is the single source of truth for canonical Sanskrit
works known to SanskritAI.

Version
-------
v0.6.0
"""

from functools import lru_cache
import json
from pathlib import Path
from typing import Iterator

from SanskritAI.acquisition.metadata.models.work_definition import (
    WorkDefinition,
)


class WorkRegistry:
    """
    Repository of canonical Sanskrit works.
    """

    DEFAULT_REGISTRY_PATH = (
        Path(__file__)
        .parents[3]
        / "resources"
        / "work_registry.json"
    )

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(
        self,
        registry_path: Path | None = None,
    ) -> None:

        self._registry_path = (
            registry_path
            if registry_path is not None
            else self.DEFAULT_REGISTRY_PATH
        )

    # ---------------------------------------------------------
    # Registry Loading
    # ---------------------------------------------------------

    @lru_cache(maxsize=1)
    def load(
        self,
    ) -> tuple[WorkDefinition, ...]:
        """
        Load and cache the registry.

        Returns
        -------
        tuple[WorkDefinition, ...]
        """

        if not self._registry_path.exists():

            raise FileNotFoundError(
                f"Registry not found: {self._registry_path}"
            )

        with self._registry_path.open(
            "r",
            encoding="utf-8",
        ) as fp:

            data = json.load(fp)

        self._validate_registry(data)

        works: list[WorkDefinition] = []

        for item in data["works"]:

            works.append(
                WorkDefinition.from_dict(item)
            )

        return tuple(works)

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    @staticmethod
    def _validate_registry(
        data: dict,
    ) -> None:
        """
        Performs lightweight validation of the registry.
        """

        if not isinstance(data, dict):

            raise TypeError(
                "Registry root must be a JSON object."
            )

        if "works" not in data:

            raise ValueError(
                "Registry missing 'works' collection."
            )

        if not isinstance(data["works"], list):

            raise TypeError(
                "'works' must be a list."
            )

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def find_work(
        self,
        text: str,
    ) -> WorkDefinition | None:
        """
        Finds the first matching work.
        """

        for work in self.load():

            if work.matches(text):

                return work

        return None

    # ---------------------------------------------------------

    def get(
        self,
        identifier: str,
    ) -> WorkDefinition | None:
        """
        Retrieve a work by identifier.
        """

        identifier = identifier.lower()

        for work in self.load():

            if work.identifier.lower() == identifier:

                return work

        return None

    # ---------------------------------------------------------

    def exists(
        self,
        identifier: str,
    ) -> bool:

        return self.get(identifier) is not None

    # ---------------------------------------------------------

    def identifiers(
        self,
    ) -> tuple[str, ...]:

        return tuple(

            work.identifier

            for work in self.load()

        )

    # ---------------------------------------------------------

    def titles(
        self,
    ) -> tuple[str, ...]:

        return tuple(

            work.title

            for work in self.load()

        )

    # ---------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> list[WorkDefinition]:
        """
        Searches identifiers, titles and aliases.
        """

        query = query.lower()

        results: list[WorkDefinition] = []

        for work in self.load():

            if query in work.identifier.lower():

                results.append(work)

                continue

            if query in work.title.lower():

                results.append(work)

                continue

            if work.matches(query):

                results.append(work)

        return results

    # ---------------------------------------------------------

    def corpus_types(
        self,
    ) -> tuple[str, ...]:

        corpus_types = {

            work.corpus_type

            for work in self.load()

            if work.corpus_type is not None

        }

        return tuple(sorted(corpus_types))

    # ---------------------------------------------------------

    def works_by_corpus_type(
        self,
        corpus_type: str,
    ) -> list[WorkDefinition]:

        corpus_type = corpus_type.lower()

        return [

            work

            for work in self.load()

            if work.corpus_type
            and work.corpus_type.lower() == corpus_type

        ]

    # ---------------------------------------------------------

    def authors(
        self,
    ) -> tuple[str, ...]:

        authors = {

            work.author

            for work in self.load()

            if work.author

        }

        return tuple(sorted(authors))

    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[WorkDefinition]:

        return iter(self.load())

    # ---------------------------------------------------------

    def __contains__(
        self,
        identifier: str,
    ) -> bool:

        return self.exists(identifier)

    # ---------------------------------------------------------

    def __getitem__(
        self,
        identifier: str,
    ) -> WorkDefinition:

        work = self.get(identifier)

        if work is None:

            raise KeyError(identifier)

        return work

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self.load())

    # ---------------------------------------------------------

    @property
    def registry_path(
        self,
    ) -> Path:

        return self._registry_path

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"works={len(self)}, "
            f"path='{self._registry_path.name}')"
        )
