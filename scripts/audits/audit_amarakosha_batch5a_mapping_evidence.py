from __future__ import annotations

"""
BATCH 5A — AMARAKOSHA → CANONICAL MAPPING EVIDENCE AUDIT
==========================================================

Purpose
-------
Collect runtime/source evidence required to finalize the
Amarakośa → Canonical Knowledge mapping.

This audit does NOT modify production code.

It deliberately avoids:
- creating an Amarakośa adapter
- creating canonical Amarakośa models
- changing CanonicalDictionaryEntry
- changing CanonicalDictionarySense
- changing LexicalLookupEngine
- inserting synthetic Amarakośa records
- registering synthetic objects

Historical duplicate files are ignored during repository audits.
"""

import inspect
import sys
from dataclasses import fields, is_dataclass
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = REPOSITORY_ROOT.parent

if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def heading(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def subheading(title: str) -> None:
    print()
    print("-" * 90)
    print(title)
    print("-" * 90)


def show_signature(obj: object, label: str) -> None:
    print(f"\n[{label}]")
    try:
        print("signature:", inspect.signature(obj))
    except (TypeError, ValueError):
        print("signature: <unavailable>")


def show_source(obj: object, label: str) -> None:
    print(f"\n[{label} source]")
    try:
        source = inspect.getsource(obj)
        print(source.rstrip())
    except (OSError, TypeError):
        print("<source unavailable>")


def show_dataclass_fields(cls: type, label: str) -> None:
    print(f"\n[{label} fields]")

    if not is_dataclass(cls):
        print("not a dataclass")
        return

    for field in fields(cls):
        print(
            f"  {field.name}: "
            f"{field.type!r} "
            f"default={field.default!r} "
            f"default_factory={field.default_factory!r}"
        )


def show_public_members(obj: object, label: str) -> None:
    print(f"\n[{label} public members]")

    for name in sorted(dir(obj)):
        if name.startswith("_"):
            continue

        try:
            value = getattr(obj, name)
        except Exception as exc:
            print(
                f"  {name}: "
                f"<ERROR {type(exc).__name__}: {exc}>"
            )
            continue

        if callable(value):
            print(f"  {name}()")
        else:
            print(
                f"  {name}: "
                f"{type(value).__name__}"
            )


# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------

def import_components():
    from SanskritAI.amarakosha.builders.synset_builder import (
        SynsetBuilder,
    )
    from SanskritAI.amarakosha.builders.varga_builder import (
        VargaBuilder,
    )
    from SanskritAI.amarakosha.importers.amarakosha_importer import (
        AmarakoshaImporter,
    )
    from SanskritAI.amarakosha.models.synset import Synset
    from SanskritAI.amarakosha.models.synset_metadata import (
        SynsetMetadata,
    )
    from SanskritAI.amarakosha.models.varga import Varga
    from SanskritAI.amarakosha.models.varga_metadata import (
        VargaMetadata,
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

    from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
        CanonicalDictionaryEntry,
    )
    from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
        CanonicalDictionarySense,
    )
    from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
        CanonicalLexicon,
    )

    from SanskritAI.lexical.models.lexeme import Lexeme
    from SanskritAI.lexical.models.lexeme_metadata import (
        LexemeMetadata,
    )

    return {
        "SynsetBuilder": SynsetBuilder,
        "VargaBuilder": VargaBuilder,
        "AmarakoshaImporter": AmarakoshaImporter,
        "Synset": Synset,
        "SynsetMetadata": SynsetMetadata,
        "Varga": Varga,
        "VargaMetadata": VargaMetadata,
        "AmarakoshaParser": AmarakoshaParser,
        "SynsetRecord": SynsetRecord,
        "VargaRecord": VargaRecord,
        "AmarakoshaRegistry": AmarakoshaRegistry,
        "CanonicalDictionaryEntry": CanonicalDictionaryEntry,
        "CanonicalDictionarySense": CanonicalDictionarySense,
        "CanonicalLexicon": CanonicalLexicon,
        "Lexeme": Lexeme,
        "LexemeMetadata": LexemeMetadata,
    }


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    heading(
        "BATCH 5A — AMARAKOSHA → CANONICAL MAPPING EVIDENCE AUDIT"
    )

    print(f"Repository root : {REPOSITORY_ROOT}")
    print(f"Package root    : {PACKAGE_ROOT}")
    print(f"Python          : {sys.executable}")
    print(f"Version         : {sys.version.split()[0]}")

    components = import_components()

    # -------------------------------------------------------------
    # 1. Parser
    # -------------------------------------------------------------

    heading("1. PARSER CONTRACT")

    parser_cls = components["AmarakoshaParser"]

    show_signature(
        parser_cls,
        "AmarakoshaParser",
    )

    show_source(
        parser_cls.parse,
        "AmarakoshaParser.parse",
    )

    # -------------------------------------------------------------
    # 2. Records
    # -------------------------------------------------------------

    heading("2. AMARAKOSHA RECORDS")

    for name in (
        "SynsetRecord",
        "VargaRecord",
    ):
        cls = components[name]

        show_signature(cls, name)
        show_dataclass_fields(cls, name)

    # -------------------------------------------------------------
    # 3. Builders
    # -------------------------------------------------------------

    heading("3. BUILDER IMPLEMENTATION STATUS")

    for name in (
        "SynsetBuilder",
        "VargaBuilder",
    ):
        cls = components[name]

        show_signature(cls, name)
        show_source(cls, name)

        print(
            "\nabstract:",
            bool(inspect.isabstract(cls)),
        )

        print(
            "abstract methods:",
            sorted(
                getattr(
                    cls,
                    "__abstractmethods__",
                    set(),
                )
            ),
        )

    # -------------------------------------------------------------
    # 4. Importer
    # -------------------------------------------------------------

    heading("4. IMPORTER IMPLEMENTATION STATUS")

    importer_cls = components[
        "AmarakoshaImporter"
    ]

    show_signature(
        importer_cls,
        "AmarakoshaImporter",
    )

    show_source(
        importer_cls.import_source,
        "AmarakoshaImporter.import_source",
    )

    # -------------------------------------------------------------
    # 5. Registry
    # -------------------------------------------------------------

    heading("5. REGISTRY CONTRACT")

    registry_cls = components[
        "AmarakoshaRegistry"
    ]

    show_signature(
        registry_cls,
        "AmarakoshaRegistry",
    )

    show_source(
        registry_cls.register_many,
        "AmarakoshaRegistry.register_many",
    )

    show_source(
        registry_cls.vargas,
        "AmarakoshaRegistry.vargas",
    )

    show_source(
        registry_cls.synsets,
        "AmarakoshaRegistry.synsets",
    )

    # -------------------------------------------------------------
    # 6. Amarakośa domain models
    # -------------------------------------------------------------

    heading("6. AMARAKOSHA DOMAIN MODELS")

    for name in (
        "SynsetMetadata",
        "VargaMetadata",
        "Synset",
        "Varga",
    ):
        cls = components[name]

        show_signature(cls, name)

        if is_dataclass(cls):
            show_dataclass_fields(
                cls,
                name,
            )

        show_public_members(
            cls,
            name,
        )

    # -------------------------------------------------------------
    # 7. Generic Lexeme
    # -------------------------------------------------------------

    heading("7. GENERIC LEXEME BOUNDARY")

    lexeme_cls = components["Lexeme"]
    lexeme_metadata_cls = components[
        "LexemeMetadata"
    ]

    show_signature(
        lexeme_cls,
        "Lexeme",
    )

    show_signature(
        lexeme_metadata_cls,
        "LexemeMetadata",
    )

    if is_dataclass(lexeme_metadata_cls):
        show_dataclass_fields(
            lexeme_metadata_cls,
            "LexemeMetadata",
        )

    show_source(
        lexeme_cls,
        "Lexeme",
    )

    # -------------------------------------------------------------
    # 8. Canonical Dictionary Entry
    # -------------------------------------------------------------

    heading("8. CANONICAL DICTIONARY ENTRY")

    entry_cls = components[
        "CanonicalDictionaryEntry"
    ]

    show_signature(
        entry_cls,
        "CanonicalDictionaryEntry",
    )

    show_dataclass_fields(
        entry_cls,
        "CanonicalDictionaryEntry",
    )

    # -------------------------------------------------------------
    # 9. Canonical Dictionary Sense
    # -------------------------------------------------------------

    heading("9. CANONICAL DICTIONARY SENSE")

    sense_cls = components[
        "CanonicalDictionarySense"
    ]

    show_signature(
        sense_cls,
        "CanonicalDictionarySense",
    )

    show_dataclass_fields(
        sense_cls,
        "CanonicalDictionarySense",
    )

    # -------------------------------------------------------------
    # 10. Canonical Lexicon
    # -------------------------------------------------------------

    heading("10. CANONICAL LEXICON")

    lexicon_cls = components[
        "CanonicalLexicon"
    ]

    show_signature(
        lexicon_cls,
        "CanonicalLexicon",
    )

    show_public_members(
        lexicon_cls,
        "CanonicalLexicon",
    )

    # -------------------------------------------------------------
    # 11. Preliminary mapping evidence
    # -------------------------------------------------------------

    heading(
        "11. PRELIMINARY FIELD MAPPING EVIDENCE"
    )

    mapping = [
        (
            "SynsetRecord.identifier",
            "CanonicalDictionaryEntry.source_record_id",
            "DIRECT / provenance identity",
        ),
        (
            "SynsetRecord.source",
            "CanonicalDictionaryEntry.source_name",
            "DIRECT",
        ),
        (
            "SynsetRecord.source_version",
            "CanonicalDictionaryEntry.source_version",
            "DIRECT",
        ),
        (
            "SynsetRecord.devanagari",
            "CanonicalDictionaryEntry.headword",
            "CANDIDATE — semantic confirmation required",
        ),
        (
            "SynsetRecord.iast",
            "CanonicalDictionaryEntry.transliteration",
            "CANDIDATE",
        ),
        (
            "SynsetRecord.gloss",
            "CanonicalDictionarySense.gloss",
            "CANDIDATE",
        ),
        (
            "SynsetRecord.kanda",
            "CanonicalDictionaryEntry.metadata",
            "PROVENANCE / structural metadata",
        ),
        (
            "SynsetRecord.varga",
            "CanonicalDictionaryEntry.metadata",
            "PROVENANCE / structural metadata",
        ),
        (
            "SynsetRecord.verse",
            "CanonicalDictionaryEntry.metadata",
            "PROVENANCE / citation metadata",
        ),
        (
            "SynsetRecord.lexeme_ids",
            "Lexical relations / canonical metadata",
            "NO DIRECT ENTRY FIELD — requires design decision",
        ),
        (
            "VargaRecord.kanda",
            "Canonical metadata",
            "STRUCTURAL CONTEXT",
        ),
        (
            "VargaRecord.varga_number",
            "Canonical metadata",
            "STRUCTURAL CONTEXT",
        ),
        (
            "VargaRecord.name",
            "Canonical context metadata",
            "CANDIDATE",
        ),
        (
            "VargaRecord.title",
            "Canonical context metadata",
            "CANDIDATE",
        ),
    ]

    print()

    print(
        f"{'AMARAKOSHA FIELD':45} | "
        f"{'CANONICAL TARGET':45} | "
        f"DECISION"
    )

    print("-" * 120)

    for source, target, decision in mapping:
        print(
            f"{source:45} | "
            f"{target:45} | "
            f"{decision}"
        )

    # -------------------------------------------------------------
    # 12. Architecture decision gate
    # -------------------------------------------------------------

    heading(
        "12. BATCH 5A DECISION GATE"
    )

    print(
        "DO NOT IMPLEMENT THE AMARAKOSHA ADAPTER YET."
    )

    print()
    print("Reason:")

    print(
        "  1. SynsetBuilder is currently abstract."
    )

    print(
        "  2. VargaBuilder is currently abstract."
    )

    print(
        "  3. AmarakoshaImporter currently does not "
        "complete builder/registry integration."
    )

    print(
        "  4. Therefore the current production Amarakośa "
        "pipeline does not yet produce a complete "
        "Synset/Varga runtime graph."
    )

    print(
        "  5. The canonical model should not be changed "
        "merely to accommodate this incomplete path."
    )

    print()
    print("NEXT:")
    print(
        "  Batch 5B — finalize the field-level mapping matrix."
    )
    print(
        "  Batch 5C — determine whether the existing "
        "Amarakośa builder/importer layer must first "
        "be completed."
    )

    heading("BATCH 5A COMPLETE")


if __name__ == "__main__":
    main()
