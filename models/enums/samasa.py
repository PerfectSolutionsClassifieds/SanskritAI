"""
Sanskrit Samāsa Types

Traditional classification based on
Pāṇinian grammar.
"""

from enum import Enum


class Samasa(Enum):
    """
    Major Sanskrit compound types.
    """

    UNKNOWN = "unknown"

    # -----------------------------------------
    # Main Types
    # -----------------------------------------

    AVYAYIBHAVA = "avyayibhava"

    TATPURUSHA = "tatpurusha"

    KARMADHARAYA = "karmadharaya"

    DVIGU = "dvigu"

    DVANDVA = "dvandva"

    BAHUVRIHI = "bahuvrihi"

    # -----------------------------------------
    # Tatpurusha Subtypes
    # -----------------------------------------

    PRATHAMA_TATPURUSHA = "prathama_tatpurusha"

    DVITIYA_TATPURUSHA = "dvitiya_tatpurusha"

    TRITIYA_TATPURUSHA = "tritiya_tatpurusha"

    CHATURTHI_TATPURUSHA = "chaturthi_tatpurusha"

    PANCHAMI_TATPURUSHA = "panchami_tatpurusha"

    SHASHTHI_TATPURUSHA = "shashthi_tatpurusha"

    SAPTAMI_TATPURUSHA = "saptami_tatpurusha"

    NAN_TATPURUSHA = "nan_tatpurusha"

    UPAPADA_TATPURUSHA = "upapada_tatpurusha"

    ALUK_TATPURUSHA = "aluk_tatpurusha"

    # -----------------------------------------
    # Miscellaneous
    # -----------------------------------------

    EKASESHA = "ekasesha"

    NONE = "none"
