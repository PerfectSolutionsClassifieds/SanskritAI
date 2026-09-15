
from __future__ import annotations

"""
SanskritAI
==========

Amarakośa Importer

Coordinates parsing, lexical-reference resolution, domain-object
construction, and registration for Amarakośa knowledge resources.

Architecture
------------

AmarakoshaParser
        |
        v
SynsetRecord / VargaRecord
        |
        v
AmarakoshaImporter
        |
        +--> LexicalRepository
        |       |
        |       +--> get_lexeme()
        |
        +--> SynsetRecordBuilder
        |
        +--> VargaBuilder
        |
        v
AmarakoshaRegistry

The importer is the orchestration boundary for Amarakośa records.

No separate LexemeResolver or AmarakośaOrchestrator is introduced.

Version
-------
v0.5.0
"""

from collections.abc import Iterable

from SanskritAI.amarakosha.builders.synset_record_builder import (
    SynsetRecordBuilder,
)
from SanskritAI.amarakosha.builders.varga_builder import (
    VargaBuilder,
)
from SanskritAI.amarakosha.models.synset import (
    Synset,
)
from SanskritAI.amarakosha.models.varga import (
    Varga,
)
from SanskritAI.amarakosha.parsers.amarakosha_parser import (
    AmarakoshaParser,
)
from SanskritAI.amarakosha.records.synset_record import (
    SynsetRecord,
)
from SanskritAI.amarakosha.records.varga_record import (
    VargaRecord,
)
from SanskritAI.amarakosha.registries.amarakosha_registry import (
    AmarakoshaRegistry,
)
from SanskritAI.lexical.models.lexeme import (
    Lexeme,
)
from SanskritAI.lexical.repositories.lexical_repository import (
    LexicalRepository,
)


class AmarakoshaImporter:
    """
    Orchestrates Amarakośa record-to-domain import.

    Responsibilities
    ----------------
    1. Parse the supplied source.
    2. Resolve SynsetRecord.lexeme_ids through the existing
       LexicalRepository boundary.
    3. Build Synset objects through SynsetRecordBuilder.
    4. Build Varga objects through VargaBuilder.
    5. Register constructed domain objects.

    The importer does not own lexical lookup semantics.

    It delegates lexical identity resolution to the existing
    LexicalRepository contract.
    """

    def __init__(
        self,
        parser: AmarakoshaParser,
        registry: AmarakoshaRegistry,
        lexical_repository: LexicalRepository | None = None,
    ) -> None:
        self._parser = parser
        self._registry = registry
        self._lexical_repository = lexical_repository

    # =========================================================
    # Dependencies
    # =========================================================

    @property
    def parser(self) -> AmarakoshaParser:
        """Return the configured Amarakośa parser."""
        return self._parser

    @property
    def registry(self) -> AmarakoshaRegistry:
        """Return the target Amarakośa registry."""
        return self._registry

    @property
    def lexical_repository(self) -> LexicalRepository | None:
        """Return the optional lexical repository."""
        return self._lexical_repository

    # =========================================================
    # Source Import
    # =========================================================

    def import_source(
        self,
        source: str,
    ) -> None:
        """
        Parse and import an Amarakośa source.

        Records are processed in parser order.
        """
        records = self._parser.parse(source)

        for record in records:
            self.import_record(record)

    # =========================================================
    # Record Import
    # =========================================================

    def import_record(
        self,
        record: SynsetRecord | VargaRecord,
    ) -> Synset | Varga:
        """
        Import one already-parsed Amarakośa record.

        SynsetRecord instances are resolved and converted into
        Synset objects.

        VargaRecord instances are converted into Varga objects.

        The constructed object is registered before being returned.
        """
        if isinstance(record, SynsetRecord):
            synset = self._build_synset(record)
            self._registry.add(synset)
            return synset

        if isinstance(record, VargaRecord):
            varga = self._build_varga(record)
            self._registry.add(varga)
            return varga

        raise TypeError(
            "Unsupported Amarakośa record type: "
            f"{type(record).__name__}"
        )

    # =========================================================
    # Batch Record Import
    # =========================================================

    def import_records(
        self,
        records: Iterable[SynsetRecord | VargaRecord],
    ) -> tuple[Synset | Varga, ...]:
        """
        Import multiple already-parsed Amarakośa records.

        Returns constructed objects in input order.
        """
        imported: list[Synset | Varga] = []

        for record in records:
            imported.append(
                self.import_record(record)
            )

        return tuple(imported)

    # =========================================================
    # Synset Construction
    # =========================================================

    def _build_synset(
        self,
        record: SynsetRecord,
    ) -> Synset:
        """
        Resolve lexical references and build one Synset.
        """
        lexemes = self._resolve_lexemes(record)

        builder = SynsetRecordBuilder()

        if lexemes:
            builder.with_lexemes(lexemes)

        return builder.build(record)

    # =========================================================
    # Lexeme Resolution
    # =========================================================

    def _resolve_lexemes(
        self,
        record: SynsetRecord,
    ) -> tuple[Lexeme, ...]:
        """
        Resolve SynsetRecord.lexeme_ids through the existing
        LexicalRepository.

        Resolution deliberately remains at the importer
        orchestration boundary.

        No LexemeResolver abstraction is introduced.
        """
        identifiers = tuple(record.lexeme_ids)

        if not identifiers:
            return ()

        if self._lexical_repository is None:
            raise ValueError(
                "SynsetRecord "
                f"{record.identifier!r} contains lexical references "
                "but no LexicalRepository was configured."
            )

        lexemes: list[Lexeme] = []
        missing: list[str] = []

        for identifier in identifiers:
            lexeme = self._lexical_repository.get_lexeme(
                identifier
            )

            if lexeme is None:
                missing.append(identifier)
            else:
                lexemes.append(lexeme)

        if missing:
            raise LookupError(
                "Unable to resolve lexical identifiers for "
                f"SynsetRecord {record.identifier!r}: "
                + ", ".join(
                    repr(identifier)
                    for identifier in missing
                )
            )

        return tuple(lexemes)

    # =========================================================
    # Varga Construction
    # =========================================================

    def _build_varga(
        self,
        record: VargaRecord,
    ) -> Varga:
        """
        Build one Varga from a VargaRecord.

        VargaRecord does not currently provide a Synset-reference
        collection, so this method deliberately does not invent
        Varga/Synset grouping semantics.
        """
        builder = VargaBuilder()

        builder.with_identifier(
            record.identifier
        )

        return builder.build()
