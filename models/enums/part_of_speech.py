"""
Part of Speech
"""

from enum import Enum


class PartOfSpeech(Enum):

    UNKNOWN = "unknown"

    NOUN = "noun"

    PRONOUN = "pronoun"

    VERB = "verb"

    ADJECTIVE = "adjective"

    ADVERB = "adverb"

    PARTICLE = "particle"

    INDECLINABLE = "indeclinable"

    PREFIX = "prefix"

    SUFFIX = "suffix"

    NUMERAL = "numeral"

    INTERJECTION = "interjection"
