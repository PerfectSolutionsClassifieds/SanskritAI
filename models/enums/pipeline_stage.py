"""
SanskritAI
Pipeline Stages

Represents the current processing stage of an object.
"""

from enum import Enum


class PipelineStage(Enum):

    CREATED = "created"

    NORMALIZED = "normalized"

    TOKENIZED = "tokenized"

    PADACCHEDA = "padaccheda"

    MORPHOLOGY = "morphology"

    GRAMMAR = "grammar"

    SANDHI = "sandhi"

    SAMASA = "samasa"

    KARAKA = "karaka"

    DICTIONARY = "dictionary"

    TRANSLATION = "translation"

    COMPLETE = "complete"

    FAILED = "failed"
