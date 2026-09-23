from __future__ import annotations

"""
SanskritAI
==========

Synset Record Builder

Concrete adapter converting immutable SynsetRecord objects
into Synset domain objects.

Pipeline
--------

SynsetRecord
      ↓
SynsetValidator
      ↓
SynsetRecordBuilder
      ↓
SynsetBuilder
      ↓
Synset

Version
-------
v0.4.0
"""

from SanskritAI.amarakosha.builders.base_knowledge_record_builder import (
    BaseKnowledgeRecordBuilder,
)
from SanskritAI.amarakosha.builders.synset_builder import (
    SynsetBuilder,
)
from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.validators.synset_validator import (
    SynsetValidator,
)
from SanskritAI.core.records.knowledge_record import (
    KnowledgeRecord,
)


class SynsetRecordBuilder(
    BaseKnowledgeRecordBuilder[Synset],
):
    """
    Adapter converting knowledge records into Synset objects.
    """

    def __init__(self) -> None:
        super().__init__(
            validator=SynsetValidator(),
        )

    @property
    def record_type(self) -> type[KnowledgeRecord]:
        return KnowledgeRecord

    def build(
        self,
        record: KnowledgeRecord,
    ) -> Synset:
        """
        Convert a validated knowledge record into a Synset.
        """

        builder = SynsetBuilder()

        builder \
            .with_identifier(record.identifier)

        #
        # Additional Synset-specific mappings will naturally be
        # added as SynsetRecord evolves.
        #

        return builder.build()
