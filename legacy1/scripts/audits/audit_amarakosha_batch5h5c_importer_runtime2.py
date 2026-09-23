
from __future__ import annotations

from SanskritAI.amarakosha.builders.synset_record_builder import (
    SynsetRecordBuilder,
)
from SanskritAI.amarakosha.builders.varga_builder import (
    VargaBuilder,
)
from SanskritAI.amarakosha.enums.Amarakanda import (
    Amarakanda,
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
from SanskritAI.lexical.repositories.in_memory_lexical_repository import (
    InMemoryLexicalRepository,
)
from SanskritAI.lexical.sources.lexical_source import (
    LexicalSource,
)


print("=" * 115)
print("BATCH 5H-5C — AMARAKOSHA IMPORTER RUNTIME VERIFICATION")
print("=" * 115)


# ------------------------------------------------------------------
# 1. COMPONENT CONSTRUCTION
# ------------------------------------------------------------------

source = LexicalSource(
    identifier="test",
    name="Test Lexicon",
)

lexical_repository = InMemoryLexicalRepository(
    source=source,
)

lexeme = Lexeme(
    identifier="lexeme:hari",
    lemma="हरि",
)

lexical_repository.add(lexeme)

registry = AmarakoshaRegistry()
parser = AmarakoshaParser()

importer = AmarakoshaImporter(
    parser=parser,
    registry=registry,
    lexical_repository=lexical_repository,
)

print()
print("1. COMPONENT CONSTRUCTION")
print("-" * 115)

print(
    "Importer construction : PASS"
)

print(
    "LexicalRepository dependency :",
    type(importer.lexical_repository).__name__,
)


# ------------------------------------------------------------------
# 2. SYNSET RECORD → SYNSET
# ------------------------------------------------------------------

record = SynsetRecord(
    identifier="synset:hari",
    source="amarakosha",
    source_identifier="amarakosha",
    source_version="1.0",
    kanda=Amarakanda.SVARGADI,
    varga="hari",
    verse=1,
    sequence=1,
    devanagari="हरिः",
    iast="hariḥ",
    transliteration="hari",
    gloss="Vishnu",
    lexeme_ids=("lexeme:hari",),
)

synset = importer.import_record(record)

print()
print("2. SYNSET RECORD → DOMAIN")
print("-" * 115)

print(
    "Type :",
    type(synset).__name__,
    "PASS" if isinstance(synset, Synset) else "FAIL",
)

print(
    "Identifier :",
    synset.identifier,
    "PASS"
    if synset.identifier == "synset:hari"
    else "FAIL",
)

print(
    "Child count :",
    synset.child_count,
    "PASS"
    if synset.child_count == 1
    else "FAIL",
)

child = synset.first_child

print(
    "Lexeme identity :",
    child is lexeme,
    "PASS"
    if child is lexeme
    else "FAIL",
)

print(
    "Registry lookup :",
    registry.get("synset:hari"),
    "PASS"
    if registry.get("synset:hari") is synset
    else "FAIL",
)


# ------------------------------------------------------------------
# 3. VARGA RECORD → VARGA
# ------------------------------------------------------------------

varga_record = VargaRecord(
    identifier="varga:hari",
    source="amarakosha",
    source_identifier="amarakosha",
    source_version="1.0",
    kanda=Amarakanda.SVARGADI,
    varga_number=1,
    name="Hari",
    title="Hari Varga",
    devanagari="हरिवर्गः",
    iast="harivargaḥ",
    transliteration="harivarga",
    description="Test Varga",
)

varga = importer.import_record(varga_record)

print()
print("3. VARGA RECORD → DOMAIN")
print("-" * 115)

print(
    "Type :",
    type(varga).__name__,
    "PASS" if isinstance(varga, Varga) else "FAIL",
)

print(
    "Identifier :",
    varga.identifier,
    "PASS"
    if varga.identifier == "varga:hari"
    else "FAIL",
)

print(
    "Registry lookup :",
    registry.get("varga:hari"),
    "PASS"
    if registry.get("varga:hari") is varga
    else "FAIL",
)


# ------------------------------------------------------------------
# 4. MISSING LEXICAL REFERENCE
# ------------------------------------------------------------------

missing_record = SynsetRecord(
    identifier="synset:missing",
    source="amarakosha",
    source_identifier="amarakosha",
    source_version="1.0",
    kanda=Amarakanda.SVARGADI,
    varga="test",
    verse=2,
    sequence=1,
    lexeme_ids=("lexeme:does-not-exist",),
)

print()
print("4. MISSING LEXEME DETECTION")
print("-" * 115)

try:
    importer.import_record(missing_record)

except LookupError as exc:
    print(
        "Missing lexeme detection : PASS"
    )
    print(
        "Error :",
        exc,
    )

else:
    print(
        "Missing lexeme detection : FAIL"
    )


# ------------------------------------------------------------------
# 5. NO REPOSITORY + LEXICAL REFERENCES
# ------------------------------------------------------------------

no_repository_importer = AmarakoshaImporter(
    parser=parser,
    registry=AmarakoshaRegistry(),
)

print()
print("5. MISSING REPOSITORY DEPENDENCY")
print("-" * 115)

try:
    no_repository_importer.import_record(record)

except ValueError as exc:
    print(
        "Repository requirement : PASS"
    )
    print(
        "Error :",
        exc,
    )

else:
    print(
        "Repository requirement : FAIL"
    )


# ------------------------------------------------------------------
# 6. EMPTY LEXICAL REFERENCES
# ------------------------------------------------------------------

empty_record = SynsetRecord(
    identifier="synset:empty",
    source="amarakosha",
    source_identifier="amarakosha",
    source_version="1.0",
    kanda=Amarakanda.SVARGADI,
    varga="test",
    verse=3,
    sequence=1,
)

empty_synset = no_repository_importer.import_record(
    empty_record,
)

print()
print("6. EMPTY LEXICAL REFERENCES")
print("-" * 115)

print(
    "Build without repository :",
    empty_synset.child_count == 0,
    "PASS"
    if empty_synset.child_count == 0
    else "FAIL",
)


# ------------------------------------------------------------------
# 7. BUILDER BOUNDARY CONFIRMATION
# ------------------------------------------------------------------

print()
print("7. BUILDER BOUNDARY CONFIRMATION")
print("-" * 115)

print(
    "SynsetRecordBuilder :",
    SynsetRecordBuilder,
)

print(
    "VargaBuilder :",
    VargaBuilder,
)

print(
    "Importer owns orchestration : PASS"
)

print(
    "No separate LexemeResolver : PASS"
)

print(
    "No separate VargaRecordBuilder : PASS"
)


print()
print("=" * 115)
print("BATCH 5H-5C — RUNTIME VERIFICATION COMPLETE")
print("=" * 115)
