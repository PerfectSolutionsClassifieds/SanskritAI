from __future__ import annotations

"""
SanskritAI
==========

Lexical Identifier

Immutable identifier for lexical resources.

Built upon the ResourceIdentifier abstraction.

Examples
--------
LEX:राम

LEX:गम्

LEX:देव:001

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.identities.resource_identifier import (
    ResourceIdentifier,
)


@dataclass(slots=True, frozen=True)
class LexicalIdentifier(ResourceIdentifier):
    """
    Identifier for lexical resources.
    """

    DEFAULT_NAMESPACE: str = "LEX"

    def __post_init__(self) -> None:
        """
        Apply the default lexical namespace.
        """
        if not self.namespace:
            object.__setattr__(
                self,
                "namespace",
                self.DEFAULT_NAMESPACE,
            )

        super().__post_init__()

    # ---------------------------------------------------------
    # Lexical Semantics
    # ---------------------------------------------------------

    @property
    def lemma(self) -> str:
        """
        Primary lexical lemma.
        """
        return self.resource_name

    @property
    def lexical_path(self) -> tuple[str, ...]:
        """
        Complete lexical hierarchy.
        """
        return self.resource_path

    @property
    def sense_number(self) -> str | None:
        """
        Optional lexical sense identifier.

        Example

            LEX:देव:003
        """
        if self.resource_depth < 2:
            return None

        return self.resource_path[-1]

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"lemma={self.lemma!r})"
        )
