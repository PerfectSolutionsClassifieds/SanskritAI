
from __future__ import annotations

"""
SanskritAI
==========

Base Registry Framework

This module defines the abstract base class for all registry-backed
resources used throughout SanskritAI.

Goals
-----
* Single implementation of JSON loading
* Registry validation
* Object construction
* In-memory caching
* Generic repository API
* Strong typing
* Storage abstraction

Future subclasses include

    WorkRegistry
    AuthorRegistry
    RepositoryRegistry
    LanguageRegistry
    ScriptRegistry
    CorpusTypeRegistry
    LexiconRegistry
    PublisherRegistry

Version
-------
v0.6.0
"""

from abc import ABC, abstractmethod
from functools import cached_property
import json
from pathlib import Path
from typing import (
    Any,
    Generic,
    Iterator,
    Sequence,
    TypeVar,
)


T = TypeVar("T")


class BaseRegistry(ABC, Generic[T]):
    """
    Abstract base class for registry-backed repositories.
    """

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(
        self,
        registry_path: Path,
    ) -> None:

        self._registry_path = registry_path

    # ---------------------------------------------------------
    # Required API
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def collection_name(self) -> str:
        """
        JSON collection name.

        Example
        -------
        "works"
        "authors"
        "languages"
        """
        ...

    # ---------------------------------------------------------

    @abstractmethod
    def create_item(
        self,
        data: dict[str, Any],
    ) -> T:
        """
        Convert a JSON dictionary into a domain object.
        """
        ...

    # ---------------------------------------------------------

    @abstractmethod
    def get_identifier(
        self,
        item: T,
    ) -> str:
        """
        Return the unique identifier of a domain object.
        """
        ...

    # ---------------------------------------------------------
    # Registry Loading
    # ---------------------------------------------------------

    @cached_property
    def items(
        self,
    ) -> tuple[T, ...]:
        """
        Loads and caches the registry.
        """

        data = self._load_json()

        self._validate_registry(data)

        return tuple(

            self.create_item(item)

            for item in data[self.collection_name]

        )

    # ---------------------------------------------------------

    def _load_json(
        self,
    ) -> dict[str, Any]:

        if not self._registry_path.exists():

            raise FileNotFoundError(

                f"Registry file not found: "
                f"{self._registry_path}"

            )

        with self._registry_path.open(
            "r",
            encoding="utf-8",
        ) as fp:

            return json.load(fp)

    # ---------------------------------------------------------

    def _validate_registry(
        self,
        data: dict[str, Any],
    ) -> None:

        if not isinstance(data, dict):

            raise TypeError(
                "Registry root must be an object."
            )

        if self.collection_name not in data:

            raise ValueError(

                f"Missing collection "
                f"'{self.collection_name}'."

            )

        collection = data[self.collection_name]

        if not isinstance(collection, list):

            raise TypeError(

                f"'{self.collection_name}' "
                f"must be a list."

            )

    # ---------------------------------------------------------
    # Repository API
    # ---------------------------------------------------------

    def get(
        self,
        identifier: str,
    ) -> T | None:

        identifier = identifier.lower()

        for item in self.items:

            if (

                self.get_identifier(item)
                .lower()

                == identifier

            ):

                return item

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

            self.get_identifier(item)

            for item in self.items

        )

    # ---------------------------------------------------------

    def all(
        self,
    ) -> Sequence[T]:

        return self.items

    # ---------------------------------------------------------

    def reload(
        self,
    ) -> None:
        """
        Clears cached registry.

        Next access reloads from disk.
        """

        self.__dict__.pop(
            "items",
            None,
        )

    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[T]:

        return iter(self.items)

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self.items)

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
    ) -> T:

        item = self.get(identifier)

        if item is None:

            raise KeyError(identifier)

        return item

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
            f"items={len(self)}, "
            f"path='{self._registry_path.name}')"
        )
