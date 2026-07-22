from __future__ import annotations

"""
SanskritAI
==========

Identifier

Defines the canonical immutable identifier shared throughout the
SanskritAI architecture.

An Identifier represents the identity of a domain object. It is
format-independent and serves as the base class for specialized
identifier types such as UUIDIdentifier, CorpusIdentifier,
LexicalIdentifier, and KnowledgeIdentifier.

Version
-------
v0.6.0
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True, order=True)
class Identifier:
    """
    Immutable base identifier.

    Concrete subclasses may impose additional validation rules.
    """

    value: str

    def __post_init__(self) -> None:
        """
        Validate and normalize the identifier.
        """
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("Identifier cannot be empty.")

        object.__setattr__(self, "value", normalized)

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_empty(self) -> bool:
        """
        Returns True if the identifier is empty.

        This should always be False because construction of an
        empty Identifier is prohibited, but the property provides
        a consistent API.
        """
        return len(self.value) == 0

    @property
    def length(self) -> int:
        """
        Length of the identifier.
        """
        return len(self.value)

    def starts_with(
        self,
        prefix: str,
    ) -> bool:
        """
        Returns True if the identifier starts with the given
        prefix.
        """
        return self.value.startswith(prefix)

    def ends_with(
        self,
        suffix: str,
    ) -> bool:
        """
        Returns True if the identifier ends with the given
        suffix.
        """
        return self.value.endswith(suffix)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(value={self.value!r})"
        )
