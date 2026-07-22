from __future__ import annotations

"""
SanskritAI
==========

Corpus Identifier

Provides an immutable identifier for textual corpus objects.

Corpus identifiers uniquely identify locations within textual
corpora such as the Purāṇas, Vedas, Upaniṣads, Mahābhārata,
Rāmāyaṇa, etc.

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

from SanskritAI.core.identities.namespaced_identifier import (
    NamespacedIdentifier,
)


@dataclass(slots=True, frozen=True)
class CorpusIdentifier(NamespacedIdentifier):
    """
    Immutable identifier for corpus objects.
    """

    DEFAULT_NAMESPACE: str = "CORPUS"

    def __post_init__(self) -> None:
        """
        Apply the default namespace if omitted.
        """
        if not self.namespace:
            object.__setattr__(
                self,
                "namespace",
                self.DEFAULT_NAMESPACE,
            )

        super().__post_init__()

    # ---------------------------------------------------------
    # Factory Methods
    # ---------------------------------------------------------

    @classmethod
    def from_components(
        cls,
        *components: str,
    ) -> "CorpusIdentifier":
        """
        Construct a corpus identifier.

        Example
        -------
        CorpusIdentifier.from_components(
            "BRAHMAPURANA",
            "001",
            "066",
            "002",
        )
        """
        return cls(
            value="",
            namespace=cls.DEFAULT_NAMESPACE,
            local_parts=tuple(components),
        )

    # ---------------------------------------------------------
    # Semantic Accessors
    # ---------------------------------------------------------

    @property
    def corpus(self) -> str | None:
        """
        Corpus name.
        """
        return (
            self.local_parts[0]
            if len(self.local_parts) >= 1
            else None
        )

    @property
    def document(self) -> str | None:
        """
        Document or book identifier.
        """
        return (
            self.local_parts[1]
            if len(self.local_parts) >= 2
            else None
        )

    @property
    def chapter(self) -> str | None:
        """
        Chapter identifier.
        """
        return (
            self.local_parts[2]
            if len(self.local_parts) >= 3
            else None
        )

    @property
    def location(self) -> tuple[str, ...]:
        """
        Remaining location hierarchy after the chapter.
        """
        if len(self.local_parts) <= 3:
            return ()

        return self.local_parts[3:]

    @property
    def hierarchy(self) -> tuple[str, ...]:
        """
        Entire corpus hierarchy excluding the namespace.
        """
        return self.local_parts

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"corpus={self.corpus!r}, "
            f"hierarchy={self.local_parts!r})"
        )
