
from __future__ import annotations

import inspect
from pathlib import Path

from SanskritAI.amarakosha.importers.amarakosha_importer import (
    AmarakoshaImporter,
)
from SanskritAI.amarakosha.builders.synset_record_builder import (
    SynsetRecordBuilder,
)
from SanskritAI.amarakosha.builders.varga_builder import (
    VargaBuilder,
)
from SanskritAI.amarakosha.registries.amarakosha_registry import (
    AmarakoshaRegistry,
)
from SanskritAI.amarakosha.parsers.amarakosha_parser import (
    AmarakoshaParser,
)


print("=" * 115)
print("BATCH 5H-5A — AMARAKOSHA IMPORTER / ORCHESTRATION BOUNDARY AUDIT")
print("=" * 115)

# ----------------------------------------------------------------------
# 1. Component resolution
# ----------------------------------------------------------------------

print("\n1. COMPONENT RESOLUTION")
print("-" * 115)

components = {
    "AmarakoshaImporter": AmarakoshaImporter,
    "AmarakoshaParser": AmarakoshaParser,
    "AmarakoshaRegistry": AmarakoshaRegistry,
    "SynsetRecordBuilder": SynsetRecordBuilder,
    "VargaBuilder": VargaBuilder,
}

for name, component in components.items():
    print(f"{name:<28}: {component}")
    print(f"{'module':<28}: {component.__module__}")


# ----------------------------------------------------------------------
# 2. Importer MRO and constructor
# ----------------------------------------------------------------------

print("\n2. IMPORTER CLASS CONTRACT")
print("-" * 115)

print("MRO:")
for cls in inspect.getmro(AmarakoshaImporter):
    print("  ", cls)

print("\nConstructor:")
print(inspect.signature(AmarakoshaImporter))

print("\nConstructor source:")
print(inspect.getsource(AmarakoshaImporter.__init__))


# ----------------------------------------------------------------------
# 3. Importer complete source
# ----------------------------------------------------------------------

print("\n3. COMPLETE IMPORTER SOURCE")
print("-" * 115)

print(inspect.getsource(AmarakoshaImporter))


# ----------------------------------------------------------------------
# 4. Importer public methods
# ----------------------------------------------------------------------

print("\n4. IMPORTER PUBLIC METHODS")
print("-" * 115)

for name in sorted(
    name
    for name in dir(AmarakoshaImporter)
    if not name.startswith("_")
):
    try:
        attribute = getattr(AmarakoshaImporter, name)

        if callable(attribute):
            try:
                print(f"  {name}{inspect.signature(attribute)}")
            except (TypeError, ValueError):
                print(f"  {name}")
        else:
            print(f"  {name}")

    except Exception as exc:
        print(f"  {name} [inspection failed: {exc}]")


# ----------------------------------------------------------------------
# 5. Existing parser boundary
# ----------------------------------------------------------------------

print("\n5. PARSER BOUNDARY")
print("-" * 115)

print("AmarakoshaParser:")
print(inspect.signature(AmarakoshaParser))

print("\nParser public methods:")
for name in sorted(
    name
    for name in dir(AmarakoshaParser)
    if not name.startswith("_")
):
    try:
        attribute = getattr(AmarakoshaParser, name)

        if callable(attribute):
            try:
                print(f"  {name}{inspect.signature(attribute)}")
            except (TypeError, ValueError):
                print(f"  {name}")
        else:
            print(f"  {name}")

    except Exception:
        print(f"  {name}")


# ----------------------------------------------------------------------
# 6. Registry contract
# ----------------------------------------------------------------------

print("\n6. REGISTRY CONTRACT")
print("-" * 115)

registry = AmarakoshaRegistry()

print("Registry construction : SUCCESS")
print("Registry methods:")

for name in sorted(
    name
    for name in dir(registry)
    if not name.startswith("_")
):
    try:
        attribute = getattr(registry, name)

        if callable(attribute):
            try:
                print(f"  {name}{inspect.signature(attribute)}")
            except (TypeError, ValueError):
                print(f"  {name}")
        else:
            print(f"  {name}")

    except Exception:
        print(f"  {name}")


# ----------------------------------------------------------------------
# 7. Builder boundaries
# ----------------------------------------------------------------------

print("\n7. BUILDER BOUNDARIES")
print("-" * 115)

print("SynsetRecordBuilder:")
print("  ", inspect.signature(SynsetRecordBuilder))
print("  build:", inspect.signature(SynsetRecordBuilder.build))
print("  with_lexemes:",
      inspect.signature(SynsetRecordBuilder.with_lexemes))

print("\nVargaBuilder:")
print("  ", inspect.signature(VargaBuilder))
print("  build:", inspect.signature(VargaBuilder.build))
print("  add_synset:",
      inspect.signature(VargaBuilder.add_synset))


# ----------------------------------------------------------------------
# 8. Repository references in importer
# ----------------------------------------------------------------------

print("\n8. IMPORTER REPOSITORY DEPENDENCY")
print("-" * 115)

source_file = Path(
    inspect.getsourcefile(AmarakoshaImporter)
)

print("Importer source file:")
print(" ", source_file)

source_text = source_file.read_text(
    encoding="utf-8"
)

print("\nRepository-related textual references:")

for line_number, line in enumerate(
    source_text.splitlines(),
    start=1,
):
    lowered = line.lower()

    if (
        "repository" in lowered
        or "get_lexeme" in lowered
        or "lexeme_id" in lowered
    ):
        print(
            f"  L{line_number}: {line.rstrip()}"
        )


# ----------------------------------------------------------------------
# 9. Existing construction dependencies
# ----------------------------------------------------------------------

print("\n9. IMPORTER CONSTRUCTION DEPENDENCIES")
print("-" * 115)

try:
    parser = AmarakoshaParser()
    registry = AmarakoshaRegistry()

    importer = AmarakoshaImporter(
        parser=parser,
        registry=registry,
    )

    print("Current importer construction : SUCCESS")
    print("Importer instance             :", importer)

except Exception as exc:
    print("Current importer construction : FAILED")
    print("Exception                     :", repr(exc))


# ----------------------------------------------------------------------
# 10. Importer instance state
# ----------------------------------------------------------------------

print("\n10. IMPORTER INSTANCE STATE")
print("-" * 115)

try:
    print("Instance __dict__:")

    for key, value in vars(importer).items():
        print(
            f"  {key:<25}: "
            f"{type(value)} = {value!r}"
        )

except Exception as exc:
    print(
        "Instance state inspection failed:",
        repr(exc),
    )


# ----------------------------------------------------------------------
# 11. Decision questions
# ----------------------------------------------------------------------

print("\n11. BATCH 5H-5A DECISION QUESTIONS")
print("-" * 115)

print(
    "Q1. Does AmarakoshaImporter already own the "
    "record → domain orchestration?"
)

print(
    "Q2. Does the importer already accept or expose "
    "a dependency-injection boundary suitable for "
    "LexicalRepository?"
)

print(
    "Q3. Does the importer already resolve "
    "SynsetRecord.lexeme_ids?"
)

print(
    "Q4. Does the importer already construct "
    "Synset/Varga through the existing builders?"
)

print(
    "Q5. Can repository resolution be added to the "
    "existing importer without creating another "
    "orchestration abstraction?"
)

print(
    "Q6. Where should missing Lexeme identifiers "
    "be detected and reported?"
)

print(
    "Q7. Does the current importer process "
    "SynsetRecord and VargaRecord separately?"
)


# ----------------------------------------------------------------------
# 12. Gate
# ----------------------------------------------------------------------

print("\n12. BATCH 5H-5A STATUS")
print("-" * 115)

print(
    "READ-ONLY IMPORTER BOUNDARY AUDIT COMPLETE"
)

print("=" * 115)
