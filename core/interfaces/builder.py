from __future__ import annotations

"""
SanskritAI
==========

Builder Interface

Defines the canonical contract for all builder objects within
the SanskritAI Architectural Kernel.

A Builder incrementally constructs a domain object while
providing a fluent API.

The interface intentionally does not prescribe how objects are
constructed. Concrete implementations are free to expose
additional domain-specific methods.

Typical Implementations
-----------------------

- CorpusBuilder
- DocumentBuilder
- SectionBuilder
- VerseBuilder
- ParagraphBuilder
- LineBuilder
- TokenBuilder

Future builders:

- LexemeBuilder
- DictionaryEntryBuilder
- DhatuBuilder
- ParserBuilder

Version
-------
v0.3.0
"""

from abc import ABC, abstractmethod
from typing import Generic, Self

from SanskritAI.core.typing import T


class Builder(
    Generic[T],
    ABC,
):
    """
    Generic builder contract.
    """

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    @abstractmethod
    def reset(
        self,
    ) -> Self:
        """
        Reset the builder to a clean state.
        """
        ...

    # ---------------------------------------------------------

    @abstractmethod
    def build(
        self,
    ) -> T:
        """
        Construct and return the final object.
        """
        ...

    # ---------------------------------------------------------

    @abstractmethod
    def validate(
        self,
    ) -> None:
        """
        Validate the current state before building.
        """
        ...

    # ---------------------------------------------------------
    # Existing Object
    # ---------------------------------------------------------

    @abstractmethod
    def from_instance(
        self,
        instance: T,
    ) -> Self:
        """
        Initialize the builder from an existing object.
        """
        ...

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def instance(
        self,
    ) -> T:
        """
        Return the object currently being built.
        """
        ...
