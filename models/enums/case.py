"""
Sanskrit Vibhakti (Case)
"""

from enum import Enum


class Case(Enum):

    UNKNOWN = "unknown"

    PRATHAMA = "nominative"

    DVITIYA = "accusative"

    TRITIYA = "instrumental"

    CHATURTHI = "dative"

    PANCHAMI = "ablative"

    SHASHTHI = "genitive"

    SAPTAMI = "locative"

    SAMBODHANA = "vocative"
