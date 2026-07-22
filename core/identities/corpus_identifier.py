from __future__ import annotations

"""
SanskritAI
==========

Corpus Identifier

Immutable identifier for textual corpus resources.

A CorpusIdentifier identifies any resource contained within a
textual corpus. It intentionally remains corpus-agnostic so
that it can represent Purāṇas, Vedas, Upaniṣads, Itihāsas,
Śāstras, or future corpus types.

Examples
--------
CORPUS:BRAHMAPURANA:001:066:002

CORPUS:RIGVEDA:001:001:003

CORPUS:BHAGAVADGITA:002:047

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.identities.resource_identifier import (
    ResourceIdentifier,
)


@dataclass(slots=True, frozen=True)
class CorpusIdentifier(ResourceIdentifier):
    """
    Identifier for corpus resources.
    """

    DEFAULT_NAMESPACE: str = "CORPUS"

    def __post_init__(self) -> None:
        """
        Apply the default corpus namespace.
        """
        if not self.namespace:
            object.__setattr__(
                self,
                "namespace",
                self.DEFAULT_NAMESPACE,
            )

        super().__post_init__()

    # ---------------------------------------------------------
    # Corpus Semantics
    # ---------------------------------------------------------

    @property
    def corpus_name(self) -> str:
        """
        Top-level corpus name.

        Example
        -------
        BRAHMAPURANA

        RIGVEDA

        BHAGAVADGITA
        """
        return self.resource_path[0]

    @property
    def corpus_path(self) -> tuple[str, ...]:
        """
        Complete corpus hierarchy excluding the namespace.
        """
        return self.resource_path

    @property
    def location(self) -> tuple[str, ...]:
        """
        Returns the location within the corpus.

        Example
        -------
        CORPUS:BRAHMAPURANA:001:066:002

        location ->
            ("001", "066", "002")
        """
        if self.resource_depth <= 1:
            return ()

        return self.resource_path[1:]

    @property
    def location_depth(self) -> int:
        """
        Number of hierarchical levels beneath the corpus root.
        """
        return len(self.location)

    @property
    def root_resource(self) -> str:
        """
        Returns the corpus root resource.
        """
        return self.corpus_name

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"corpus={self.corpus_name!r}, "
            f"path={self.corpus_path!r})"
        )
