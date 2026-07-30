from __future__ import annotations

"""
SanskritAI
==========

Dhatu Gana

Defines the canonical immutable foundation for Sanskrit धातु
गणाः (verbal root classes).

A DhatuGana represents one classical gana such as:
- भ्वादि
- अदादि
- जुहोत्यादि
- दिवादि
- स्वादि
- तुदादि
- रुधादि
- तनादि
- क्र्यादि
- चुरादि

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class DhatuGana(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable Dhatu gana.
    """

    identifier: str

    sanskrit_name: str

    english_name: str

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.sanskrit_name

    @property
    def display_text(self) -> str:
        if self.english_name:
            return f"{self.sanskrit_name} ({self.english_name})"
        return self.sanskrit_name

    @property
    def display_description(self) -> str:
        return self.description

    def __str__(self) -> str:
        return self.display_text


BVADI = DhatuGana(
    identifier="bhuvadi",
    sanskrit_name="भ्वादि",
    english_name="Beginning with भू",
    description="First major Sanskrit verbal root class.",
)

ADADI = DhatuGana(
    identifier="adadi",
    sanskrit_name="अदादि",
    english_name="Beginning with अद्",
    description="Second major Sanskrit verbal root class.",
)

JUHOTYADI = DhatuGana(
    identifier="juhotyadi",
    sanskrit_name="जुहोत्यादि",
    english_name="Beginning with जुहोति",
    description="Third major Sanskrit verbal root class.",
)

DIVADI = DhatuGana(
    identifier="divadi",
    sanskrit_name="दिवादि",
    english_name="Beginning with दिव्",
    description="Fourth major Sanskrit verbal root class.",
)

SVADI = DhatuGana(
    identifier="svadi",
    sanskrit_name="स्वादि",
    english_name="Beginning with स्वाद्",
    description="Fifth major Sanskrit verbal root class.",
)

TUDADI = DhatuGana(
    identifier="tudadi",
    sanskrit_name="तुदादि",
    english_name="Beginning with तुद्",
    description="Sixth major Sanskrit verbal root class.",
)

RUDHADI = DhatuGana(
    identifier="rudhadi",
    sanskrit_name="रुधादि",
    english_name="Beginning with रुध्",
    description="Seventh major Sanskrit verbal root class.",
)

TANADI = DhatuGana(
    identifier="tanadi",
    sanskrit_name="तनादि",
    english_name="Beginning with तन्",
    description="Eighth major Sanskrit verbal root class.",
)

KRYADI = DhatuGana(
    identifier="kryadi",
    sanskrit_name="क्र्यादि",
    english_name="Beginning with कृ",
    description="Ninth major Sanskrit verbal root class.",
)

CURADI = DhatuGana(
    identifier="curadi",
    sanskrit_name="चुरादि",
    english_name="Beginning with चुर्",
    description="Tenth major Sanskrit verbal root class.",
)
