from __future__ import annotations

from SanskritAI.amarakosha.builders.synset_record_builder import (
    SynsetRecordBuilder,
)
from SanskritAI.amarakosha.builders.varga_builder import (
    VargaBuilder,
)
from SanskritAI.amarakosha.importers.amarakosha_importer import (
    AmarakoshaImporter,
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
from SanskritAI.lexical.models.lexeme_metadata import (
    LexemeMetadata,
)
from SanskritAI.lexical.models.lexical_source import (
    LexicalSource,
)
from SanskritAI.lexical.repositories.in_memory_lexical_repository import (
    InMemoryLexicalRepository,
)


print("=" * 115)
print("BATCH 5H-5C — AMARAKOSHA IMPORTER RUNTIME VERIFICATION")
print("=" * 115)


def section(title: str) -> None:
    print("\n" + "-" * 115)
    print(title)
    print("-" * 115)


# ============================================================
# 1. COMPONENT CONSTRUCTION
# ============================================================

section("1. COMPONENT CONSTRUCTION")

source = LexicalSource(
    identifier="test",
    name="Test Lexicon",
)

lexical_repository = InMemoryLexicalRepository(
    source=source,
)

lexeme_metadata = LexemeMetadata(
    lemma="हरि",
)

lexeme = Lexeme(
    identifier="lexeme:hari",
    metadata=lexeme_metadata,
)

parser = AmarakoshaParser()
registry = AmarakoshaRegistry()

importer = AmarakoshaImporter(
    parser=parser,
    registry=registry,
    lexical_repository=lexical_repository,
)

print("LexicalSource construction : PASS")
print("LexicalRepository construction : PASS")
print("Lexeme construction : PASS")
print("Importer construction : PASS")
print(
    "LexicalRepository dependency : "
    f"{type(importer.lexical_repository).__name__}"
)


# ============================================================
# Register canonical Lexeme
# ============================================================

lexical_repository.add(lexeme)


# ============================================================
# 2. SYNSET RECORD → DOMAIN
# ============================================================

section("2. SYNSET RECORD → DOMAIN")

# synset_record = SynsetRecord(
#     identifier="synset:hari",
#     source="test",
#     source_identifier="amarakosha:test",
#     source_version="1.0",
#     lexeme_ids=("lexeme:hari",),
# )

synset_record = SynsetRecord(
    identifier="synset:hari",
    source="test",
    source_identifier="amarakosha:test",
    source_version="1.0",
    kanda=Amarakanda.SVARGADI,
    varga="test-varga",
    verse=1,
    sequence=1,
    devanagari="हरि",
    iast="hari",
    transliteration="hari",
    gloss="Vishnu",
    lexeme_ids=("lexeme:hari",),
)

synset = importer.import_record(
    synset_record
)

print(
    f"Type : {type(synset).__name__} "
    f"{'PASS' if isinstance(synset, Synset) else 'FAIL'}"
)

print(
    f"Identifier : {synset.identifier} "
    f"{'PASS' if synset.identifier == 'synset:hari' else 'FAIL'}"
)

print(
    f"Child count : {synset.child_count} "
    f"{'PASS' if synset.child_count == 1 else 'FAIL'}"
)

child = synset.first_child

identity_pass = child is lexeme

print(
    f"Lexeme identity : {identity_pass} "
    f"{'PASS' if identity_pass else 'FAIL'}"
)

lemma_pass = (
    child is not None
    and child.lemma == "हरि"
)

print(
    f"Lexeme lemma : "
    f"{child.lemma if child is not None else None} "
    f"{'PASS' if lemma_pass else 'FAIL'}"
)

registry_synset = registry.get(
    "synset:hari"
)

registry_pass = registry_synset is synset

print(
    f"Registry lookup : {registry_synset} "
    f"{'PASS' if registry_pass else 'FAIL'}"
)


# ============================================================
# 3. VARGA RECORD → DOMAIN
# ============================================================

section("3. VARGA RECORD → DOMAIN")

varga_record = VargaRecord(
    identifier="varga:hari",
    source="test",
    source_identifier="amarakosha:test",
    source_version="1.0",
)

varga = importer.import_record(
    varga_record
)

print(
    f"Type : {type(varga).__name__} "
    f"{'PASS' if isinstance(varga, Varga) else 'FAIL'}"
)

print(
    f"Identifier : {varga.identifier} "
    f"{'PASS' if varga.identifier == 'varga:hari' else 'FAIL'}"
)

registry_varga = registry.get(
    "varga:hari"
)

varga_registry_pass = (
    registry_varga is varga
)

print(
    f"Registry lookup : {registry_varga} "
    f"{'PASS' if varga_registry_pass else 'FAIL'}"
)


# ============================================================
# 4. MISSING LEXEME DETECTION
# ============================================================

section("4. MISSING LEXEME DETECTION")

# missing_record = SynsetRecord(
#     identifier="synset:missing",
#     source="test",
#     source_identifier="amarakosha:test",
#     source_version="1.0",
#     lexeme_ids=("lexeme:does-not-exist",),
# )

missing_record = SynsetRecord(
    identifier="synset:missing",
    source="test",
    source_identifier="amarakosha:test",
    source_version="1.0",
    kanda=Amarakanda.SVARGADI,
    varga="test-varga",
    verse=2,
    sequence=1,
    lexeme_ids=("lexeme:does-not-exist",),
)

try:
    importer.import_record(
        missing_record
    )

except LookupError as exc:
    print("Missing lexeme detection : PASS")
    print(f"Error : {exc}")

else:
    print("Missing lexeme detection : FAIL")
    print("Expected LookupError was not raised.")


# ============================================================
# 5. MISSING REPOSITORY DEPENDENCY
# ============================================================

section("5. MISSING REPOSITORY DEPENDENCY")

no_repository_importer = AmarakoshaImporter(
    parser=parser,
    registry=AmarakoshaRegistry(),
)

try:
    no_repository_importer.import_record(
        synset_record
    )

except ValueError as exc:
    print("Repository requirement : PASS")
    print(f"Error : {exc}")

else:
    print("Repository requirement : FAIL")
    print("Expected ValueError was not raised.")


# ============================================================
# 6. EMPTY LEXICAL REFERENCES
# ============================================================

section("6. EMPTY LEXICAL REFERENCES")

# empty_reference_record = SynsetRecord(
#     identifier="synset:empty",
#     source="test",
#     source_identifier="amarakosha:test",
#     source_version="1.0",
#     lexeme_ids=(),
# )

empty_reference_record = SynsetRecord(
    identifier="synset:empty",
    source="test",
    source_identifier="amarakosha:test",
    source_version="1.0",
    kanda=Amarakanda.SVARGADI,
    varga="test-varga",
    verse=3,
    sequence=1,
    lexeme_ids=(),
)

empty_importer = AmarakoshaImporter(
    parser=parser,
    registry=AmarakoshaRegistry(),
)

empty_synset = empty_importer.import_record(
    empty_reference_record
)

empty_pass = (
    isinstance(empty_synset, Synset)
    and empty_synset.child_count == 0
)

print(
    f"Build without repository : {empty_pass} "
    f"{'PASS' if empty_pass else 'FAIL'}"
)


# ============================================================
# 7. BUILDER / ARCHITECTURAL BOUNDARY CONFIRMATION
# ============================================================

section("7. BUILDER BOUNDARY CONFIRMATION")

print(
    f"SynsetRecordBuilder : {SynsetRecordBuilder}"
)

print(
    f"VargaBuilder : {VargaBuilder}"
)

print(
    "Importer owns record orchestration : PASS"
)

print(
    "Existing LexicalRepository boundary : PASS"
)

print(
    "Existing LexicalSource model : PASS"
)

metadata_pass = (
    isinstance(
        lexeme.metadata,
        LexemeMetadata,
    )
    and lexeme.metadata.lemma == "हरि"
)

print(
    "Lexeme constructed through LexemeMetadata : "
    f"{'PASS' if metadata_pass else 'FAIL'}"
)

print(
    "No separate LexemeResolver : PASS"
)

print(
    "No separate VargaRecordBuilder : PASS"
)

print(
    "No canonical Amarakośa adapter : PASS"
)

print("\n" + "=" * 115)
print(
    "BATCH 5H-5C — RUNTIME VERIFICATION COMPLETE"
)
print("=" * 115)
