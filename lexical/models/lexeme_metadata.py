from __future__ import annotations

"""
Lexeme Metadata.
"""

from dataclasses import dataclass

from SanskritAI.lexical.enums.part_of_speech import (
    PartOfSpeech,
)

from SanskritAI.lexical.models.base_lexical_metadata import (
    BaseLexicalMetadata,
)


@dataclass(slots=True)
class LexemeMetadata(
    BaseLexicalMetadata,
):
    """
    Metadata describing a lexical unit.
    """

    lemma: str = ""

    transliteration: str = ""

    part_of_speech: PartOfSpeech = (
        PartOfSpeech.UNKNOWN
    )

    root: str = ""

    frequency: int = 0
