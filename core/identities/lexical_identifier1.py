from __future__ import annotations

"""
SanskritAI
==========

Lexical Identifier

Provides an immutable identifier for lexical objects within the
SanskritAI architecture.

Lexical identifiers are built upon the NamespacedIdentifier
infrastructure and default to the "LEX" namespace.

Examples
--------
LEX:राम

LEX:गम्

LEX:देव.001

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.identities.namespaced_identifier import (
    NamespacedIdentifier,
)


@dataclass(slots=True, frozen=True)
class LexicalIdentifier(NamespacedIdentifier):
    """
    Immutable identifier for lexical objects.
    """

    DEFAULT_NAMESPACE: str = "LEX"

    def __post_init__(self) -> None:
        """
        Ensure the lexical namespace is applied.
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
    ) -> "LexicalIdentifier":
        """
        Construct a lexical identifier from hierarchical
        components.

        Example
        -------
        LexicalIdentifier.from_components("राम")

        LexicalIdentifier.from_components(
            "देव",
            "001",
        )
        """
        return cls(
            value="",
            namespace=cls.DEFAULT_NAMESPACE,
            local_parts=tuple(components),
        )

    @classmethod
    def from_lemma(
        cls,
        lemma: str,
    ) -> "LexicalIdentifier":
        """
        Construct a lexical identifier directly from a lemma.
        """
        return cls.from_components(lemma)

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def lemma(self) -> str:
        """
        Returns the primary lexical component.
        """
        return self.local_parts[0]

    @property
    def hierarchy(self) -> tuple[str, ...]:
        """
        Returns the lexical hierarchy excluding the namespace.
        """
        return self.local_parts

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"namespace={self.namespace!r}, "
            f"lemma={self.lemma!r})"
        )
