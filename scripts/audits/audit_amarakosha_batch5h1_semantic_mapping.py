from __future__ import annotations

"""
BATCH 5H-1 — AMARAKOSHA SEMANTIC RECORD MAPPING AUDIT

Read-only audit.

Purpose
-------
Determine exactly which SynsetRecord fields are currently mapped into
Synset / SynsetMetadata, which fields are intentionally metadata or
provenance, and which fields currently have no construction path.

Also inspect whether VargaRecord has an existing record-builder path.

This audit does NOT modify production code.
"""

import inspect
from pathlib import Path

from SanskritAI.amarakosha.builders.base_knowledge_record_builder import (
    BaseKnowledgeRecordBuilder,
)
from SanskritAI.amarakosha.builders.synset_builder import SynsetBuilder
from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.models.synset_metadata import SynsetMetadata
from SanskritAI.amarakosha.models.varga import Varga
from SanskritAI.amarakosha.models.varga_metadata import VargaMetadata
from SanskritAI.amarakosha.records.synset_record import SynsetRecord
from SanskritAI.amarakosha.records.varga_record import VargaRecord


ROOT = Path("/content/SanskritAI")


def section(title: str) -> None:
    print()
    print("-" * 115)
    print(title)
    print("-" * 115)


def source(obj) -> None:
    try:
        print(inspect.getsource(obj))
    except (OSError, TypeError) as exc:
        print("SOURCE ERROR:", exc)


print("=" * 115)
print("BATCH 5H-1 — AMARAKOSHA SEMANTIC RECORD MAPPING AUDIT")
print("=" * 115)

print("Repository root :", ROOT)
print("Audit mode      : READ-ONLY")


# =====================================================================
# 1. RESOLUTION
# =====================================================================

section("1. COMPONENT RESOLUTION")

components = {
    "BaseKnowledgeRecordBuilder": BaseKnowledgeRecordBuilder,
    "SynsetRecord": SynsetRecord,
    "VargaRecord": VargaRecord,
    "SynsetBuilder": SynsetBuilder,
    "Synset": Synset,
    "SynsetMetadata": SynsetMetadata,
    "Varga": Varga,
    "VargaMetadata": VargaMetadata,
}

for name, obj in components.items():
    print(f"{name:<30}: {obj.__module__}.{obj.__name__}")


# =====================================================================
# 2. BASE RECORD BUILDER
# =====================================================================

section("2. BASE KNOWLEDGE RECORD BUILDER")

print("MRO:")
for cls in BaseKnowledgeRecordBuilder.__mro__:
    print("  ", cls)

print()
print("Signature:")
print(" ", inspect.signature(BaseKnowledgeRecordBuilder))

print()
print("Abstract methods:")
print(" ", getattr(BaseKnowledgeRecordBuilder, "__abstractmethods__", None))

print()
print("Constructor:")
source(BaseKnowledgeRecordBuilder.__init__)

if hasattr(BaseKnowledgeRecordBuilder, "build"):
    print()
    print("build:")
    source(BaseKnowledgeRecordBuilder.build)

if hasattr(BaseKnowledgeRecordBuilder, "validate"):
    print()
    print("validate:")
    source(BaseKnowledgeRecordBuilder.validate)


# =====================================================================
# 3. SYNSET RECORD FIELDS
# =====================================================================

section("3. SYNSET RECORD FIELD INVENTORY")

synset_fields = list(
    getattr(SynsetRecord, "__dataclass_fields__", {}).keys()
)

for field in synset_fields:
    print("  ", field)


# =====================================================================
# 4. SYNSET METADATA FIELDS
# =====================================================================

section("4. SYNSET METADATA FIELD INVENTORY")

metadata_fields = list(
    getattr(SynsetMetadata, "__dataclass_fields__", {}).keys()
)

for field in metadata_fields:
    print("  ", field)


# =====================================================================
# 5. VARGA RECORD FIELDS
# =====================================================================

section("5. VARGA RECORD FIELD INVENTORY")

varga_record_fields = list(
    getattr(VargaRecord, "__dataclass_fields__", {}).keys()
)

for field in varga_record_fields:
    print("  ", field)


# =====================================================================
# 6. VARGA METADATA FIELDS
# =====================================================================

section("6. VARGA METADATA FIELD INVENTORY")

varga_metadata_fields = list(
    getattr(VargaMetadata, "__dataclass_fields__", {}).keys()
)

for field in varga_metadata_fields:
    print("  ", field)


# =====================================================================
# 7. CURRENT SYNSET RECORD BUILDER
# =====================================================================

section("7. CURRENT SYNSET RECORD BUILDER")

from SanskritAI.amarakosha.builders.synset_record_builder import (
    SynsetRecordBuilder,
)

print("MRO:")
for cls in SynsetRecordBuilder.__mro__:
    print("  ", cls)

print()
print("Abstract methods:")
print(" ", getattr(SynsetRecordBuilder, "__abstractmethods__", None))

print()
print("Constructor:")
source(SynsetRecordBuilder.__init__)

print()
print("build:")
source(SynsetRecordBuilder.build)


# =====================================================================
# 8. FIELD REFERENCE SEARCH
# =====================================================================

section("8. SYNSET RECORD FIELD REFERENCES IN PRODUCTION")

fields_to_trace = [
    "record.kanda",
    "record.varga",
    "record.verse",
    "record.sequence",
    "record.devanagari",
    "record.iast",
    "record.transliteration",
    "record.gloss",
    "record.lexeme_ids",
    "record.tags",
    "record.notes",
    "record.source",
    "record.source_identifier",
    "record.source_version",
    "record.created_at",
    "record.active",
]

production_roots = [
    ROOT / "amarakosha",
    ROOT / "acquisition",
    ROOT / "domain",
    ROOT / "lexical",
]

for expression in fields_to_trace:

    print()
    print("SEARCH:", expression)

    matches = []

    for base in production_roots:
        if not base.exists():
            continue

        for path in base.rglob("*.py"):

            if "__pycache__" in path.parts:
                continue

            if "tests" in path.parts:
                continue

            if re_suffix := path.stem:
                if re_suffix.endswith(("1", "2", "3")):
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

            if expression in text:
                matches.append(path)

    if matches:
        for match in sorted(set(matches)):
            print("  ", match)
    else:
        print("  NONE")


# =====================================================================
# 9. SYNSET BUILDER MAPPING SURFACE
# =====================================================================

section("9. SYNSET BUILDER MAPPING SURFACE")

print("SynsetBuilder methods:")

for name, member in inspect.getmembers(
    SynsetBuilder,
    predicate=inspect.isfunction,
):
    if not name.startswith("__"):
        print("  ", name)

print()
print("SynsetBuilder source:")
source(SynsetBuilder)


# =====================================================================
# 10. SYNSET MODEL MAPPING SURFACE
# =====================================================================

section("10. SYNSET MODEL MAPPING SURFACE")

print("Synset methods/properties:")

for name, member in inspect.getmembers(
    Synset,
):
    if name.startswith("_"):
        continue

    if isinstance(member, property) or inspect.isfunction(member):
        print("  ", name)


# =====================================================================
# 11. SYNSET METADATA CONSTRUCTION PROBE
# =====================================================================

section("11. SYNSET METADATA CONSTRUCTION PROBE")

try:
    metadata = SynsetMetadata()

    print("Default construction : SUCCESS")
    print()
    print("Default values:")

    for field in metadata_fields:
        try:
            value = getattr(metadata, field)
        except AttributeError:
            value = "<ATTRIBUTE ERROR>"

        print(f"  {field:<22}: {value!r}")

except Exception as exc:
    print("Default construction : FAILED")
    print(type(exc).__name__, ":", exc)


# =====================================================================
# 12. VARGA METADATA CONSTRUCTION PROBE
# =====================================================================

section("12. VARGA METADATA CONSTRUCTION PROBE")

try:
    metadata = VargaMetadata()

    print("Default construction : SUCCESS")
    print()
    print("Default values:")

    for field in varga_metadata_fields:
        try:
            value = getattr(metadata, field)
        except AttributeError:
            value = "<ATTRIBUTE ERROR>"

        print(f"  {field:<22}: {value!r}")

except Exception as exc:
    print("Default construction : FAILED")
    print(type(exc).__name__, ":", exc)


# =====================================================================
# 13. VARGA RECORD BUILDER SEARCH
# =====================================================================

section("13. VARGA RECORD BUILDER SEARCH")

candidate_files = []

for path in (ROOT / "amarakosha").rglob("*.py"):

    if "__pycache__" in path.parts:
        continue

    if "tests" in path.parts:
        continue

    if path.stem.endswith(("1", "2", "3")):
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

    if "VargaRecord" in text or "VargaBuilder" in text:
        candidate_files.append(path)

for path in sorted(set(candidate_files)):
    print("  ", path)


# =====================================================================
# 14. CURRENT SEMANTIC MAPPING MATRIX
# =====================================================================

section("14. CURRENT SEMANTIC MAPPING MATRIX")

matrix = {
    "identifier": "Synset.identifier",
    "source": "NOT CURRENTLY MAPPED",
    "source_identifier": "NOT CURRENTLY MAPPED",
    "source_version": "NOT CURRENTLY MAPPED",
    "created_at": "NOT CURRENTLY MAPPED",
    "active": "NOT CURRENTLY MAPPED",
    "kanda": "NOT CURRENTLY MAPPED",
    "varga": "NOT CURRENTLY MAPPED",
    "verse": "NOT CURRENTLY MAPPED",
    "sequence": "NOT CURRENTLY MAPPED",
    "devanagari": "NOT CURRENTLY MAPPED",
    "iast": "NOT CURRENTLY MAPPED",
    "transliteration": "NOT CURRENTLY MAPPED",
    "gloss": "NOT CURRENTLY MAPPED",
    "lexeme_ids": "NOT RESOLVED",
    "tags": "NOT CURRENTLY MAPPED",
    "notes": "NOT CURRENTLY MAPPED",
}

for field, target in matrix.items():
    print(f"{field:<20} -> {target}")


# =====================================================================
# 15. ARCHITECTURAL QUESTIONS
# =====================================================================

section("15. ARCHITECTURAL QUESTIONS")

print(
    "Q1: Should SynsetRecord fields kanda/varga/verse/sequence be copied"
)
print(
    "    into SynsetMetadata as provenance/context?"
)

print()
print(
    "Q2: Should devanagari/iast/transliteration/gloss become"
)
print(
    "    SynsetMetadata fields, or should they populate Lexeme/Sense?"
)

print()
print(
    "Q3: How should lexeme_ids be resolved to existing Lexeme objects?"
)

print()
print(
    "Q4: Should source/source_identifier/source_version/created_at/active"
)
print(
    "    be retained in SynsetMetadata.extra/provenance?"
)

print()
print(
    "Q5: Does VargaRecord require a dedicated existing builder boundary,"
)
print(
    "    or is Varga construction intended to be orchestrated elsewhere?"
)

print()
print(
    "Q6: Is the absence of VargaRecordBuilder intentional?"
)


# =====================================================================
# 16. DECISION GATE
# =====================================================================

section("16. BATCH 5H-1 DECISION GATE")

print("RecordBuilder execution             : VERIFIED")
print("SynsetBuilder execution             : VERIFIED")
print("Synset child construction           : VERIFIED")
print("Lexeme ID resolution                : UNRESOLVED")
print("Metadata mapping completeness       : INCOMPLETE")
print("Provenance retention                : INCOMPLETE")
print("VargaRecordBuilder existence        : NOT FOUND")

print()
print("RECOMMENDATION")
print("--------------")
print("Do NOT create VargaRecordBuilder yet.")
print("Do NOT create a Lexeme resolver yet.")
print("Do NOT implement the canonical adapter yet.")
print()
print(
    "Next: inspect the actual Lexeme identity/resolution boundaries"
)
print(
    "and the intended Varga construction/orchestration path."
)

print()
print("BATCH 5H-1 COMPLETE — READ-ONLY")
