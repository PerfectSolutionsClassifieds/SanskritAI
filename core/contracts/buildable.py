from __future__ import annotations

"""
SanskritAI
==========

Buildable Contract

Defines the architectural contract for objects that can be
constructed through the SanskritAI Builder framework.

This contract specifies that an object participates in a build
process but intentionally does not prescribe how construction
is performed.

Construction responsibilities belong to the Builder Kernel
rather than to the domain objects themselves.

Typical implementations include:

- Lexeme
- Synset
- DictionaryEntry
- Corpus
- Chapter
- Verse
- KnowledgeNode

Architecture
------------

Contract
      │
      ▼
Buildable

Version
-------
v0.6.0
"""

from abc import abstractmethod

from SanskritAI.core.contracts.contract import Contract


class Buildable(Contract):
    """
    Architectural contract for buildable objects.
    """

    @property
    def can_build(self) -> bool:
        """
        Indicates that this object participates in the Builder
        architecture.
        """
        return True

    @property
    @abstractmethod
    def builder_type(self) -> type | None:
        """
        Returns the preferred builder type capable of
        constructing this object.

        Returns
        -------
        type | None
            Concrete Builder class, if known.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def record_type(self) -> type | None:
        """
        Returns the canonical Record type used as input to the
        Builder.

        Returns
        -------
        type | None
            Concrete Record class, if known.
        """
        raise NotImplementedError
