from __future__ import annotations

"""
BATCH 5H-0 — AMARAKOSHA RECORD BUILDER CONTRACT VERIFICATION

Read-only audit.

Purpose
-------
Verify the existing:

    SynsetRecord
        ↓
    SynsetRecordBuilder
        ↓
    SynsetBuilder
        ↓
    Synset

and:

    VargaRecord
        ↓
    VargaBuilder / VargaRecordBuilder
        ↓
    Varga

boundaries.

This audit does not modify production code.
"""

import inspect
from pathlib import Path

from SanskritAI.amarakosha.builders.synset_builder import SynsetBuilder
from SanskritAI.amarakosha.builders.synset_record_builder import (
    SynsetRecordBuilder,
)
from SanskritAI.amarakosha.builders.varga_builder import VargaBuilder
from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.models.synset_metadata import SynsetMetadata
from SanskritAI.amarakosha.models.varga import Varga
from SanskritAI.amarakosha.models.varga_metadata import VargaMetadata
from SanskritAI.amarakosha.records.synset_record import SynsetRecord
from SanskritAI.amarakosha.records.varga_record import VargaRecord
from SanskritAI.domain.lexical.lexeme import Lexeme


ROOT = Path("/content/SanskritAI")


def section(title: str) -> None:
    print()
    print("-" * 110)
    print(title)
    print("-" * 110)


def show_signature(label: str, obj) -> None:
    print(f"{label}")
    print(f"  signature : {inspect.signature(obj)}")


def show_source(label: str, obj) -> None:
    print()
    print(f"{label}")
    print("-" * 80)

    try:
        print(inspect.getsource(obj))
    except (OSError, TypeError) as exc:
        print(f"  SOURCE ERROR: {exc}")


def source_path(obj) -> str:
    try:
        return inspect.getsourcefile(obj) or "<unknown>"
    except TypeError:
        return "<unknown>"


print("=" * 110)
print("BATCH 5H-0 — AMARAKOSHA RECORD BUILDER CONTRACT VERIFICATION")
print("=" * 110)

print(f"Repository root : {ROOT}")
print("Audit mode      : READ-ONLY")


# =====================================================================
# 1. RESOLUTION
# =====================================================================

section("1. COMPONENT RESOLUTION")

components = {
    "SynsetRecord": SynsetRecord,
    "VargaRecord": VargaRecord,
    "SynsetRecordBuilder": SynsetRecordBuilder,
    "SynsetBuilder": SynsetBuilder,
    "VargaBuilder": VargaBuilder,
    "Synset": Synset,
    "Varga": Varga,
    "SynsetMetadata": SynsetMetadata,
    "VargaMetadata": VargaMetadata,
    "Lexeme": Lexeme,
}

for name, obj in components.items():
    print(f"{name:<24}: {obj.__module__}.{obj.__name__}")
    print(f"{'':24}  source: {source_path(obj)}")


# =====================================================================
# 2. RECORD CONTRACTS
# =====================================================================

section("2. RECORD CONTRACTS")

show_signature("SynsetRecord", SynsetRecord)
print("Fields:")
for name in getattr(SynsetRecord, "__dataclass_fields__", {}):
    print(f"  - {name}")

show_signature("VargaRecord", VargaRecord)
print("Fields:")
for name in getattr(VargaRecord, "__dataclass_fields__", {}):
    print(f"  - {name}")


# =====================================================================
# 3. RECORD BUILDER CONTRACTS
# =====================================================================

section("3. RECORD BUILDER CONTRACTS")

show_signature("SynsetRecordBuilder", SynsetRecordBuilder)
print(
    "Abstract methods:",
    getattr(SynsetRecordBuilder, "__abstractmethods__", None),
)

show_source(
    "SynsetRecordBuilder.__init__",
    SynsetRecordBuilder.__init__,
)

show_source(
    "SynsetRecordBuilder.build",
    SynsetRecordBuilder.build,
)

if hasattr(SynsetRecordBuilder, "_create_instance"):
    show_source(
        "SynsetRecordBuilder._create_instance",
        SynsetRecordBuilder._create_instance,
    )


# =====================================================================
# 4. VARGA RECORD BUILDER DISCOVERY
# =====================================================================

section("4. VARGA RECORD BUILDER DISCOVERY")

varga_record_builder_module = None

try:
    from SanskritAI.amarakosha.builders.varga_record_builder import (
        VargaRecordBuilder,
    )

    varga_record_builder_module = VargaRecordBuilder

    print(
        "VargaRecordBuilder:",
        f"{VargaRecordBuilder.__module__}.{VargaRecordBuilder.__name__}",
    )
    print(
        "Abstract methods:",
        getattr(VargaRecordBuilder, "__abstractmethods__", None),
    )

    show_signature("VargaRecordBuilder", VargaRecordBuilder)

    show_source(
        "VargaRecordBuilder.__init__",
        VargaRecordBuilder.__init__,
    )

    show_source(
        "VargaRecordBuilder.build",
        VargaRecordBuilder.build,
    )

except ImportError as exc:
    print("VargaRecordBuilder: NOT FOUND")
    print(f"Import detail: {exc}")


# =====================================================================
# 5. SYNSET BUILDER CONTRACT
# =====================================================================

section("5. SYNSET BUILDER CONTRACT")

print(
    "Abstract methods:",
    getattr(SynsetBuilder, "__abstractmethods__", None),
)

show_source(
    "SynsetBuilder.__init__",
    SynsetBuilder.__init__,
)

show_source(
    "SynsetBuilder._create_instance",
    SynsetBuilder._create_instance,
)

show_source(
    "SynsetBuilder.build",
    SynsetBuilder.build,
)


# =====================================================================
# 6. VARGA BUILDER CONTRACT
# =====================================================================

section("6. VARGA BUILDER CONTRACT")

print(
    "Abstract methods:",
    getattr(VargaBuilder, "__abstractmethods__", None),
)

show_source(
    "VargaBuilder.__init__",
    VargaBuilder.__init__,
)

show_source(
    "VargaBuilder._create_instance",
    VargaBuilder._create_instance,
)

show_source(
    "VargaBuilder.build",
    VargaBuilder.build,
)


# =====================================================================
# 7. RUNTIME RECORD CONSTRUCTION
# =====================================================================

section("7. RUNTIME RECORD CONSTRUCTION")

try:
    synset_record = SynsetRecord(
        identifier="synset-record:test:1",
        source="amarakosha",
        source_identifier="amk:test:1",
        source_version="1.0",
        kanda=list(
            __import__(
                "SanskritAI.amarakosha.enums.Amarakanda",
                fromlist=["Amarakanda"],
            ).Amarakanda
        )[0],
        varga="test-varga",
        verse=1,
        sequence=1,
        devanagari="हरिः",
        iast="hariḥ",
        transliteration="hari",
        gloss="Vishnu",
        lexeme_ids=("lexeme:test:1", "lexeme:test:2"),
        tags=("test",),
        notes="Batch 5H runtime probe",
    )

    print("SynsetRecord construction : SUCCESS")
    print("Record identifier         :", synset_record.identifier)
    print("Source                    :", synset_record.source)
    print("Kanda                     :", synset_record.kanda)
    print("Varga                     :", synset_record.varga)
    print("Verse                     :", synset_record.verse)
    print("Sequence                  :", synset_record.sequence)
    print("Devanagari                :", synset_record.devanagari)
    print("IAST                      :", synset_record.iast)
    print("Transliteration           :", synset_record.transliteration)
    print("Gloss                     :", synset_record.gloss)
    print("Lexeme IDs                :", synset_record.lexeme_ids)
    print("Tags                      :", synset_record.tags)
    print("Notes                     :", synset_record.notes)

except Exception as exc:
    synset_record = None
    print("SynsetRecord construction : FAILED")
    print(type(exc).__name__, ":", exc)


try:
    from SanskritAI.amarakosha.enums.Amarakanda import Amarakanda

    varga_record = VargaRecord(
        identifier="varga-record:test:1",
        source="amarakosha",
        source_identifier="amk:varga:test:1",
        source_version="1.0",
        kanda=list(Amarakanda)[0],
        varga_number=1,
        name="test-varga",
        title="Test Varga",
        devanagari="परीक्षणवर्गः",
        iast="parīkṣaṇavargaḥ",
        transliteration="parīkṣaṇavargaḥ",
        description="Batch 5H runtime probe",
        tags=("test",),
        notes="Batch 5H runtime probe",
    )

    print()
    print("VargaRecord construction  : SUCCESS")
    print("Record identifier         :", varga_record.identifier)
    print("Source                    :", varga_record.source)
    print("Kanda                     :", varga_record.kanda)
    print("Varga number              :", varga_record.varga_number)
    print("Name                      :", varga_record.name)
    print("Title                     :", varga_record.title)
    print("Devanagari                :", varga_record.devanagari)
    print("IAST                      :", varga_record.iast)
    print("Transliteration           :", varga_record.transliteration)
    print("Description               :", varga_record.description)
    print("Tags                      :", varga_record.tags)
    print("Notes                     :", varga_record.notes)

except Exception as exc:
    varga_record = None
    print()
    print("VargaRecord construction  : FAILED")
    print(type(exc).__name__, ":", exc)


# =====================================================================
# 8. LEXEME FIXTURES
# =====================================================================

section("8. LEXEME FIXTURES")

lexeme_1 = Lexeme(
    identifier="lexeme:test:1",
    lemma="हरि",
    language="sanskrit",
    script="devanagari",
    transliteration="hari",
)

lexeme_2 = Lexeme(
    identifier="lexeme:test:2",
    lemma="विष्णु",
    language="sanskrit",
    script="devanagari",
    transliteration="viṣṇu",
)

print("Lexeme 1:", lexeme_1)
print("Lexeme 2:", lexeme_2)


# =====================================================================
# 9. SYNSET RECORD BUILDER RUNTIME
# =====================================================================

section("9. SYNSET RECORD BUILDER RUNTIME")

if synset_record is not None:

    try:
        builder = SynsetRecordBuilder()

        print("Builder instantiation : SUCCESS")
        print(
            "Abstract methods      :",
            getattr(SynsetRecordBuilder, "__abstractmethods__", None),
        )

        built_synset = builder.build(synset_record)

        print("Builder.build(record) : SUCCESS")
        print("Result type           :", type(built_synset).__name__)
        print("Identifier            :", built_synset.identifier)
        print("Child count           :", len(built_synset.children))

        if len(built_synset.children) > 0:
            print(
                "Child identifiers     :",
                [child.identifier for child in built_synset.children],
            )

    except Exception as exc:
        built_synset = None

        print("Builder.build(record) : FAILED")
        print(type(exc).__name__, ":", exc)

else:
    built_synset = None
    print("Skipped because SynsetRecord construction failed.")


# =====================================================================
# 10. DIRECT SYNSET BUILDER WITH RECORD DATA
# =====================================================================

section("10. SYNSET BUILDER WITH REPRESENTATIVE RECORD DATA")

try:
    synset_builder = (
        SynsetBuilder()
        .with_identifier("synset:record-mapped:1")
        .add_lexeme(lexeme_1)
        .add_lexeme(lexeme_2)
    )

    mapped_synset = synset_builder.build()

    print("Construction : SUCCESS")
    print("Identifier   :", mapped_synset.identifier)
    print("Child count  :", len(mapped_synset.children))
    print(
        "Children     :",
        [child.identifier for child in mapped_synset.children],
    )

except Exception as exc:
    mapped_synset = None
    print("Construction : FAILED")
    print(type(exc).__name__, ":", exc)


# =====================================================================
# 11. VARGA BUILDER RUNTIME
# =====================================================================

section("11. VARGA BUILDER WITH REPRESENTATIVE DATA")

if mapped_synset is not None:

    try:
        varga_builder = (
            VargaBuilder()
            .with_identifier("varga:test:1")
            .add_synset(mapped_synset)
        )

        mapped_varga = varga_builder.build()

        print("Construction : SUCCESS")
        print("Identifier   :", mapped_varga.identifier)
        print("Child count  :", len(mapped_varga.children))
        print(
            "Children     :",
            [child.identifier for child in mapped_varga.children],
        )

    except Exception as exc:
        mapped_varga = None
        print("Construction : FAILED")
        print(type(exc).__name__, ":", exc)

else:
    mapped_varga = None
    print("Skipped because Synset construction failed.")


# =====================================================================
# 12. SOURCE-TO-BUILDER SEARCH
# =====================================================================

section("12. PRODUCTION RECORD-BUILDER REFERENCES")

patterns = (
    "SynsetRecordBuilder",
    "VargaRecordBuilder",
    ".build(record",
)

for pattern in patterns:
    print()
    print(f"SEARCH: {pattern}")

    matches = []

    for path in ROOT.rglob("*.py"):
        path_text = str(path)

        if any(
            token in path_text
            for token in (
                "__pycache__",
                "/tests/",
                "\\tests\\",
            )
        ):
            continue

        if path.name.endswith(("1.py", "2.py", "3.py")):
            continue

        if "_G" in path.stem:
            continue

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except OSError:
            continue

        if pattern in text:
            matches.append(path)

    if matches:
        for match in matches:
            print("  ", match)
    else:
        print("  NONE")


# =====================================================================
# 13. DECISION GATE
# =====================================================================

section("13. BATCH 5H-0 DECISION GATE")

record_ok = synset_record is not None
varga_record_ok = varga_record is not None

synset_builder_concrete = not bool(
    getattr(SynsetBuilder, "__abstractmethods__", None)
)

varga_builder_concrete = not bool(
    getattr(VargaBuilder, "__abstractmethods__", None)
)

synset_record_builder_concrete = not bool(
    getattr(SynsetRecordBuilder, "__abstractmethods__", None)
)

print("SynsetRecord construction       :", "PASS" if record_ok else "FAIL")
print("VargaRecord construction        :", "PASS" if varga_record_ok else "FAIL")
print(
    "SynsetBuilder concrete          :",
    "PASS" if synset_builder_concrete else "FAIL",
)
print(
    "VargaBuilder concrete           :",
    "PASS" if varga_builder_concrete else "FAIL",
)
print(
    "SynsetRecordBuilder concrete    :",
    "PASS" if synset_record_builder_concrete else "FAIL",
)

if built_synset is not None:
    print(
        "SynsetRecordBuilder runtime     : PASS"
    )
else:
    print(
        "SynsetRecordBuilder runtime     : NOT VERIFIED"
    )

if mapped_synset is not None:
    print(
        "SynsetBuilder representative    : PASS"
    )
else:
    print(
        "SynsetBuilder representative    : FAIL"
    )

if mapped_varga is not None:
    print(
        "VargaBuilder representative     : PASS"
    )
else:
    print(
        "VargaBuilder representative     : NOT VERIFIED"
    )

print()
print("IMPORTANT:")
print(
    "This audit does NOT decide the final SynsetRecord → CanonicalDictionary"
)
print(
    "mapping. It only verifies the existing RecordBuilder → Domain boundary."
)

print()
print(
    "NEXT DECISION:"
)

if built_synset is not None:
    print(
        "  Proceed to Batch 5H runtime/semantic mapping inspection."
    )
else:
    print(
        "  Repair SynsetRecordBuilder boundary before proceeding."
    )

print()
print("BATCH 5H-0 COMPLETE — READ-ONLY")
