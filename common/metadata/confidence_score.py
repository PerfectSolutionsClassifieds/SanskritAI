from __future__ import annotations

"""
SanskritAI
==========

Confidence Score

Represents the confidence associated with an inferred or extracted
piece of information.

Typical Uses
------------
* Language detection
* Script detection
* Metadata extraction
* OCR confidence
* AI predictions
* Search ranking

Version
-------
v0.1.0
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConfidenceScore:
    """
    Immutable confidence score.

    Value must lie within the closed interval [0.0, 1.0].
    """

    value: float

    def __post_init__(self) -> None:

        if not (0.0 <= self.value <= 1.0):
            raise ValueError(
                "Confidence score must be between "
                "0.0 and 1.0."
            )

    @property
    def percentage(self) -> float:
        """
        Confidence expressed as a percentage.
        """
        return self.value * 100.0

    def is_high(
        self,
        threshold: float = 0.90,
    ) -> bool:

        return self.value >= threshold

    def is_low(
        self,
        threshold: float = 0.50,
    ) -> bool:

        return self.value < threshold

    def to_dict(self) -> dict:

        return {

            "value": self.value,

            "percentage": self.percentage,

        }

    def __str__(self) -> str:

        return f"{self.percentage:.2f}%"
