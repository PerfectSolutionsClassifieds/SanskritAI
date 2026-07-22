from __future__ import annotations

"""
SanskritAI
==========

Amarakosha Parser

Concrete parser for Amarakośa sources.

Responsibilities
----------------
* Parse Amarakośa text sources.
* Detect Kāṇḍa, Varga and Synset boundaries.
* Produce immutable parser records.
* Perform no validation.
* Construct no domain objects.

Pipeline
--------

Raw Source
      │
      ▼
AmarakoshaParser
      │
      ├──────────────► VargaRecord
      │
      └──────────────► SynsetRecord

Version
-------
v0.6.0
"""

from collections.abc import Iterable

from SanskritAI.amarakosha.parsers.base_knowledge_parser import (
    BaseKnowledgeParser,
)

from SanskritAI.amarakosha.records.synset_record import (
    SynsetRecord,
)

from SanskritAI.amarakosha.records.varga_record import (
    VargaRecord,
)


class AmarakoshaParser(BaseKnowledgeParser):
    """
    Concrete parser for Amarakośa.
    """

    @property
    def knowledge_source(self) -> str:
        return "amarakosha"

    # ---------------------------------------------------------
    # Single-source parsing
    # ---------------------------------------------------------

    def parse(
        self,
        source: object,
    ) -> Iterable[SynsetRecord | VargaRecord]:
        """
        Parse a single Amarakośa source.

        Current implementation intentionally acts as a thin
        orchestration layer.

        Parsing rules will be progressively introduced during
        the parser milestone.
        """

        raise NotImplementedError(
            "Amarakosha parsing rules "
            "will be implemented incrementally."
        )

    # ---------------------------------------------------------
    # Internal parsing hooks
    # ---------------------------------------------------------

    def parse_kanda(
        self,
        lines: Iterable[str],
    ):
        """
        Parse a Kāṇḍa.

        Future implementation.
        """
        raise NotImplementedError

    def parse_varga(
        self,
        lines: Iterable[str],
    ):
        """
        Parse a Varga.

        Future implementation.
        """
        raise NotImplementedError

    def parse_synset(
        self,
        line: str,
    ):
        """
        Parse one Synset.

        Future implementation.
        """
        raise NotImplementedError
