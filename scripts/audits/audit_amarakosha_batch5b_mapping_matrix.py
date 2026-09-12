from __future__ import annotations

"""
BATCH 5B — AMARAKOSHA → CANONICAL MAPPING MATRIX AUDIT

Purpose
-------
Finalize the field-level mapping evidence identified in Batch 5A.

This audit is READ-ONLY.

It does NOT:
- modify production code
- create canonical models
- create an Amarakośa adapter
- modify the lookup engine
- modify CanonicalDictionaryEntry
- modify CanonicalDictionarySense
- modify CanonicalLexicon
- complete the Amarakośa importer
- implement the abstract builders

Classification vocabulary
-------------------------
DIRECT
METADATA
PROVENANCE
RELATION
CONTEXT
LOSS
UNRESOLVED

Architectural gate
------------------
Batch 5B must establish the mapping matrix before Batch 5C
decides whether the existing Amarakośa builder/importer boundary
should be completed before canonical integration.
"""

from dataclasses import fields
from inspect import getsource, signature
from typing import Any


# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------

from SanskritAI.amarakosha.records.synset_record import SynsetRecord
from SanskritAI.amarakosha.records.varga_record import VargaRecord

from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.models.synset_metadata import SynsetMetadata
from SanskritAI.amarakosha.models.varga import Varga
from SanskritAI.amarakosha.models.varga_metadata import VargaMetadata

from SanskritAI.amarakosha.builders.synset_builder import SynsetBuilder
from SanskritAI.amarakosha.builders.varga_builder import VargaBuilder

from SanskritAI.amarakosha.importers.amarakosha_importer import (
    AmarakoshaImporter,
)
from SanskritAI.amarakosha.registries.amarakosha_registry import (
    AmarakoshaRegistry,
)

from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexeme_metadata import LexemeMetadata

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)


# ---------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------

WIDTH = 118


def section(title: str) -> None:
    print()
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def show_signature(label: str, obj: Any) -> None:
    print()
    print(f"[{label}]")
    try:
        print(f"signature: {signature(obj)}")
    except Exception as exc:
        print(f"signature: <ERROR: {exc}>")


def show_fields(label: str, cls: type[Any]) -> None:
    print()
    print(f"[{label} fields]")
    try:
        for field in fields(cls):
            print(
                f"  {field.name:<28} "
                f"type={field.type!r:<45} "
                f"default={field.default!r}"
            )
    except Exception as exc:
        print(f"  <ERROR: {exc}>")


def show_source(label: str, obj: Any) -> None:
    print()
    print(f"[{label} source]")
    try:
        print(getsource(obj))
    except Exception as exc:
        print(f"<SOURCE UNAVAILABLE: {exc}>")


# ---------------------------------------------------------------------
# Mapping table
# ---------------------------------------------------------------------

MAPPING_ROWS = [
    # SynsetRecord identity / provenance
    (
        "SynsetRecord.identifier",
        "CanonicalDictionaryEntry.source_record_id",
        "DIRECT",
        "Preserve original Amarakośa record identity.",
    ),
    (
        "SynsetRecord.source_identifier",
        "CanonicalDictionaryEntry.metadata",
        "PROVENANCE",
        "Preserve source-specific identity separately from canonical entry identity.",
    ),
    (
        "SynsetRecord.source",
        "CanonicalDictionaryEntry.source_name",
        "DIRECT",
        "Source identity is already represented by the canonical entry.",
    ),
    (
        "SynsetRecord.source_version",
        "CanonicalDictionaryEntry.source_version",
        "DIRECT",
        "Source version maps directly.",
    ),
    (
        "SynsetRecord.active",
        "CanonicalDictionaryEntry.metadata",
        "METADATA",
        "CanonicalDictionaryEntry has no active field; preserve status explicitly in metadata.",
    ),
    (
        "SynsetRecord.created_at",
        "CanonicalDictionaryEntry.metadata",
        "PROVENANCE",
        "Creation timestamp has no direct canonical entry field.",
    ),
    (
        "SynsetRecord.sequence",
        "CanonicalDictionaryEntry.metadata",
        "PROVENANCE",
        "Sequence is source-record structure, not a dictionary-entry property.",
    ),

    # Lexical content
    (
        "SynsetRecord.devanagari",
        "CanonicalDictionaryEntry.headword",
        "UNRESOLVED",
        "Candidate mapping; semantic role must be confirmed from real Amarakośa records.",
    ),
    (
        "SynsetRecord.iast",
        "CanonicalDictionaryEntry.transliteration",
        "CANDIDATE",
        "Likely direct transliteration mapping if field semantics are confirmed.",
    ),
    (
        "SynsetRecord.transliteration",
        "CanonicalDictionaryEntry.transliteration",
        "CANDIDATE",
        "Potentially redundant with iast; precedence must be established.",
    ),
    (
        "SynsetRecord.gloss",
        "CanonicalDictionarySense.gloss",
        "CANDIDATE",
        "Gloss belongs more naturally to a sense than to the entry.",
    ),
    (
        "SynsetRecord.lexeme_ids",
        "CanonicalDictionaryEntry / knowledge graph",
        "RELATION",
        "Represents multiple lexical members of an Amarakośa semantic grouping; no direct entry field exists.",
    ),
    (
        "SynsetRecord.tags",
        "CanonicalDictionaryEntry.metadata",
        "METADATA",
        "Preserve source tags without inventing canonical fields.",
    ),
    (
        "SynsetRecord.notes",
        "CanonicalDictionaryEntry.metadata",
        "METADATA",
        "Preserve editorial/source notes.",
    ),

    # Amarakośa hierarchy
    (
        "SynsetRecord.kanda",
        "CanonicalDictionaryEntry.metadata",
        "PROVENANCE",
        "Canonical entry should retain Amarakośa structural location.",
    ),
    (
        "SynsetRecord.varga",
        "CanonicalDictionaryEntry.metadata",
        "PROVENANCE",
        "Varga is source organization, not automatically a dictionary sense.",
    ),
    (
        "SynsetRecord.verse",
        "CanonicalDictionaryEntry.citation / metadata",
        "PROVENANCE",
        "Verse location should remain recoverable.",
    ),

    # VargaRecord
    (
        "VargaRecord.identifier",
        "Canonical metadata / context",
        "PROVENANCE",
        "Preserve source-specific Varga identity.",
    ),
    (
        "VargaRecord.source_identifier",
        "Canonical metadata / context",
        "PROVENANCE",
        "Preserve original source identity.",
    ),
    (
        "VargaRecord.source",
        "Canonical metadata / context",
        "DIRECT",
        "Source provenance.",
    ),
    (
        "VargaRecord.source_version",
        "Canonical metadata / context",
        "DIRECT",
        "Source version provenance.",
    ),
    (
        "VargaRecord.kanda",
        "Canonical metadata / context",
        "CONTEXT",
        "Structural Amarakośa hierarchy.",
    ),
    (
        "VargaRecord.varga_number",
        "Canonical metadata / context",
        "CONTEXT",
        "Structural ordering/identity.",
    ),
    (
        "VargaRecord.name",
        "CanonicalContext / metadata",
        "UNRESOLVED",
        "Candidate context label; exact CanonicalContext ownership must be confirmed.",
    ),
    (
        "VargaRecord.title",
        "CanonicalContext / metadata",
        "UNRESOLVED",
        "Candidate context title; exact canonical ownership must be confirmed.",
    ),
    (
        "VargaRecord.devanagari",
        "CanonicalContext / metadata",
        "CANDIDATE",
        "Preserve source-language label.",
    ),
    (
        "VargaRecord.iast",
        "CanonicalContext / metadata",
        "CANDIDATE",
        "Preserve transliterated label.",
    ),
    (
        "VargaRecord.transliteration",
        "CanonicalContext / metadata",
        "CANDIDATE",
        "Potentially redundant with iast.",
    ),
    (
        "VargaRecord.description",
        "CanonicalContext / metadata",
        "CONTEXT",
        "Description belongs naturally to structural context.",
    ),
    (
        "VargaRecord.tags",
        "CanonicalContext / metadata",
        "METADATA",
        "Preserve source tags.",
    ),
    (
        "VargaRecord.notes",
        "CanonicalContext / metadata",
        "METADATA",
        "Preserve editorial/source notes.",
    ),

    # Domain graph
    (
        "Synset",
        "CanonicalDictionaryEntry",
        "UNRESOLVED",
        "One-to-one semantic equivalence has not yet been established.",
    ),
    (
        "Synset.lexemes",
        "CanonicalDictionaryEntry.senses / lexical relations",
        "RELATION",
        "The synset groups Lexeme objects; this requires explicit canonical relation semantics.",
    ),
    (
        "Varga",
        "CanonicalContext / source hierarchy",
        "CONTEXT",
        "Varga is primarily an organizational context.",
    ),
    (
        "Varga.synsets",
        "CanonicalContext / relation graph",
        "RELATION",
        "Represents containment/organization, not necessarily lexical meaning.",
    ),

    # Generic Lexeme
    (
        "Lexeme.identifier",
        "Canonical lexical identity",
        "RELATION",
        "Potential canonical lexical identity, but no direct CanonicalDictionaryEntry field is dedicated to it.",
    ),
    (
        "LexemeMetadata.lemma",
        "CanonicalDictionaryEntry.lemma",
        "CANDIDATE",
        "Strong semantic candidate where the Lexeme represents a dictionary lemma.",
    ),
    (
        "LexemeMetadata.transliteration",
        "CanonicalDictionaryEntry.transliteration",
        "CANDIDATE",
        "Potential direct mapping.",
    ),
    (
        "LexemeMetadata.language",
        "CanonicalDictionaryEntry.language",
        "DIRECT",
        "Canonical language field exists.",
    ),
    (
        "LexemeMetadata.script",
        "CanonicalDictionaryEntry.script",
        "DIRECT",
        "Canonical script field exists.",
    ),
    (
        "LexemeMetadata.part_of_speech",
        "CanonicalDictionarySense.part_of_speech",
        "CANDIDATE",
        "Sense-level mapping may be appropriate, but Amarakośa source evidence is required.",
    ),
    (
        "LexemeMetadata.root",
        "CanonicalDictionarySense.dhatu",
        "CANDIDATE",
        "Only if the root is actually a Dhātu and not another lexical root representation.",
    ),
    (
        "LexemeMetadata.frequency",
        "CanonicalDictionaryEntry.metadata",
        "METADATA",
        "No direct canonical frequency field.",
    ),
    (
        "LexemeMetadata.description",
        "CanonicalDictionarySense.definition / metadata",
        "UNRESOLVED",
        "Exact semantic role must be established before mapping.",
    ),
    (
        "LexemeMetadata.aliases",
        "CanonicalDictionaryEntry.metadata",
        "METADATA",
        "No direct canonical aliases field.",
    ),
    (
        "LexemeMetadata.extra",
        "CanonicalDictionaryEntry.metadata",
        "METADATA",
        "Preserve source-specific information.",
    ),
]


# ---------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------

def main() -> None:
    section(
        "BATCH 5B — AMARAKOSHA → CANONICAL MAPPING MATRIX AUDIT"
    )

    print("Repository root : /content/SanskritAI")
    print("Audit mode      : READ-ONLY")
    print("Purpose         : finalize mapping evidence before Batch 5C")

    # -----------------------------------------------------------------
    # 1. Record contracts
    # -----------------------------------------------------------------

    section("1. SOURCE RECORD CONTRACTS")

    show_signature("SynsetRecord", SynsetRecord)
    show_fields("SynsetRecord", SynsetRecord)

    show_signature("VargaRecord", VargaRecord)
    show_fields("VargaRecord", VargaRecord)

    # -----------------------------------------------------------------
    # 2. Domain contracts
    # -----------------------------------------------------------------

    section("2. AMARAKOSHA DOMAIN CONTRACTS")

    show_signature("Synset", Synset)
    show_signature("Varga", Varga)

    show_fields("SynsetMetadata", SynsetMetadata)
    show_fields("VargaMetadata", VargaMetadata)

    # -----------------------------------------------------------------
    # 3. Generic lexical boundary
    # -----------------------------------------------------------------

    section("3. GENERIC LEXEME CONTRACT")

    show_signature("Lexeme", Lexeme)
    show_signature("LexemeMetadata", LexemeMetadata)
    show_fields("LexemeMetadata", LexemeMetadata)

    # -----------------------------------------------------------------
    # 4. Canonical dictionary boundary
    # -----------------------------------------------------------------

    section("4. CANONICAL DICTIONARY CONTRACTS")

    show_signature(
        "CanonicalDictionaryEntry",
        CanonicalDictionaryEntry,
    )
    show_fields(
        "CanonicalDictionaryEntry",
        CanonicalDictionaryEntry,
    )

    show_signature(
        "CanonicalDictionarySense",
        CanonicalDictionarySense,
    )
    show_fields(
        "CanonicalDictionarySense",
        CanonicalDictionarySense,
    )

    show_signature(
        "CanonicalLexicon",
        CanonicalLexicon,
    )
    show_fields(
        "CanonicalLexicon",
        CanonicalLexicon,
    )

    # -----------------------------------------------------------------
    # 5. Builder/importer status
    # -----------------------------------------------------------------

    section("5. BUILDER / IMPORTER STATUS")

    show_signature("SynsetBuilder", SynsetBuilder)
    show_source("SynsetBuilder", SynsetBuilder)

    print()
    print(
        "SynsetBuilder abstract:",
        bool(getattr(SynsetBuilder, "__abstractmethods__", False)),
    )
    print(
        "SynsetBuilder abstract methods:",
        sorted(getattr(SynsetBuilder, "__abstractmethods__", set())),
    )

    show_signature("VargaBuilder", VargaBuilder)
    show_source("VargaBuilder", VargaBuilder)

    print()
    print(
        "VargaBuilder abstract:",
        bool(getattr(VargaBuilder, "__abstractmethods__", False)),
    )
    print(
        "VargaBuilder abstract methods:",
        sorted(getattr(VargaBuilder, "__abstractmethods__", set())),
    )

    show_signature("AmarakoshaImporter", AmarakoshaImporter)
    show_source(
        "AmarakoshaImporter.import_source",
        AmarakoshaImporter.import_source,
    )

    show_signature("AmarakoshaRegistry", AmarakoshaRegistry)

    # -----------------------------------------------------------------
    # 6. Final mapping matrix
    # -----------------------------------------------------------------

    section("6. FINAL FIELD-LEVEL MAPPING MATRIX")

    header = (
        f"{'SOURCE FIELD':<40} | "
        f"{'CANONICAL TARGET':<39} | "
        f"{'STATUS':<12} | "
        f"RATIONALE"
    )

    print(header)
    print("-" * len(header))

    for source, target, status, rationale in MAPPING_ROWS:
        print(
            f"{source:<40} | "
            f"{target:<39} | "
            f"{status:<12} | "
            f"{rationale}"
        )

    # -----------------------------------------------------------------
    # 7. Status summary
    # -----------------------------------------------------------------

    section("7. MAPPING STATUS SUMMARY")

    counts: dict[str, int] = {}

    for _, _, status, _ in MAPPING_ROWS:
        counts[status] = counts.get(status, 0) + 1

    for status in (
        "DIRECT",
        "CANDIDATE",
        "METADATA",
        "PROVENANCE",
        "CONTEXT",
        "RELATION",
        "LOSS",
        "UNRESOLVED",
    ):
        print(f"{status:<14}: {counts.get(status, 0)}")

    # -----------------------------------------------------------------
    # 8. Critical unresolved questions
    # -----------------------------------------------------------------

    section("8. CRITICAL UNRESOLVED SEMANTIC QUESTIONS")

    questions = [
        (
            "Q1",
            "Does one Amarakośa Synset represent one canonical "
            "dictionary entry, or a semantic relation/grouping "
            "containing multiple lexical entries?"
        ),
        (
            "Q2",
            "What exactly does SynsetRecord.devanagari represent "
            "when the record contains multiple lexeme_ids?"
        ),
        (
            "Q3",
            "Should lexeme_ids become canonical lexical relations "
            "rather than metadata?"
        ),
        (
            "Q4",
            "Should Varga become CanonicalContext, source hierarchy, "
            "or remain Amarakośa-specific structural metadata?"
        ),
        (
            "Q5",
            "When both iast and transliteration are present, which "
            "field has canonical precedence?"
        ),
        (
            "Q6",
            "Does LexemeMetadata.root represent a Dhātu in the "
            "Amarakośa path, or only a generic lexical root?"
        ),
        (
            "Q7",
            "Can gloss be promoted directly to a canonical sense, "
            "or does the source require additional semantic evidence?"
        ),
    ]

    for number, question in questions:
        print(f"{number}: {question}")

    # -----------------------------------------------------------------
    # 9. Information-loss gate
    # -----------------------------------------------------------------

    section("9. INFORMATION-LOSS GATE")

    loss_candidates = [
        "SynsetRecord.sequence",
        "SynsetRecord.active",
        "SynsetRecord.created_at",
        "SynsetRecord.tags",
        "SynsetRecord.notes",
        "VargaRecord.tags",
        "VargaRecord.notes",
        "LexemeMetadata.frequency",
        "LexemeMetadata.aliases",
        "LexemeMetadata.extra",
    ]

    print(
        "The following fields have no dedicated canonical field "
        "identified by this audit:"
    )

    for item in loss_candidates:
        print(f"  - {item}")

    print()
    print(
        "RULE: absence of a direct canonical field is NOT permission "
        "to discard the information."
    )
    print(
        "Such information must remain available through canonical "
        "metadata/provenance unless a later design explicitly "
        "promotes it into a first-class relation or context."
    )

    # -----------------------------------------------------------------
    # 10. Adapter gate
    # -----------------------------------------------------------------

    section("10. BATCH 5B ARCHITECTURAL GATE")

    print("ADAPTER IMPLEMENTATION: BLOCKED")
    print()
    print("Reason:")
    print("  1. Synset → CanonicalDictionaryEntry semantics remain unresolved.")
    print("  2. Synset.lexeme_ids require relation-level design.")
    print("  3. Varga ownership as canonical context remains unresolved.")
    print("  4. SynsetBuilder remains abstract.")
    print("  5. VargaBuilder remains abstract.")
    print("  6. AmarakoshaImporter does not construct/register domain objects.")
    print()
    print("NEXT:")
    print("  Batch 5C — Builder / Importer Boundary Audit")
    print()
    print(
        "Batch 5C must determine whether the existing Amarakośa "
        "record → domain graph boundary should be completed before "
        "canonical integration."
    )

    section("BATCH 5B COMPLETE")


if __name__ == "__main__":
    main()
