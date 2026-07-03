"""
Processing status enumeration.
"""

from enum import Enum


class Status(Enum):

    CREATED = "created"

    NORMALIZED = "normalized"

    TOKENIZED = "tokenized"

    PADACCHEDA = "padaccheda"

    MORPHOLOGY = "morphology"

    GRAMMAR = "grammar"

    DICTIONARY = "dictionary"

    TRANSLATED = "translated"

    ANALYZED = "analyzed"

    COMPLETE = "complete"

    ERROR = "error"
