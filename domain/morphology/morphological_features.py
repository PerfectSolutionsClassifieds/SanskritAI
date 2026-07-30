from __future__ import annotations

"""
SanskritAI
==========

Morphological Features

Defines the immutable typed grammatical feature set for a
WordForm or a MorphologicalAnalysis.

This object composes the canonical grammatical categories
established in the Morphology Kernel.

It intentionally contains no parsing logic.

Relationship
------------

WordForm
    │
    ▼
MorphologicalFeatures
    │
    ▼
MorphologicalAnalysis

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.morphology.indeclinable_avyaya_category import (
    IndeclinableAvyayaCategory,
)
from SanskritAI.domain.morphology.lakara import Lakara
from SanskritAI.domain.morphology.linga import Linga
from SanskritAI.domain.morphology.pada import Pada
from SanskritAI.domain.morphology.prayoga import Prayoga
from SanskritAI.domain.morphology.purusha import Purusha
from SanskritAI.domain.morphology.vacana import Vacana
from SanskritAI.domain.morphology.vibhakti import Vibhakti


@dataclass(frozen=True, slots=True)
class MorphologicalFeatures(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable typed grammatical feature set.
    """

    vibhakti: Vibhakti | None = None

    vacana: Vacana | None = None

    linga: Linga | None = None

    purusha: Purusha | None = None

    lakara: Lakara | None = None

    pada: Pada | None = None

    prayoga: Prayoga | None = None

    avyaya: IndeclinableAvyayaCategory | None = None

    stem: str = ""

    root: str = ""

    description: str = ""

    @property
    def display_name(self) -> str:
        return "Morphological Features"

    @property
    def display_text(self) -> str:
        parts: list[str] = []

        if self.linga:
            parts.append(self.linga.display_name)

        if self.vacana:
            parts.append(self.vacana.display_name)

        if self.vibhakti:
            parts.append(self.vibhakti.display_name)

        if self.purusha:
            parts.append(self.purusha.display_name)

        if self.lakara:
            parts.append(self.lakara.display_name)

        if self.pada:
            parts.append(self.pada.display_name)

        if self.prayoga:
            parts.append(self.prayoga.display_name)

        if self.avyaya:
            parts.append(self.avyaya.display_name)

        if self.root:
            parts.append(f"root={self.root}")

        if self.stem:
            parts.append(f"stem={self.stem}")

        if parts:
            return ", ".join(parts)

        return self.display_name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def is_nominal(self) -> bool:
        return any(
            (
                self.vibhakti is not None,
                self.vacana is not None,
                self.linga is not None,
            )
        )

    @property
    def is_verbal(self) -> bool:
        return any(
            (
                self.purusha is not None,
                self.lakara is not None,
                self.pada is not None,
                self.prayoga is not None,
            )
        )

    @property
    def is_indeclinable(self) -> bool:
        return self.avyaya is not None

    @property
    def feature_count(self) -> int:
        count = 0

        if self.vibhakti is not None:
            count += 1

        if self.vacana is not None:
            count += 1

        if self.linga is not None:
            count += 1

        if self.purusha is not None:
            count += 1

        if self.lakara is not None:
            count += 1

        if self.pada is not None:
            count += 1

        if self.prayoga is not None:
            count += 1

        if self.avyaya is not None:
            count += 1

        if self.stem:
            count += 1

        if self.root:
            count += 1

        return count

    @property
    def has_features(self) -> bool:
        return self.feature_count > 0

    def __str__(self) -> str:
        return self.display_text
