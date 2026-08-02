from __future__ import annotations

"""
SanskritAI

Monier–Williams Transformer
"""

from dataclasses import dataclass
from typing import Iterable

from SanskritAI.acquisition.knowledge.abstract_lexical_transformer import (
    AbstractLexicalTransformer,
)

from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_lexical_record import (
    CanonicalLexicalRecord,
)


@dataclass(slots=True)
class MonierWilliamsTransformer(
    AbstractLexicalTransformer,
):
    """
    Canonical Monier–Williams transformer.
    """

    resource_name: str = "Monier-Williams"

    resource_version: str = "unknown"

    def transform(
        self,
        entry: RawLexicalEntry,
    ) -> CanonicalLexicalRecord:

        return CanonicalLexicalRecord(

            headword=entry.headword.strip(),

            transliteration=entry.transliteration,

            language=entry.language,

            script=entry.script,

            definition=entry.raw_text.strip(),

            entry_type=entry.entry_type,

            source_name=entry.source_name,

            source_version=entry.source_version,

            source_record_id=entry.source_record_id,

            citation=entry.citation,

            metadata=dict(
                entry.metadata,
            ),

        )
