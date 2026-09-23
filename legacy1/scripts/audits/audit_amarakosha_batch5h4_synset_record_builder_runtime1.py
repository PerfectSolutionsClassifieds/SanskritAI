
from __future__ import annotations

import inspect

from SanskritAI.amarakosha.builders.synset_record_builder import (
    SynsetRecordBuilder,
)
from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.records.synset_record import SynsetRecord
from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexeme_metadata import LexemeMetadata


print("=" * 110)
print("BATCH 5H-4 — SYNSET RECORD BUILDER RUNTIME VERIFICATION")
print("=" * 110)


# ----------------------------------------------------------------------
# 1. Component resolution
# ----------------------------------------------------------------------

print("\n1. COMPONENT RESOLUTION")
print("-" * 110)

print("SynsetRecordBuilder :", SynsetRecordBuilder)
print("SynsetRecord        :", SynsetRecord)
print("Synset              :", Synset)
print("Lexeme              :", Lexeme)


# ----------------------------------------------------------------------
# 2. Framework inheritance
# ----------------------------------------------------------------------

print("\n2. FRAMEWORK INHERITANCE")
print("-" * 110)

print("MRO:")
for cls in inspect.getmro(SynsetRecordBuilder):
    print("  ", cls)

print(
    "BaseKnowledgeRecordBuilder preserved:",
    any(
        cls.__name__ == "BaseKnowledgeRecordBuilder"
        for cls in inspect.getmro(SynsetRecordBuilder)
    ),
)


# ----------------------------------------------------------------------
# 3. Builder construction
# ----------------------------------------------------------------------

print("\n3. BUILDER CONSTRUCTION")
print("-" * 110)

builder = SynsetRecordBuilder()

print("Construction : SUCCESS")
print("Signature    :", inspect.signature(SynsetRecordBuilder))


# ----------------------------------------------------------------------
# 4. Canonical Lexeme construction
# ----------------------------------------------------------------------

print("\n4. CANONICAL LEXEME CONSTRUCTION")
print("-" * 110)

metadata = LexemeMetadata(
    lemma="हरि",
    transliteration="hari",
    language="sanskrit",
    script="devanagari",
)

lexeme = Lexeme(
    identifier="lexeme:amarakosha:hari",
    metadata=metadata,
)

print("Lexeme construction : SUCCESS")
print("Identifier           :", lexeme.id)
print("Lemma                :", lexeme.lemma)
print("Kernel Lexeme        :", isinstance(lexeme, Lexeme))


# ----------------------------------------------------------------------
# 5. SynsetRecord construction
# ----------------------------------------------------------------------

print("\n5. SYNSET RECORD CONSTRUCTION")
print("-" * 110)

record = SynsetRecord(
    identifier="synset:amarakosha:test",
    source="amarakosha",
    source_identifier="amarakosha:test",
    source_version="1.0",
    kanda="svargadi",
    varga="deva",
    verse=1,
    sequence=1,
    devanagari="हरि",
    iast="hari",
    transliteration="hari",
    gloss="Vishnu",
    lexeme_ids=(lexeme.id,),
    tags=("test",),
    notes="Batch 5H-4 runtime verification",
)

print("SynsetRecord construction : SUCCESS")
print("Identifier                :", record.identifier)
print("Lexeme IDs                :", record.lexeme_ids)


# ----------------------------------------------------------------------
# 6. Existing record-only contract
# ----------------------------------------------------------------------

print("\n6. RECORD-ONLY BUILD CONTRACT")
print("-" * 110)

record_only_builder = SynsetRecordBuilder()

synset_without_lexemes = record_only_builder.build(record)

print("Build without Lexemes : SUCCESS")
print("Type                  :", type(synset_without_lexemes))
print("Identifier            :", synset_without_lexemes.identifier)
print("Child count           :", synset_without_lexemes.child_count)


# ----------------------------------------------------------------------
# 7. Resolved Lexeme boundary
# ----------------------------------------------------------------------

print("\n7. RESOLVED LEXEME BOUNDARY")
print("-" * 110)

resolved_builder = (
    SynsetRecordBuilder()
    .with_lexemes([lexeme])
)

synset = resolved_builder.build(record)

print("Build with Lexeme : SUCCESS")
print("Type              :", type(synset))
print("Identifier        :", synset.identifier)
print("Child count       :", synset.child_count)
print("Lexemes           :", list(synset.lexemes))


# ----------------------------------------------------------------------
# 8. Object identity
# ----------------------------------------------------------------------

print("\n8. LEXEME OBJECT IDENTITY")
print("-" * 110)

children = list(synset.lexemes)

identity_ok = (
    len(children) == 1
    and children[0] is lexeme
)

print("Same object identity :", identity_ok)
print("Canonical Lexeme     :", isinstance(children[0], Lexeme))


# ----------------------------------------------------------------------
# 9. Builder isolation
# ----------------------------------------------------------------------

print("\n9. BUILDER ISOLATION")
print("-" * 110)

builder_a = SynsetRecordBuilder().with_lexemes([lexeme])
builder_b = SynsetRecordBuilder()

synset_a = builder_a.build(record)
synset_b = builder_b.build(record)

print(
    "Builder A child count :",
    synset_a.child_count,
)

print(
    "Builder B child count :",
    synset_b.child_count,
)

print(
    "Builder isolation     :",
    synset_a.child_count == 1
    and synset_b.child_count == 0,
)


# ----------------------------------------------------------------------
# 10. Repository dependency check
# ----------------------------------------------------------------------

print("\n10. REPOSITORY DEPENDENCY CHECK")
print("-" * 110)

source = inspect.getsource(SynsetRecordBuilder)

repository_dependency = (
    "LexicalRepository" in source
    or "get_lexeme" in source
    or "InMemoryLexicalRepository" in source
)

print(
    "Repository dependency inside builder :",
    repository_dependency,
)

print(
    "Boundary preserved                    :",
    not repository_dependency,
)


# ----------------------------------------------------------------------
# 11. Decision gate
# ----------------------------------------------------------------------

print("\n11. BATCH 5H-4 DECISION GATE")
print("-" * 110)

checks = {
    "Framework inheritance preserved":
        any(
            cls.__name__ == "BaseKnowledgeRecordBuilder"
            for cls in inspect.getmro(SynsetRecordBuilder)
        ),

    "Record-only build preserved":
        synset_without_lexemes.child_count == 0,

    "Canonical Lexeme accepted":
        isinstance(children[0], Lexeme),

    "Lexeme object identity preserved":
        identity_ok,

    "Builder isolation preserved":
        synset_a.child_count == 1
        and synset_b.child_count == 0,

    "No repository dependency":
        not repository_dependency,
}

for name, result in checks.items():
    print(f"{name:<45}: {'PASS' if result else 'FAIL'}")

overall = all(checks.values())

print("\n" + "=" * 110)
print(
    "BATCH 5H-4 STATUS:",
    "PASS" if overall else "FAIL",
)
print("=" * 110)

if not overall:
    raise SystemExit(1)
