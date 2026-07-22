from __future__ import annotations

"""
SanskritAI
==========

Base Builder

Generic abstract builder for constructing Canonical Corpus objects.

This class provides a reusable foundation for all builders in the
SanskritAI project.

Derived Builders
----------------
* CorpusBuilder
* DocumentBuilder
* SectionBuilder
* VerseBuilder
* ParagraphBuilder
* LineBuilder
* TokenBuilder

Version
-------
v0.1.0
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseBuilder(Generic[T], ABC):
    """
    Generic abstract builder.
    """

    def __init__(self) -> None:
        self._instance: T = self._create_instance()

    # ---------------------------------------------------------
    # Abstract Factory
    # ---------------------------------------------------------

    @abstractmethod
    def _create_instance(self) -> T:
        """
        Create a fresh object.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def reset(self) -> "BaseBuilder[T]":
        """
        Reset the builder to a fresh instance.
        """

        self._instance = self._create_instance()

        return self

    # ---------------------------------------------------------

    def instance(self) -> T:
        """
        Return the current working instance.
        """

        return self._instance

    # ---------------------------------------------------------

    def build(self) -> T:
        """
        Validate and return the constructed object.

        A deep copy is returned so the builder may continue to be
        reused independently.
        """

        self.validate()

        return deepcopy(self._instance)

    # ---------------------------------------------------------

    def clone(self) -> "BaseBuilder[T]":
        """
        Return a cloned builder.
        """

        builder = self.__class__()

        builder._instance = deepcopy(self._instance)

        return builder

    # ---------------------------------------------------------

    def from_instance(
        self,
        instance: T,
    ) -> "BaseBuilder[T]":
        """
        Initialize the builder from an existing object.
        """

        self._instance = deepcopy(instance)

        return self

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(self) -> None:
        """
        Validate the current instance.

        Subclasses may override.
        """

        return

    # ---------------------------------------------------------

    @property
    def is_valid(self) -> bool:
        """
        Returns True if validation succeeds.
        """

        try:
            self.validate()
            return True
        except Exception:
            return False
