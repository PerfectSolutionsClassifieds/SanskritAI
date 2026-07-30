from __future__ import annotations

"""
SanskritAI
==========

Dhatu Specification

Defines the declarative specification used to construct
canonical Sanskrit Dhatu objects.

This module plays the same architectural role that
phoneme_specification.py plays for the Phonology Kernel.

The specification intentionally contains data only.

No business logic belongs here.

Hierarchy
---------

DhatuSpecification
        │
        ▼
DhatuFactory
        │
        ▼
DhatuCollection
        │
        ▼
DhatuRepository

Future
------

Eventually the complete Dhātupāṭha (~2000 roots) can be
represented entirely by immutable specifications.

Version
-------
v1.0.0
"""

from typing import NamedTuple

from SanskritAI.domain.dhatu.dhatu_gana import (
    DhatuGana,
    BVADI,
)


class DhatuSpecification(
    NamedTuple):
    """
    Declarative specification for constructing one Dhatu.
    """

    identifier: str

    root: str

    transliteration: str

    meaning: str

    gana: DhatuGana

    class_number: int

    notes: str = ""


# ---------------------------------------------------------
# Bootstrap Canonical Specification
# ---------------------------------------------------------

CANONICAL_DHATU_SPECIFICATION: tuple[
    DhatuSpecification,
    ...
] = (

    DhatuSpecification(
        identifier="dhatu.bhu",
        root="भू",
        transliteration="bhū",
        meaning="to be",
        gana=BVADI,
        class_number=1,
    ),

    DhatuSpecification(
        identifier="dhatu.gam",
        root="गम्",
        transliteration="gam",
        meaning="to go",
        gana=BVADI,
        class_number=1,
    ),

    DhatuSpecification(
        identifier="dhatu.kri",
        root="कृ",
        transliteration="kṛ",
        meaning="to do",
        gana=BVADI,
        class_number=1,
    ),

    DhatuSpecification(
        identifier="dhatu.drsh",
        root="दृश्",
        transliteration="dṛś",
        meaning="to see",
        gana=BVADI,
        class_number=1,
    ),

)
