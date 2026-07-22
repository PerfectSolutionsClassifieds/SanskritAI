from __future__ import annotations

"""
SanskritAI
==========

Part of Speech

Defines the grammatical category of a lexical item.

Version
-------
v0.3.0
"""

from enum import Enum


class PartOfSpeech(str, Enum):
    """
    Universal lexical categories.
    """

    UNKNOWN = "unknown"

    NOUN = "noun"

    PRONOUN = "pronoun"

    ADJECTIVE = "adjective"

    VERB = "verb"

    ADVERB = "adverb"

    PARTICLE = "particle"

    PREPOSITION = "preposition"

    POSTPOSITION = "postposition"

    CONJUNCTION = "conjunction"

    INTERJECTION = "interjection"

    PREFIX = "prefix"

    SUFFIX = "suffix"

    NUMERAL = "numeral"

    SYMBOL = "symbol"

    PUNCTUATION = "punctuation"
