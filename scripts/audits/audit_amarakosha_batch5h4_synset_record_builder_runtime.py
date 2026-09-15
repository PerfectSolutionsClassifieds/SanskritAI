
from __future__ import annotations

import ast
import inspect
from pathlib import Path

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

framework_preserved = any(
    cls.__name__ == "BaseKnowledgeRecordBuilder"
    for cls in inspect.getmro(SynsetRecordBuilder)
)

print(
    "BaseKnowledgeRecordBuilder preserved:",
    framework_preserved,
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

builder_isolation = (
    synset_a.child_count == 1
    and synset_b.child_count == 0
)

print("Builder A child count :", synset_a.child_count)
print("Builder B child count :", synset_b.child_count)
print("Builder isolation     :", builder_isolation)


# ----------------------------------------------------------------------
# 10. Production dependency inspection
# ----------------------------------------------------------------------

print("\n10. PRODUCTION DEPENDENCY INSPECTION")
print("-" * 110)

builder_source_file = Path(
    inspect.getsourcefile(SynsetRecordBuilder)
)

print("Source file:")
print(" ", builder_source_file)


# Parse the actual production source and inspect imports.
#
# This deliberately ignores:
#   - docstrings
#   - comments
#   - explanatory strings
#
# We only want to know whether the production module actually imports
# or references repository classes.

tree = ast.parse(
    builder_source_file.read_text(
        encoding="utf-8"
    )
)

imported_names: set[str] = set()
imported_modules: set[str] = set()

for node in ast.walk(tree):

    if isinstance(node, ast.Import):
        for alias in node.names:
            imported_modules.add(alias.name)
            imported_names.add(alias.asname or alias.name.split(".")[-1])

    elif isinstance(node, ast.ImportFrom):
        if node.module:
            imported_modules.add(node.module)

        for alias in node.names:
            imported_names.add(
                alias.asname or alias.name
            )


repository_imports = sorted(
    name
    for name in imported_names
    if "Repository" in name
)

repository_modules = sorted(
    module
    for module in imported_modules
    if "repository" in module.lower()
)

print("\nImported names containing Repository:")
if repository_imports:
    for name in repository_imports:
        print("  ", name)
else:
    print("   NONE")

print("\nImported modules containing repository:")
if repository_modules:
    for module in repository_modules:
        print("  ", module)
else:
    print("   NONE")


# Also inspect executable AST references to repository identifiers.
#
# A repository dependency would require actual code-level references,
# not merely words appearing in documentation.

code_repository_names: set[str] = set()

for node in ast.walk(tree):

    if isinstance(node, ast.Name):
        if node.id in {
            "LexicalRepository",
            "InMemoryLexicalRepository",
        }:
            code_repository_names.add(node.id)

    elif isinstance(node, ast.Attribute):
        if node.attr in {
            "get_lexeme",
        }:
            code_repository_names.add(node.attr)


print("\nExecutable repository references:")
if code_repository_names:
    for name in sorted(code_repository_names):
        print("  ", name)
else:
    print("   NONE")


repository_dependency = bool(
    repository_imports
    or repository_modules
    or code_repository_names
)

print(
    "\nActual repository dependency :",
    repository_dependency,
)

print(
    "Documentation-only mentions ignored :",
    not repository_dependency,
)


# ----------------------------------------------------------------------
# 11. Decision gate
# ----------------------------------------------------------------------

print("\n11. BATCH 5H-4 DECISION GATE")
print("-" * 110)

checks = {
    "Framework inheritance preserved":
        framework_preserved,

    "Record-only build preserved":
        synset_without_lexemes.child_count == 0,

    "Canonical Lexeme accepted":
        isinstance(children[0], Lexeme),

    "Lexeme object identity preserved":
        identity_ok,

    "Builder isolation preserved":
        builder_isolation,

    "No repository dependency":
        not repository_dependency,
}

for name, result in checks.items():
    print(
        f"{name:<45}: "
        f"{'PASS' if result else 'FAIL'}"
    )

overall = all(checks.values())

print("\n" + "=" * 110)
print(
    "BATCH 5H-4 STATUS:",
    "PASS" if overall else "FAIL",
)
print("=" * 110)

if not overall:
    raise SystemExit(1)
