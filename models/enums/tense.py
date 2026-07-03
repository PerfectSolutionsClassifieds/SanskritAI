"""
General Sanskrit tense/aspect.
"""

from enum import Enum


class Tense(Enum):

    UNKNOWN = "unknown"

    PRESENT = "present"

    PAST = "past"

    FUTURE = "future"
