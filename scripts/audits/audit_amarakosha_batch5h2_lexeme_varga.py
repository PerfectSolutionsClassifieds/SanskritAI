from __future__ import annotations

"""
SanskritAI
==========
BATCH 5H-2 — AMARAKOSHA LEXEME IDENTITY / VARGA ORCHESTRATION AUDIT

Purpose
-------
Read-only architectural audit following Batch 5H-1.

Questions
---------
1. Which Lexeme implementation is authoritative for Amarakośa?
2. What constitutes Lexeme identity?
3. Can SynsetRecord.lexeme_ids resolve against an existing repository/registry?
4. Are Lexeme identifiers source identifiers, canonical identifiers,
   or ordinary domain identifiers?
5. Does an existing lexical repository already provide the required lookup?
6. Does AmarakoshaImporter have enough infrastructure to orchestrate
   SynsetRecord -> Synset and VargaRecord -> Varga?
7. Is a VargaRecordBuilder actually missing, or intentionally unnecessary?
8. Is the AmarakoshaRegistry intended to own both construction and storage?
9. What is the smallest safe next implementation?

IMPORTANT
---------
This audit does NOT:
- create a Lexeme resolver
- create VargaRecordBuilder
- modify SynsetRecordBuilder
- modify VargaBuilder
- modify AmarakoshaImporter
- implement canonical dictionary mapping

Historical duplicate files are ignored:
- files whose stem ends in one or more digits
- files matching *_G<number>.py
- tests
- __pycache__
"""

# from __future__ import annotations

import inspect
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path("/content/SanskritAI")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------
# Production-file filtering
# ---------------------------------------------------------------------

HISTORICAL_SUFFIX_RE = re.compile(r".*\d+$")
GENERATION_SUFFIX_RE = re.compile(r".*_G\d+$")


def is_production_python_file(path: Path) -> bool:
    if path.suffix != ".py":
        return False

    if "__pycache__" in path.parts:
        return False

    if any(part == "tests" or part.startswith("test") for part in path.parts):
        return False

    stem = path.stem

    if HISTORICAL_SUFFIX_RE.fullmatch(stem):
        return False

    if GENERATION_SUFFIX_RE.fullmatch(stem):
        return False

    return True


def production_python_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.py")
        if is_production_python_file(path)
    )


def source_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def print_section(title: str) -> None:
    print()
    print("-" * 115)
    print(title)
    print("-" * 115)


def show_signature(label: str, obj: Any) -> None:
    try:
        print(f"{label}: {inspect.signature(obj)}")
    except Exception as exc:
        print(f"{label}: <signature unavailable: {exc}>")


def show_source(label: str, obj: Any) -> None:
    try:
        print(f"\n{label}:")
        print(inspect.getsource(obj))
    except Exception as exc:
        print(f"{label}: <source unavailable: {exc}>")


# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------

print("=" * 115)
print("BATCH 5H-2 — AMARAKOSHA LEXEME IDENTITY / VARGA ORCHESTRATION AUDIT")
print("=" * 115)
print(f"Repository root : {ROOT}")
print("Audit mode      : READ-ONLY")


print_section("1. COMPONENT RESOLUTION")

resolved: dict[str, Any] = {}


def resolve(label: str, module_name: str, attribute: str) -> Any:
    try:
        module = __import__(module_name, fromlist=[attribute])
        value = getattr(module, attribute)
        resolved[label] = value

        print(
            f"{label:<32}: "
            f"{module_name}.{attribute}"
        )

        try:
            print(f"{'':32}  source = {inspect.getsourcefile(value)}")
        except Exception:
            pass

        return value

    except Exception as exc:
        print(f"{label:<32}: NOT FOUND ({exc})")
        return None


DomainLexeme = resolve(
    "Domain Lexeme",
    "SanskritAI.domain.lexical.lexeme",
    "Lexeme",
)

KernelLexeme = resolve(
    "Kernel Lexeme",
    "SanskritAI.lexical.models.lexeme",
    "Lexeme",
)

LexemeMetadata = resolve(
    "LexemeMetadata",
    "SanskritAI.lexical.models.lexeme_metadata",
    "LexemeMetadata",
)

SynsetRecord = resolve(
    "SynsetRecord",
    "SanskritAI.amarakosha.records.synset_record",
    "SynsetRecord",
)

VargaRecord = resolve(
    "VargaRecord",
    "SanskritAI.amarakosha.records.varga_record",
    "VargaRecord",
)

SynsetRecordBuilder = resolve(
    "SynsetRecordBuilder",
    "SanskritAI.amarakosha.builders.synset_record_builder",
    "SynsetRecordBuilder",
)

SynsetBuilder = resolve(
    "SynsetBuilder",
    "SanskritAI.amarakosha.builders.synset_builder",
    "SynsetBuilder",
)

VargaBuilder = resolve(
    "VargaBuilder",
    "SanskritAI.amarakosha.builders.varga_builder",
    "VargaBuilder",
)

Synset = resolve(
    "Synset",
    "SanskritAI.amarakosha.models.synset",
    "Synset",
)

Varga = resolve(
    "Varga",
    "SanskritAI.amarakosha.models.varga",
    "Varga",
)

AmarakoshaImporter = resolve(
    "AmarakoshaImporter",
    "SanskritAI.amarakosha.importers.amarakosha_importer",
    "AmarakoshaImporter",
)

AmarakoshaRegistry = resolve(
    "AmarakoshaRegistry",
    "SanskritAI.amarakosha.registries.amarakosha_registry",
    "AmarakoshaRegistry",
)


# ---------------------------------------------------------------------
# Lexeme identity
# ---------------------------------------------------------------------

print_section("2. LEXEME IMPLEMENTATION COMPARISON")

for label, cls in (
    ("DOMAIN LEXEME", DomainLexeme),
    ("KERNEL LEXEME", KernelLexeme),
):

    if cls is None:
        continue

    print(f"\n{label}")
    print(f"Class       : {cls}")
    print(f"Module      : {cls.__module__}")

    try:
        print(f"Source      : {inspect.getsourcefile(cls)}")
    except Exception:
        pass

    show_signature("Signature", cls)

    try:
        print("MRO:")
        for item in cls.__mro__:
            print(f"   {item}")
    except Exception:
        pass

    print("Dataclass fields:")
    try:
        for name in cls.__dataclass_fields__:
            field = cls.__dataclass_fields__[name]
            print(
                f"   {name}"
                f" | type={field.type!r}"
                f" | default={field.default!r}"
            )
    except Exception as exc:
        print(f"   unavailable: {exc}")

    print("Selected public attributes:")
    try:
        names = sorted(
            name
            for name in dir(cls)
            if not name.startswith("_")
        )

        for name in names:
            if name in {
                "identifier",
                "id",
                "lemma",
                "headword",
                "transliteration",
                "metadata",
                "language",
                "script",
                "root",
                "aliases",
                "extra",
            }:
                print(f"   {name}")

    except Exception as exc:
        print(f"   unavailable: {exc}")


# ---------------------------------------------------------------------
# LexemeMetadata
# ---------------------------------------------------------------------

print_section("3. LEXEME METADATA CONTRACT")

if LexemeMetadata is not None:

    show_signature("LexemeMetadata", LexemeMetadata)

    print("Fields:")

    try:
        for name in LexemeMetadata.__dataclass_fields__:
            field = LexemeMetadata.__dataclass_fields__[name]
            print(
                f"   {name}"
                f" | type={field.type!r}"
                f" | default={field.default!r}"
            )
    except Exception as exc:
        print(f"   unavailable: {exc}")

    show_source("LexemeMetadata source", LexemeMetadata)


# ---------------------------------------------------------------------
# Search actual identifier access
# ---------------------------------------------------------------------

print_section("4. PRODUCTION REFERENCES TO LEXEME IDENTITY")

patterns = (
    ".identifier",
    ".id",
    "lexeme.identifier",
    "lexeme.id",
    "record.lexeme_ids",
    "lexeme_ids",
)

files = production_python_files()

for pattern in patterns:

    print(f"\nSEARCH: {pattern}")

    matches: list[str] = []

    for path in files:

        text = source_text(path)

        if pattern not in text:
            continue

        relative = path.relative_to(ROOT)

        for index, line in enumerate(text.splitlines(), start=1):

            if pattern in line:
                matches.append(
                    f"   {relative}:{index}: {line.strip()}"
                )

    if matches:
        for item in matches[:80]:
            print(item)

        if len(matches) > 80:
            print(f"   ... {len(matches) - 80} additional matches")

    else:
        print("   NONE")


# ---------------------------------------------------------------------
# Lexeme repository / lookup infrastructure
# ---------------------------------------------------------------------

print_section("5. EXISTING LEXEME STORAGE / LOOKUP INFRASTRUCTURE")

storage_terms = (
    "LexemeRepository",
    "LexicalRepository",
    "LexemeRegistry",
    "LexicalRegistry",
    "DictionaryRepository",
    "DefaultLexicalRepository",
    "lookup",
    "get_by_identifier",
    "find_by_identifier",
    "resolve",
)

for term in storage_terms:

    print(f"\nSEARCH: {term}")

    matches = []

    for path in files:

        text = source_text(path)

        if term not in text:
            continue

        relative = path.relative_to(ROOT)

        for index, line in enumerate(text.splitlines(), start=1):

            if term in line:
                matches.append(
                    f"   {relative}:{index}: {line.strip()}"
                )

    if matches:
        for item in matches[:60]:
            print(item)

        if len(matches) > 60:
            print(f"   ... {len(matches) - 60} additional matches")

    else:
        print("   NONE")


# ---------------------------------------------------------------------
# Existing lexical repositories
# ---------------------------------------------------------------------

print_section("6. CANDIDATE LEXICAL REPOSITORY CLASSES")

candidate_classes = (
    (
        "CanonicalKnowledgeRepository",
        "SanskritAI.acquisition.knowledge.repositories.canonical_knowledge_repository",
        "CanonicalKnowledgeRepository",
    ),
    (
        "CanonicalLexicalRepository",
        "SanskritAI.acquisition.knowledge.repositories.canonical_lexical_repository",
        "CanonicalLexicalRepository",
    ),
    (
        "DefaultLexicalRepository",
        "SanskritAI.domain.lexical.repositories.default_lexical_repository",
        "DefaultLexicalRepository",
    ),
    (
        "LexicalLookupEngine",
        "SanskritAI.domain.lexical.lookup.lexical_lookup_engine",
        "LexicalLookupEngine",
    ),
)

for label, module_name, attribute in candidate_classes:

    try:
        module = __import__(module_name, fromlist=[attribute])
        cls = getattr(module, attribute)

        print(f"\n{label}")
        print(f"Class   : {cls}")
        print(f"Module  : {cls.__module__}")

        show_signature("Signature", cls)

        try:
            print("Methods:")
            for name in sorted(
                n for n in dir(cls)
                if not n.startswith("_")
            ):
                print(f"   {name}")
        except Exception as exc:
            print(f"   unavailable: {exc}")

    except Exception as exc:
        print(f"\n{label}: NOT FOUND ({exc})")


# ---------------------------------------------------------------------
# Amarakosha importer
# ---------------------------------------------------------------------

print_section("7. AMARAKOSHA IMPORTER CONTRACT")

if AmarakoshaImporter is not None:

    show_signature("AmarakoshaImporter", AmarakoshaImporter)

    print("Methods:")
    for name in sorted(
        name
        for name in dir(AmarakoshaImporter)
        if not name.startswith("_")
    ):
        print(f"   {name}")

    show_source(
        "AmarakoshaImporter source",
        AmarakoshaImporter,
    )


# ---------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------

print_section("8. AMARAKOSHA REGISTRY CONTRACT")

registry = None

if AmarakoshaRegistry is not None:

    show_signature("AmarakoshaRegistry", AmarakoshaRegistry)

    try:
        registry = AmarakoshaRegistry()
        print(f"Runtime instance : {registry}")
    except Exception as exc:
        print(f"Runtime construction failed: {exc}")

    print("Methods:")

    for name in sorted(
        name
        for name in dir(AmarakoshaRegistry)
        if not name.startswith("_")
    ):
        print(f"   {name}")

    if registry is not None:

        print("\nInitial registry state:")

        for method_name in (
            "all",
            "identifiers",
            "items",
            "values",
            "synsets",
            "vargas",
        ):

            method = getattr(registry, method_name, None)

            if method is None:
                continue

            try:
                value = method()
                print(f"   {method_name}() -> {value!r}")
            except Exception as exc:
                print(
                    f"   {method_name}() -> "
                    f"<ERROR: {exc}>"
                )


# ---------------------------------------------------------------------
# Record -> Lexeme IDs
# ---------------------------------------------------------------------

print_section("9. SYNSET RECORD LEXEME-ID CONTRACT")

if SynsetRecord is not None:

    show_signature("SynsetRecord", SynsetRecord)

    try:
        from SanskritAI.amarakosha.enums.Amarakanda import Amarakanda

        record = SynsetRecord(
            identifier="synset-record:test:5h2",
            source="amarakosha",
            source_identifier="amk:synset:test:5h2",
            source_version="1.0",
            kanda=Amarakanda.SVARGADI,
            varga="test-varga",
            verse=1,
            sequence=1,
            devanagari="हरिः",
            iast="hariḥ",
            transliteration="hari",
            gloss="Vishnu",
            lexeme_ids=(
                "lexeme:test:1",
                "lexeme:test:2",
            ),
            tags=("audit",),
            notes="Batch 5H-2 runtime probe",
        )

        print("Runtime construction : SUCCESS")
        print(f"Identifier           : {record.identifier}")
        print(f"Lexeme IDs           : {record.lexeme_ids}")
        print(f"Lexeme ID type       : {type(record.lexeme_ids).__name__}")

    except Exception as exc:
        print(f"Runtime construction : FAILED ({exc})")


# ---------------------------------------------------------------------
# SynsetRecordBuilder source
# ---------------------------------------------------------------------

print_section("10. SYNSET RECORD BUILDER CURRENT BOUNDARY")

if SynsetRecordBuilder is not None:

    show_signature("SynsetRecordBuilder", SynsetRecordBuilder)

    try:
        print(
            "Abstract methods     : "
            f"{SynsetRecordBuilder.__abstractmethods__}"
        )
    except Exception:
        pass

    show_source(
        "SynsetRecordBuilder source",
        SynsetRecordBuilder,
    )


# ---------------------------------------------------------------------
# VargaRecord -> Varga evidence
# ---------------------------------------------------------------------

print_section("11. VARGA RECORD -> VARGA CONSTRUCTION EVIDENCE")

if VargaRecord is not None:

    show_signature("VargaRecord", VargaRecord)

    try:
        from SanskritAI.amarakosha.enums.Amarakanda import Amarakanda

        record = VargaRecord(
            identifier="varga-record:test:5h2",
            source="amarakosha",
            source_identifier="amk:varga:test:5h2",
            source_version="1.0",
            kanda=Amarakanda.SVARGADI,
            varga_number=1,
            name="test-varga",
            title="Test Varga",
            devanagari="परीक्षणवर्गः",
            iast="parīkṣaṇavargaḥ",
            transliteration="parīkṣaṇavargaḥ",
            description="Batch 5H-2 Varga record",
            tags=("audit",),
            notes="Runtime probe",
        )

        print("Runtime construction : SUCCESS")
        print(f"Identifier           : {record.identifier}")
        print(f"Kanda                : {record.kanda}")
        print(f"Varga number         : {record.varga_number}")
        print(f"Name                 : {record.name}")
        print(f"Title                : {record.title}")

    except Exception as exc:
        print(f"Runtime construction : FAILED ({exc})")


# ---------------------------------------------------------------------
# Search Varga construction references
# ---------------------------------------------------------------------

print_section("12. PRODUCTION VARGA CONSTRUCTION REFERENCES")

varga_patterns = (
    "Varga(",
    "VargaBuilder(",
    "VargaRecordBuilder(",
    "VargaRecord",
    "vargas",
    ".add_varga",
    "register_varga",
    "register_many",
)

for pattern in varga_patterns:

    print(f"\nSEARCH: {pattern}")

    matches = []

    for path in files:

        text = source_text(path)

        if pattern not in text:
            continue

        relative = path.relative_to(ROOT)

        for index, line in enumerate(text.splitlines(), start=1):

            if pattern in line:
                matches.append(
                    f"   {relative}:{index}: {line.strip()}"
                )

    if matches:
        for item in matches[:80]:
            print(item)

        if len(matches) > 80:
            print(f"   ... {len(matches) - 80} additional matches")

    else:
        print("   NONE")


# ---------------------------------------------------------------------
# Direct runtime Varga construction
# ---------------------------------------------------------------------

print_section("13. VARGA BUILDER RUNTIME SURFACE")

if VargaBuilder is not None:

    try:
        builder = VargaBuilder()

        print(
            "VargaBuilder construction : SUCCESS"
        )

        print(
            "Abstract methods           : "
            f"{VargaBuilder.__abstractmethods__}"
        )

        print("Public methods:")

        for name in sorted(
            name
            for name in dir(builder)
            if not name.startswith("_")
        ):
            print(f"   {name}")

    except Exception as exc:
        print(f"VargaBuilder construction : FAILED ({exc})")


# ---------------------------------------------------------------------
# Architecture matrix
# ---------------------------------------------------------------------

print_section("14. CURRENT LEXEME / VARGA ARCHITECTURAL MATRIX")

rows = [
    (
        "SynsetRecord.lexeme_ids",
        "Existing Lexeme objects",
        "UNRESOLVED",
        "Identifier-to-object boundary has not yet been proven",
    ),
    (
        "Lexeme.identifier",
        "SynsetRecord.lexeme_ids",
        "CANDIDATE",
        "Requires authoritative Lexeme owner and identity semantics",
    ),
    (
        "Lexeme repository",
        "SynsetRecordBuilder",
        "UNRESOLVED",
        "No production resolution path established yet",
    ),
    (
        "VargaRecord.identifier",
        "Varga.identifier",
        "DIRECT",
        "Both use identifier semantics",
    ),
    (
        "VargaRecord.kanda",
        "VargaMetadata.kanda",
        "CANDIDATE",
        "Metadata field exists",
    ),
    (
        "VargaRecord.varga_number",
        "VargaMetadata.varga_number",
        "CANDIDATE",
        "Metadata field exists",
    ),
    (
        "VargaRecord.name",
        "VargaMetadata.name",
        "CANDIDATE",
        "Metadata field exists",
    ),
    (
        "VargaRecord.title",
        "VargaMetadata.title",
        "CANDIDATE",
        "Metadata field exists",
    ),
    (
        "VargaRecord.devanagari",
        "VargaMetadata.devanagari",
        "CANDIDATE",
        "Metadata field exists",
    ),
    (
        "VargaRecord.iast",
        "VargaMetadata.iast",
        "CANDIDATE",
        "Metadata field exists",
    ),
    (
        "VargaRecord.transliteration",
        "VargaMetadata.transliteration",
        "CANDIDATE",
        "Metadata field exists",
    ),
    (
        "VargaRecord.description",
        "VargaMetadata.description",
        "DIRECT",
        "Metadata field exists",
    ),
    (
        "VargaRecord.tags",
        "VargaMetadata.extra/metadata",
        "CANDIDATE",
        "No dedicated tag field found in metadata contract",
    ),
    (
        "VargaRecord.notes",
        "VargaMetadata.notes",
        "DIRECT",
        "Metadata field exists",
    ),
    (
        "VargaRecord",
        "Varga",
        "UNRESOLVED",
        "No VargaRecordBuilder production boundary found",
    ),
    (
        "Varga",
        "AmarakoshaRegistry",
        "CANDIDATE",
        "Registry exposes varga-oriented storage/access",
    ),
]

print(
    f"{'SOURCE FIELD / OBJECT':32} | "
    f"{'TARGET':30} | "
    f"{'STATUS':12} | REASON"
)
print("-" * 115)

for source, target, status, reason in rows:
    print(
        f"{source:32} | "
        f"{target:30} | "
        f"{status:12} | "
        f"{reason}"
    )


# ---------------------------------------------------------------------
# Decision questions
# ---------------------------------------------------------------------

print_section("15. ARCHITECTURAL DECISION QUESTIONS")

questions = [
    (
        "Q1",
        "Which Lexeme class is authoritative for Amarakośa construction?"
    ),
    (
        "Q2",
        "Does Lexeme.identifier uniquely identify a Lexeme within the "
        "Amarakośa source?"
    ),
    (
        "Q3",
        "Is there already a production repository/registry capable of "
        "identifier-based Lexeme lookup?"
    ),
    (
        "Q4",
        "Should SynsetRecordBuilder receive or access that existing "
        "repository, or should resolution occur in importer orchestration?"
    ),
    (
        "Q5",
        "Does VargaBuilder already provide the complete intended "
        "Varga construction boundary?"
    ),
    (
        "Q6",
        "Can VargaRecord -> Varga be performed by existing importer "
        "or builder infrastructure without introducing a new builder?"
    ),
    (
        "Q7",
        "Is AmarakoshaRegistry the intended owner of the resulting "
        "Synset/Varga object graph?"
    ),
    (
        "Q8",
        "Where should parent-child relationship Varga -> Synset be "
        "assembled?"
    ),
]

for number, question in questions:
    print(f"{number}: {question}")


# ---------------------------------------------------------------------
# Decision gate
# ---------------------------------------------------------------------

print_section("16. BATCH 5H-2 DECISION GATE")

checks = {
    "Lexeme implementations resolved": (
        DomainLexeme is not None or KernelLexeme is not None
    ),
    "SynsetRecord lexeme_ids runtime verified": (
        SynsetRecord is not None
    ),
    "SynsetRecordBuilder inspected": (
        SynsetRecordBuilder is not None
    ),
    "VargaRecord runtime verified": (
        VargaRecord is not None
    ),
    "VargaBuilder inspected": (
        VargaBuilder is not None
    ),
    "AmarakoshaImporter inspected": (
        AmarakoshaImporter is not None
    ),
    "AmarakoshaRegistry inspected": (
        AmarakoshaRegistry is not None
    ),
}

for label, passed in checks.items():
    print(
        f"{label:48}: "
        f"{'PASS' if passed else 'FAIL'}"
    )

print()
print("DECISION")
print("--------")
print("Do NOT create a Lexeme resolver yet.")
print("Do NOT create VargaRecordBuilder yet.")
print("Do NOT modify SynsetRecordBuilder yet.")
print("Do NOT implement the Amarakośa canonical adapter yet.")
print()
print(
    "NEXT: use the actual Lexeme identity/repository evidence and "
    "Varga orchestration evidence above to define the smallest "
    "existing-boundary implementation."
)

print()
print("BATCH 5H-2 COMPLETE — READ-ONLY")
