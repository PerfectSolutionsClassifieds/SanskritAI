from __future__ import annotations

"""
SanskritAI
==========

Search Term

Defines the canonical immutable search term used by the
SanskritAI Search Kernel.

A SearchTerm represents one atomic search expression.
Complex queries are composed from one or more SearchTerm
objects connected by SearchOperator values.

Typical examples include:

    dharma

    "sanātana dharma"

    agni*

    ^veda.*

Architecture
------------

ValueObject
      │
      ▼
SearchTerm
      │
      ▼
SearchQuery

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.search.search_mode import SearchMode
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(slots=True, frozen=True)
class SearchTerm(ValueObject):
    """
    Immutable atomic search term.
    """

    text: str

    mode: SearchMode = SearchMode.EXACT

    boost: float = 1.0

    negated: bool = False

    def __post_init__(self) -> None:
        text = self.text.strip()

        if not text:
            raise ValueError(
                "SearchTerm cannot be empty."
            )

        object.__setattr__(self, "text", text)

        if self.boost <= 0:
            raise ValueError(
                "SearchTerm boost must be greater than zero."
            )

    @property
    def is_phrase(self) -> bool:
        """
        Returns True if the term is enclosed in quotation marks.
        """
        return (
            len(self.text) >= 2
            and self.text.startswith('"')
            and self.text.endswith('"')
        )

    @property
    def is_negated(self) -> bool:
        """
        Indicates whether this term is negated.
        """
        return self.negated

    @property
    def is_boosted(self) -> bool:
        """
        Returns True if the term has a custom boost factor.
        """
        return self.boost != 1.0

    @property
    def normalized(self) -> str:
        """
        Returns a normalized representation suitable for
        comparison.
        """
        return self.text.casefold()

    def __str__(self) -> str:
        prefix = "-" if self.negated else ""
        return f"{prefix}{self.text}"
