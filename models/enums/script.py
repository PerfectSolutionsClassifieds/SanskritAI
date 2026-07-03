"""
Supported writing systems.
"""

from enum import Enum


class Script(Enum):

    UNKNOWN = "unknown"

    DEVANAGARI = "devanagari"

    TELUGU = "telugu"

    IAST = "iast"

    ITRANS = "itrans"

    HK = "harvard_kyoto"

    SLP1 = "slp1"

    WX = "wx"

    ISO15919 = "iso15919"
