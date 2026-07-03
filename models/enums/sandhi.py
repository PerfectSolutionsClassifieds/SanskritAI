"""
Sanskrit Sandhi Types

References:
- Pāṇini Aṣṭādhyāyī
- Siddhānta Kaumudī
- Traditional Sanskrit Grammar
"""

from enum import Enum


class Sandhi(Enum):
    """
    Major Sandhi classifications.
    """

    UNKNOWN = "unknown"

    # -----------------------------------------
    # Swaras (Vowel Sandhi)
    # -----------------------------------------

    SAVARNA_DIRGHA = "savarna_dirgha"

    GUNA = "guna"

    VRDDHI = "vrddhi"

    YAN = "yan"

    AYADI = "ayadi"

    PURVARUPA = "purvarupa"

    PARARUPA = "pararupa"

    PRAKRITIBHAVA = "prakritibhava"

    # -----------------------------------------
    # Consonant Sandhi
    # -----------------------------------------

    VYANJANA = "vyanjana"

    JASTVA = "jastva"

    SATVA = "satva"

    ANUSVARA = "anusvara"

    VISARGA = "visarga"

    # -----------------------------------------
    # Special
    # -----------------------------------------

    AVAGRAHA = "avagraha"

    OPTIONAL = "optional"

    NONE = "none"
