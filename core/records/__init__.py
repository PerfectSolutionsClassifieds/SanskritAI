"""
SanskritAI
==========

Core Records

Immutable transfer objects shared across the entire
SanskritAI platform.

These objects form the canonical interchange layer between
parsers, builders, repositories, importers, exporters,
machine-learning pipelines and external integrations.

Version
-------
v0.4.0
"""

from SanskritAI.core.records.data_record import (
    DataRecord,
)

from SanskritAI.core.records.corpus_record import (
    CorpusRecord,
)

from SanskritAI.core.records.lexical_record import (
    LexicalRecord,
)

from SanskritAI.core.records.knowledge_record import (
    KnowledgeRecord,
)

__all__ = [
    "DataRecord",
    "CorpusRecord",
    "LexicalRecord",
    "KnowledgeRecord",
]
