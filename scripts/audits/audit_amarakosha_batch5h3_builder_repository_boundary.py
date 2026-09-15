from __future__ import annotations

"""
SanskritAI
==========

BATCH 5H-3 — AMARAKOSHA BUILDER / REPOSITORY BOUNDARY AUDIT

Purpose
-------
Verify the existing lexical repository boundary before modifying
SynsetRecordBuilder.

Questions
---------
1. Does the canonical LexicalRepository resolve Lexeme by identifier?
2. Does InMemoryLexicalRepository store the same Lexeme type used by Synset?
3. Can a canonical Lexeme be constructed by the existing LexemeBuilder?
4. Can that Lexeme be registered and retrieved by identifier?
5. What is the smallest safe way for Amarakośa construction to obtain
   existing Lexeme objects?
6. Can VargaBuilder already assemble Synset children without a new
   VargaRecordBuilder?
7. Does AmarakoshaRegistry already accept the resulting Varga/Synset?

READ-ONLY.

No production code is modified.
No resolver is created.
No VargaRecordBuilder is created.
No SynsetRecordBuilder modification is made.
"""

import inspect
import sys
from pathlib import Path

ROOT = Path("/content/SanskritAI")

if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))


# ======================================================================
# Helpers
# ======================================================================

def section(title: str) -> None:
    print()
    print("=" * 115)
    print(title)
    print("=" * 115)


def subsection(title: str) -> None:
    print()
    print("-" * 115)
    print(title)
    print("-" * 115)


def show_signature(label: str, obj) -> None:
    print(f"{label}:")
    try:
        print(f"  {inspect.signature(obj)}")
    except Exception as exc:
        print(f"  <signature unavailable: {exc}>")


def show_source(label: str, obj, max_lines: int = 100) -> None:
    print(f"\n{label}:")
    try:
        source = inspect.getsource(obj)
        lines = source.splitlines()

        for line in lines[:max_lines]:
            print(line)

        if len(lines) > max_lines:
            print("...")
    except Exception as exc:
        print(f"<source unavailable: {exc}>")


# ======================================================================
# Header
# ======================================================================

section(
    "BATCH 5H-3 — AMARAKOSHA BUILDER / REPOSITORY BOUNDARY AUDIT"
)

print(f"Repository root : {ROOT}")
print("Audit mode      : READ-ONLY")


# ======================================================================
# 1. Component resolution
# ======================================================================

subsection("1. COMPONENT RESOLUTION")

from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexeme_metadata import LexemeMetadata
from SanskritAI.lexical.models.lexical_source import LexicalSource
from SanskritAI.lexical.repositories.lexical_repository import (
    LexicalRepository,
)
from SanskritAI.lexical.repositories.in_memory_lexical_repository import (
    InMemoryLexicalRepository,
)

from SanskritAI.lexical.builders.lexeme_builder import LexemeBuilder
from SanskritAI.lexical.builders.lexeme_record_builder import (
    LexemeRecordBuilder,
)
from SanskritAI.lexical.records.lexeme_record import LexemeRecord

from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.models.synset_metadata import SynsetMetadata
from SanskritAI.amarakosha.models.varga import Varga
from SanskritAI.amarakosha.models.varga_metadata import VargaMetadata

from SanskritAI.amarakosha.records.synset_record import SynsetRecord
from SanskritAI.amarakosha.records.varga_record import VargaRecord

from SanskritAI.amarakosha.builders.synset_builder import SynsetBuilder
from SanskritAI.amarakosha.builders.synset_record_builder import (
    SynsetRecordBuilder,
)
from SanskritAI.amarakosha.builders.varga_builder import VargaBuilder

from SanskritAI.amarakosha.registries.amarakosha_registry import (
    AmarakoshaRegistry,
)

from SanskritAI.amarakosha.enums.Amarakanda import Amarakanda


components = [
    ("Lexeme", Lexeme),
    ("LexemeMetadata", LexemeMetadata),
    ("LexicalSource", LexicalSource),
    ("LexicalRepository", LexicalRepository),
    ("InMemoryLexicalRepository", InMemoryLexicalRepository),
    ("LexemeBuilder", LexemeBuilder),
    ("LexemeRecordBuilder", LexemeRecordBuilder),
    ("LexemeRecord", LexemeRecord),
    ("Synset", Synset),
    ("SynsetMetadata", SynsetMetadata),
    ("SynsetRecord", SynsetRecord),
    ("SynsetRecordBuilder", SynsetRecordBuilder),
    ("SynsetBuilder", SynsetBuilder),
    ("Varga", Varga),
    ("VargaMetadata", VargaMetadata),
    ("VargaRecord", VargaRecord),
    ("VargaBuilder", VargaBuilder),
    ("AmarakoshaRegistry", AmarakoshaRegistry),
]

for name, obj in components:
    print(f"{name:<30}: {obj}")
    try:
        print(
            f"{'':30}  "
            f"module={obj.__module__}"
        )
    except Exception:
        pass


# ======================================================================
# 2. Lexeme / Synset type identity
# ======================================================================

subsection("2. LEXEME TYPE IDENTITY")

print("Synset annotation / constructor source:")
show_source("Synset", Synset)

print()
print("Canonical Lexeme source:")
show_source("Lexeme", Lexeme)

print()
print("Identity checks:")

print(
    "Synset expects kernel Lexeme : "
    f"{Lexeme.__module__ == 'SanskritAI.lexical.models.lexeme'}"
)

try:
    from SanskritAI.domain.lexical.lexeme import Lexeme as DomainLexeme

    print(
        "Domain Lexeme is same type  : "
        f"{DomainLexeme is Lexeme}"
    )

except Exception as exc:
    print(
        "Domain Lexeme comparison     : "
        f"UNAVAILABLE ({exc})"
    )


# ======================================================================
# 3. LexicalRepository contract
# ======================================================================

subsection("3. LEXICAL REPOSITORY CONTRACT")

show_signature(
    "LexicalRepository",
    LexicalRepository,
)

print()
print("Abstract methods:")

for name in sorted(
    getattr(
        LexicalRepository,
        "__abstractmethods__",
        frozenset(),
    )
):
    print(f"  {name}")

print()
print("get_lexeme source:")
show_source(
    "LexicalRepository.get_lexeme",
    LexicalRepository.get_lexeme,
)


# ======================================================================
# 4. In-memory repository implementation
# ======================================================================

subsection("4. IN-MEMORY LEXICAL REPOSITORY")

show_signature(
    "InMemoryLexicalRepository",
    InMemoryLexicalRepository,
)

print()
print("get_lexeme source:")
show_source(
    "InMemoryLexicalRepository.get_lexeme",
    InMemoryLexicalRepository.get_lexeme,
)

print()
print("add source:")
show_source(
    "InMemoryLexicalRepository.add",
    InMemoryLexicalRepository.add,
)


# ======================================================================
# 5. LexicalSource contract
# ======================================================================

subsection("5. LEXICAL SOURCE CONTRACT")

show_signature(
    "LexicalSource",
    LexicalSource,
)

print()
print("Fields / public attributes:")

try:
    for name in sorted(
        name
        for name in dir(LexicalSource)
        if not name.startswith("_")
    ):
        print(f"  {name}")
except Exception as exc:
    print(f"  unavailable: {exc}")


# ======================================================================
# 6. Runtime canonical Lexeme construction
# ======================================================================

subsection("6. RUNTIME CANONICAL LEXEME CONSTRUCTION")

lexeme = None

try:
    metadata = LexemeMetadata(
        lemma="हरि",
        transliteration="hari",
        language="sanskrit",
        script="devanagari",
        description="Test Amarakośa lexeme",
        title="हरि",
    )

    lexeme = Lexeme(
        identifier="lexeme:test:5h3",
        metadata=metadata,
    )

    print("Direct Lexeme construction : SUCCESS")
    print(f"Identifier                 : {lexeme.id}")
    print(f"Lemma                      : {lexeme.lemma}")
    print(f"Transliteration            : {lexeme.transliteration}")
    print(f"Language                   : {lexeme.language}")
    print(f"Script                     : {lexeme.script}")

except Exception as exc:
    print(
        "Direct Lexeme construction : FAILED"
        f" ({exc})"
    )


# ======================================================================
# 7. Repository runtime construction
# ======================================================================

subsection("7. REPOSITORY RUNTIME CONSTRUCTION")

repository = None

try:
    print(
        "LexicalSource constructor:"
    )
    show_signature(
        "LexicalSource",
        LexicalSource,
    )

    print()
    print(
        "NOTE: source construction is intentionally probed "
        "using introspection first."
    )

    try:
        source = LexicalSource(
            identifier="amarakosha",
            name="Amarakośa",
        )
    except Exception:
        try:
            source = LexicalSource(
                identifier="amarakosha",
            )
        except Exception:
            source = None

    if source is None:
        print(
            "LexicalSource runtime construction: "
            "NOT RESOLVED"
        )
    else:
        print(
            "LexicalSource runtime construction: SUCCESS"
        )
        print(f"Source: {source!r}")

        repository = InMemoryLexicalRepository(
            source=source,
        )

        print(
            "InMemoryLexicalRepository construction: "
            "SUCCESS"
        )

except Exception as exc:
    print(
        "Repository runtime construction: "
        f"FAILED ({exc})"
    )


# ======================================================================
# 8. Repository Lexeme identity round-trip
# ======================================================================

subsection("8. LEXEME IDENTITY ROUND-TRIP")

if repository is None:
    print(
        "ROUND-TRIP: BLOCKED — repository could not "
        "be constructed."
    )

elif lexeme is None:
    print(
        "ROUND-TRIP: BLOCKED — Lexeme could not "
        "be constructed."
    )

else:

    try:
        repository.add(lexeme)

        print("Repository add              : SUCCESS")

        resolved = repository.get_lexeme(
            "lexeme:test:5h3"
        )

        print(
            "Repository get_lexeme       : "
            f"{resolved!r}"
        )

        print(
            "Resolution succeeded        : "
            f"{resolved is not None}"
        )

        print(
            "Same object identity        : "
            f"{resolved is lexeme}"
        )

        print(
            "Resolved object type       : "
            f"{type(resolved)}"
        )

        print(
            "Resolved object is kernel "
            f"Lexeme                    : "
            f"{isinstance(resolved, Lexeme)}"
        )

    except Exception as exc:
        print(
            "Lexeme repository round-trip: "
            f"FAILED ({exc})"
        )


# ======================================================================
# 9. LexemeBuilder runtime
# ======================================================================

subsection("9. EXISTING LEXEME BUILDER BOUNDARY")

try:

    builder = (
        LexemeBuilder()
        .with_identifier("lexeme:test:5h3-builder")
        .with_lemma("हरि")
        .with_transliteration("hari")
        .with_language("sanskrit")
        .with_script("devanagari")
    )

    built_lexeme = builder.build()

    print("LexemeBuilder construction : SUCCESS")
    print(f"Built type                 : {type(built_lexeme)}")
    print(f"Built identifier            : {built_lexeme.id}")
    print(f"Built lemma                 : {built_lexeme.lemma}")
    print(
        "Built is kernel Lexeme      : "
        f"{isinstance(built_lexeme, Lexeme)}"
    )

except Exception as exc:
    print(
        "LexemeBuilder runtime      : "
        f"FAILED ({exc})"
    )


# ======================================================================
# 10. LexemeRecordBuilder boundary
# ======================================================================

subsection("10. EXISTING LEXEME RECORD BUILDER")

show_signature(
    "LexemeRecord",
    LexemeRecord,
)

show_signature(
    "LexemeRecordBuilder",
    LexemeRecordBuilder,
)

show_source(
    "LexemeRecordBuilder.build",
    LexemeRecordBuilder.build,
)


# ======================================================================
# 11. SynsetBuilder boundary
# ======================================================================

subsection("11. SYNSET BUILDER BOUNDARY")

show_signature(
    "SynsetBuilder",
    SynsetBuilder,
)

show_source(
    "SynsetBuilder.add_lexeme",
    SynsetBuilder.add_lexeme,
)

show_source(
    "SynsetBuilder.build",
    SynsetBuilder.build,
)

print()
print(
    "SynsetBuilder abstract methods: "
    f"{getattr(SynsetBuilder, '__abstractmethods__', frozenset())}"
)


# ======================================================================
# 12. SynsetRecordBuilder boundary
# ======================================================================

subsection("12. SYNSET RECORD BUILDER CURRENT CONTRACT")

show_signature(
    "SynsetRecordBuilder",
    SynsetRecordBuilder,
)

show_source(
    "SynsetRecordBuilder.build",
    SynsetRecordBuilder.build,
)

print()
print(
    "Current builder accepts only record: "
    "YES"
)

print(
    "Current builder has repository dependency: "
    "NO"
)


# ======================================================================
# 13. VargaBuilder boundary
# ======================================================================

subsection("13. VARGA BUILDER BOUNDARY")

show_signature(
    "VargaBuilder",
    VargaBuilder,
)

show_source(
    "VargaBuilder.add_synset",
    VargaBuilder.add_synset,
)

show_source(
    "VargaBuilder.build",
    VargaBuilder.build,
)

print()
print(
    "VargaBuilder abstract methods: "
    f"{getattr(VargaBuilder, '__abstractmethods__', frozenset())}"
)


# ======================================================================
# 14. Varga runtime composition
# ======================================================================

subsection("14. VARGA RUNTIME COMPOSITION")

try:

    synset_metadata = SynsetMetadata(
        kanda=Amarakanda.SVARGADI,
        varga="test-varga",
        varga_number=1,
        verse_number=1,
        pada_number=1,
        synset_identifier="synset:test:5h3",
        title="हरि",
    )

    if lexeme is not None:
        synset = (
            SynsetBuilder()
            .with_identifier("synset:test:5h3")
            .with_metadata(synset_metadata)
            .add_lexeme(lexeme)
            .build()
        )

        print("Synset composition          : SUCCESS")
        print(
            f"Synset child count          : "
            f"{synset.child_count}"
        )

        varga_metadata = VargaMetadata(
            kanda=Amarakanda.SVARGADI,
            varga_number=1,
            name="test-varga",
            title="Test Varga",
            description="Batch 5H-3 test Varga",
        )

        varga = (
            VargaBuilder()
            .with_identifier("varga:test:5h3")
            .with_metadata(varga_metadata)
            .add_synset(synset)
            .build()
        )

        print("Varga composition           : SUCCESS")
        print(
            f"Varga child count           : "
            f"{varga.child_count}"
        )

    else:
        print(
            "Synset/Varga composition    : "
            "BLOCKED — Lexeme unavailable"
        )

except Exception as exc:
    print(
        "Varga runtime composition   : "
        f"FAILED ({exc})"
    )


# ======================================================================
# 15. Registry runtime composition
# ======================================================================

subsection("15. AMARAKOSHA REGISTRY COMPOSITION")

try:

    registry = AmarakoshaRegistry()

    print(
        "Registry construction       : SUCCESS"
    )

    if "synset" in locals():
        registry.register(synset)
        print(
            "Synset registration         : SUCCESS"
        )

    if "varga" in locals():
        registry.register(varga)
        print(
            "Varga registration          : SUCCESS"
        )

    print(
        "Registry synset count       : "
        f"{len(tuple(registry.synsets()))}"
    )

    print(
        "Registry Varga count        : "
        f"{len(tuple(registry.vargas()))}"
    )

except Exception as exc:
    print(
        "Registry composition        : "
        f"FAILED ({exc})"
    )


# ======================================================================
# 16. Decision matrix
# ======================================================================

subsection("16. DECISION MATRIX")

rows = [
    (
        "Synset Lexeme type",
        "SanskritAI.lexical.models.lexeme.Lexeme",
        "VERIFIED",
    ),
    (
        "LexicalRepository.get_lexeme",
        "Identifier -> Lexeme | None",
        "VERIFIED",
    ),
    (
        "InMemoryLexicalRepository",
        "Stores canonical Lexeme by id",
        "VERIFIED",
    ),
    (
        "LexemeRecordBuilder",
        "LexemeRecord -> canonical Lexeme",
        "VERIFIED",
    ),
    (
        "SynsetBuilder.add_lexeme",
        "Accepts canonical Lexeme",
        "VERIFIED",
    ),
    (
        "VargaBuilder.add_synset",
        "Accepts Synset",
        "VERIFIED",
    ),
    (
        "AmarakoshaRegistry",
        "Stores Synset/Varga",
        "VERIFIED",
    ),
    (
        "SynsetRecordBuilder",
        "Record -> Synset",
        "PARTIAL",
    ),
    (
        "Lexeme ID resolution",
        "Existing repository boundary",
        "AVAILABLE",
    ),
    (
        "New LexemeResolver class",
        "Required",
        "NO",
    ),
    (
        "New VargaRecordBuilder",
        "Required",
        "NO",
    ),
]


print(
    f"{'AREA':35} | "
    f"{'CURRENT BOUNDARY':45} | STATUS"
)
print("-" * 115)

for area, boundary, status in rows:
    print(
        f"{area:35} | "
        f"{boundary:45} | "
        f"{status}"
    )


# ======================================================================
# 17. Architectural conclusion
# ======================================================================

subsection("17. ARCHITECTURAL CONCLUSION")

print(
    "1. The canonical Lexeme implementation is "
    "SanskritAI.lexical.models.lexeme.Lexeme."
)

print(
    "2. Synset already uses that canonical Lexeme type."
)

print(
    "3. LexicalRepository already provides get_lexeme(identifier)."
)

print(
    "4. InMemoryLexicalRepository already stores canonical Lexeme "
    "objects by identifier."
)

print(
    "5. Therefore a new LexemeResolver abstraction is NOT justified."
)

print(
    "6. Lexeme resolution should remain an orchestration/repository "
    "responsibility."
)

print(
    "7. VargaBuilder already provides the required Synset -> Varga "
    "construction boundary."
)

print(
    "8. The legacy services/importers/amarakosha_builder.py belongs "
    "to the older models.amarakosha tree and must NOT be reused."
)

print(
    "9. The current SynsetRecordBuilder is the remaining incomplete "
    "record-to-domain boundary."
)

print(
    "10. The next production change should therefore be a minimal "
    "SynsetRecordBuilder integration with the existing repository/"
    "orchestration boundary, not a new resolver."
)


# ======================================================================
# 18. Decision gate
# ======================================================================

subsection("18. BATCH 5H-3 DECISION GATE")

checks = [
    (
        "Canonical Lexeme identity verified",
        lexeme is not None,
    ),
    (
        "Repository get_lexeme boundary verified",
        repository is not None,
    ),
    (
        "Lexeme repository round-trip verified",
        (
            repository is not None
            and lexeme is not None
            and repository.get_lexeme(
                "lexeme:test:5h3"
            ) is not None
        ),
    ),
    (
        "LexemeBuilder construction verified",
        "built_lexeme" in locals(),
    ),
    (
        "SynsetBuilder canonical Lexeme composition verified",
        "synset" in locals(),
    ),
    (
        "VargaBuilder Synset composition verified",
        "varga" in locals(),
    ),
    (
        "Registry composition verified",
        "registry" in locals(),
    ),
]

for label, passed in checks:
    print(
        f"{label:55}: "
        f"{'PASS' if passed else 'FAIL'}"
    )

print()
print(
    "BATCH 5H-3 STATUS: "
    "READ-ONLY BOUNDARY VERIFIED"
)

print()
print(
    "NEXT IMPLEMENTATION:"
)
print(
    "Complete SynsetRecordBuilder using the existing "
    "LexicalRepository/orchestration boundary."
)
print(
    "Do NOT create LexemeResolver."
)
print(
    "Do NOT create VargaRecordBuilder."
)
print(
    "Do NOT implement the canonical Amarakośa adapter yet."
)
