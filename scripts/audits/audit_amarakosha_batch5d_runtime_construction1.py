from __future__ import annotations

import inspect
import sys
from dataclasses import fields
from pathlib import Path


ROOT = Path("/content/SanskritAI")

if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))


def section(title: str) -> None:
    print()
    print("=" * 118)
    print(title)
    print("=" * 118)


def report_object(label: str, obj: object) -> None:
    print(f"{label}:")
    print(f"  type       : {type(obj)}")
    print(f"  repr       : {obj!r}")


def report_class(label: str, cls: type) -> None:
    print(f"[{label}]")
    print(f"  class      : {cls}")
    print(f"  module     : {cls.__module__}")
    print(f"  qualname   : {cls.__qualname__}")
    print(f"  abstract   : {inspect.isabstract(cls)}")
    print(
        "  abstract methods:",
        sorted(getattr(cls, "__abstractmethods__", set())),
    )

    print("  MRO:")
    for index, item in enumerate(cls.__mro__):
        print(f"    {index}: {item}")


def report_source(label: str, obj: object, max_lines: int = 100) -> None:
    print(f"\n[{label}]")

    try:
        source = inspect.getsource(obj)
    except (OSError, TypeError):
        print("  <SOURCE UNAVAILABLE>")
        return

    lines = source.splitlines()

    for line in lines[:max_lines]:
        print(f"  {line}")

    if len(lines) > max_lines:
        print(f"  ... ({len(lines) - max_lines} additional lines omitted)")


def report_signature(label: str, obj: object) -> None:
    print(f"{label}:")
    try:
        print(f"  {inspect.signature(obj)}")
    except (TypeError, ValueError):
        print("  <SIGNATURE UNAVAILABLE>")


def report_dataclass(label: str, cls: type) -> None:
    print(f"\n[{label} dataclass fields]")

    try:
        for field in fields(cls):
            print(
                f"  {field.name}: "
                f"type={field.type!r}, "
                f"default={field.default!r}"
            )
    except TypeError:
        print("  <NOT A DATACLASS>")


section("BATCH 5D — AMARAKOSHA RUNTIME CONSTRUCTION PROBE")

print(f"Repository root : {ROOT}")
print("Probe mode       : READ-ONLY")
print("Purpose          : verify existing runtime construction contracts")
print()


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

section("1. IMPORT EXISTING AMARAKOSHA COMPONENTS")

try:
    from SanskritAI.amarakosha.builders.base_amarakosha_builder import (
        BaseAmarakoshaBuilder,
    )
    from SanskritAI.amarakosha.builders.base_knowledge_record_builder import (
        BaseKnowledgeRecordBuilder,
    )
    from SanskritAI.amarakosha.builders.synset_builder import SynsetBuilder
    from SanskritAI.amarakosha.builders.varga_builder import VargaBuilder
    from SanskritAI.amarakosha.builders.synset_record_builder import (
        SynsetRecordBuilder,
    )

    from SanskritAI.amarakosha.models.synset import Synset
    from SanskritAI.amarakosha.models.varga import Varga
    from SanskritAI.amarakosha.models.synset_metadata import SynsetMetadata
    from SanskritAI.amarakosha.models.varga_metadata import VargaMetadata

    from SanskritAI.amarakosha.records.synset_record import SynsetRecord
    from SanskritAI.amarakosha.records.varga_record import VargaRecord

    from SanskritAI.amarakosha.registries.amarakosha_registry import (
        AmarakoshaRegistry,
    )

    from SanskritAI.acquisition.knowledge.models.lexeme import (
        Lexeme,
        LexemeMetadata,
    )

    from SanskritAI.amarakosha.enums.Amarakanda import Amarakanda

    print("All target imports: SUCCESS")

except Exception as exc:
    print("IMPORT FAILURE:")
    print(f"  {type(exc).__name__}: {exc}")
    raise


# ---------------------------------------------------------------------------
# 2. Base builder contract
# ---------------------------------------------------------------------------

section("2. BASE AMARAKOSHA BUILDER CONTRACT")

report_class("BaseAmarakoshaBuilder", BaseAmarakoshaBuilder)
report_signature(
    "BaseAmarakoshaBuilder.__init__",
    BaseAmarakoshaBuilder.__init__,
)
report_signature(
    "BaseAmarakoshaBuilder._create_instance",
    BaseAmarakoshaBuilder._create_instance,
)
report_signature(
    "BaseAmarakoshaBuilder.build",
    BaseAmarakoshaBuilder.build,
)

report_source(
    "BaseAmarakoshaBuilder._create_instance",
    BaseAmarakoshaBuilder._create_instance,
)

report_source(
    "BaseAmarakoshaBuilder.build",
    BaseAmarakoshaBuilder.build,
)


# ---------------------------------------------------------------------------
# 3. Concrete builder construction
# ---------------------------------------------------------------------------

section("3. SYNSET BUILDER CONSTRUCTION")

report_class("SynsetBuilder", SynsetBuilder)
report_signature("SynsetBuilder.__init__", SynsetBuilder.__init__)

try:
    synset_builder = SynsetBuilder()
    print("SynsetBuilder(): SUCCESS")
    report_object("instance", synset_builder)
except Exception as exc:
    synset_builder = None
    print("SynsetBuilder(): FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


section("4. VARGA BUILDER CONSTRUCTION")

report_class("VargaBuilder", VargaBuilder)
report_signature("VargaBuilder.__init__", VargaBuilder.__init__)

try:
    varga_builder = VargaBuilder()
    print("VargaBuilder(): SUCCESS")
    report_object("instance", varga_builder)
except Exception as exc:
    varga_builder = None
    print("VargaBuilder(): FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


section("5. SYNSET RECORD BUILDER CONSTRUCTION")

report_class("SynsetRecordBuilder", SynsetRecordBuilder)
report_signature(
    "SynsetRecordBuilder.__init__",
    SynsetRecordBuilder.__init__,
)

try:
    synset_record_builder = SynsetRecordBuilder()
    print("SynsetRecordBuilder(): SUCCESS")
    report_object("instance", synset_record_builder)
except Exception as exc:
    synset_record_builder = None
    print("SynsetRecordBuilder(): FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------
# 4. Domain construction
# ---------------------------------------------------------------------------

section("6. LEXEME CONSTRUCTION")

report_class("Lexeme", Lexeme)
report_dataclass("LexemeMetadata", LexemeMetadata)

try:
    lexeme_metadata = LexemeMetadata(
        lemma="हरि",
        transliteration="hari",
        language="sanskrit",
        script="devanagari",
    )

    lexeme = Lexeme(
        identifier="amarakosha:lexeme:hari",
        metadata=lexeme_metadata,
    )

    print("Lexeme construction: SUCCESS")
    report_object("LexemeMetadata", lexeme_metadata)
    report_object("Lexeme", lexeme)

except Exception as exc:
    lexeme = None
    print("Lexeme construction: FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------
# 5. Synset construction directly
# ---------------------------------------------------------------------------

section("7. SYNSET DIRECT CONSTRUCTION")

report_class("Synset", Synset)
report_dataclass("SynsetMetadata", SynsetMetadata)

try:
    synset_metadata = SynsetMetadata(
        lemma="हरि",
        transliteration="hari",
        language="sanskrit",
        script="devanagari",
        kanda=Amarakanda.SVARGADI,
        varga="example",
        verse_number=1,
        synset_identifier="amarakosha:synset:hari",
    )

    children = [lexeme] if lexeme is not None else []

    synset = Synset(
        identifier="amarakosha:synset:hari",
        metadata=synset_metadata,
        children=children,
    )

    print("Direct Synset construction: SUCCESS")
    report_object("SynsetMetadata", synset_metadata)
    report_object("Synset", synset)

except Exception as exc:
    synset = None
    print("Direct Synset construction: FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------
# 6. Varga construction directly
# ---------------------------------------------------------------------------

section("8. VARGA DIRECT CONSTRUCTION")

report_class("Varga", Varga)
report_dataclass("VargaMetadata", VargaMetadata)

try:
    varga_metadata = VargaMetadata(
        kanda=Amarakanda.SVARGADI,
        varga_number=1,
        name="example",
        title="Example Varga",
        devanagari="उदाहरण",
        iast="udāharaṇa",
        transliteration="udaharana",
        description="Runtime probe",
    )

    children = [synset] if synset is not None else []

    varga = Varga(
        identifier="amarakosha:varga:example",
        metadata=varga_metadata,
        children=children,
    )

    print("Direct Varga construction: SUCCESS")
    report_object("VargaMetadata", varga_metadata)
    report_object("Varga", varga)

except Exception as exc:
    varga = None
    print("Direct Varga construction: FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------
# 7. Builder internal state
# ---------------------------------------------------------------------------

section("9. BUILDER INTERNAL STATE")

if synset_builder is not None:
    print("[SynsetBuilder instance state]")
    print(f"  __dict__ = {getattr(synset_builder, '__dict__', '<NO __dict__>')}")

    for name in (
        "_identifier",
        "_metadata",
        "_lexemes",
        "_instance",
    ):
        if hasattr(synset_builder, name):
            print(f"  {name} = {getattr(synset_builder, name)!r}")

if varga_builder is not None:
    print("\n[VargaBuilder instance state]")
    print(f"  __dict__ = {getattr(varga_builder, '__dict__', '<NO __dict__>')}")

    for name in (
        "_identifier",
        "_metadata",
        "_synsets",
        "_instance",
    ):
        if hasattr(varga_builder, name):
            print(f"  {name} = {getattr(varga_builder, name)!r}")


# ---------------------------------------------------------------------------
# 8. Builder methods vs abstract contract
# ---------------------------------------------------------------------------

section("10. BUILDER METHOD / ABSTRACT CONTRACT COMPARISON")

for label, cls in (
    ("SynsetBuilder", SynsetBuilder),
    ("VargaBuilder", VargaBuilder),
):
    print(f"\n[{label}]")

    for method_name in (
        "__init__",
        "_create_instance",
        "build",
        "validate",
        "reset",
        "instance",
        "from_instance",
        "clone",
    ):
        method = getattr(cls, method_name, None)

        if method is None:
            print(f"  {method_name}: MISSING")
            continue

        print(f"  {method_name}:")
        try:
            print(f"    owner: {method.__qualname__}")
        except Exception:
            pass

        try:
            print(f"    signature: {inspect.signature(method)}")
        except (TypeError, ValueError):
            print("    signature: <UNAVAILABLE>")


# ---------------------------------------------------------------------------
# 9. Attempt existing fluent construction if possible
# ---------------------------------------------------------------------------

section("11. EXISTING FLUENT BUILDER CONSTRUCTION PROBE")

if synset_builder is None:
    print("SynsetBuilder unavailable; fluent probe skipped.")
else:
    try:
        result = (
            synset_builder
            .with_identifier("amarakosha:synset:hari")
            .with_metadata(
                SynsetMetadata(
                    lemma="हरि",
                    transliteration="hari",
                    kanda=Amarakanda.SVARGADI,
                    varga="example",
                    verse_number=1,
                    synset_identifier="amarakosha:synset:hari",
                )
            )
        )

        if lexeme is not None:
            result.add_lexeme(lexeme)

        print("Fluent configuration: SUCCESS")
        print(f"  builder object: {result!r}")

        try:
            built = result.build()
            print("builder.build(): SUCCESS")
            report_object("built object", built)
        except Exception as exc:
            print("builder.build(): FAILURE")
            print(f"  {type(exc).__name__}: {exc}")

    except Exception as exc:
        print("Fluent configuration: FAILURE")
        print(f"  {type(exc).__name__}: {exc}")


if varga_builder is None:
    print("\nVargaBuilder unavailable; fluent probe skipped.")
else:
    try:
        result = (
            varga_builder
            .with_identifier("amarakosha:varga:example")
            .with_metadata(
                VargaMetadata(
                    kanda=Amarakanda.SVARGADI,
                    varga_number=1,
                    name="example",
                    title="Example Varga",
                )
            )
        )

        if synset is not None:
            result.add_synset(synset)

        print("\nVarga fluent configuration: SUCCESS")

        try:
            built = result.build()
            print("Varga builder.build(): SUCCESS")
            report_object("built object", built)
        except Exception as exc:
            print("Varga builder.build(): FAILURE")
            print(f"  {type(exc).__name__}: {exc}")

    except Exception as exc:
        print("Varga fluent configuration: FAILURE")
        print(f"  {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------
# 10. Registry construction and registration
# ---------------------------------------------------------------------------

section("12. AMARAKOSHA REGISTRY PROBE")

report_class("AmarakoshaRegistry", AmarakoshaRegistry)

try:
    registry = AmarakoshaRegistry()
    print("AmarakoshaRegistry(): SUCCESS")
    report_object("registry", registry)

except Exception as exc:
    registry = None
    print("AmarakoshaRegistry(): FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


if registry is not None:

    if synset is not None:
        try:
            registry.add(synset)
            print("registry.add(Synset): SUCCESS")
            print(f"  exists = {registry.exists(synset.identifier)}")
            print(f"  get    = {registry.get(synset.identifier)!r}")
        except Exception as exc:
            print("registry.add(Synset): FAILURE")
            print(f"  {type(exc).__name__}: {exc}")

    if varga is not None:
        try:
            registry.add(varga)
            print("registry.add(Varga): SUCCESS")
            print(f"  exists = {registry.exists(varga.identifier)}")
            print(f"  get    = {registry.get(varga.identifier)!r}")
        except Exception as exc:
            print("registry.add(Varga): FAILURE")
            print(f"  {type(exc).__name__}: {exc}")

    print("\nRegistry contents:")

    try:
        for identifier, obj in registry.items():
            print(f"  {identifier!r} -> {type(obj).__name__}")
    except Exception as exc:
        print("  registry.items() failure:")
        print(f"    {type(exc).__name__}: {exc}")

    try:
        print(
            "  synsets:",
            [obj.identifier for obj in registry.synsets()],
        )
    except Exception as exc:
        print("  synsets() failure:", exc)

    try:
        print(
            "  vargas:",
            [obj.identifier for obj in registry.vargas()],
        )
    except Exception as exc:
        print("  vargas() failure:", exc)


# ---------------------------------------------------------------------------
# 11. Record construction
# ---------------------------------------------------------------------------

section("13. SYNSET RECORD CONSTRUCTION")

try:
    synset_record = SynsetRecord(
        identifier="amarakosha:synset:hari",
        source="amarakosha",
        source_identifier="amarakosha:synset:hari",
        source_version="1.0",
        kanda=Amarakanda.SVARGADI,
        varga="example",
        verse=1,
        sequence=1,
        devanagari="हरि",
        iast="hari",
        transliteration="hari",
        gloss="Vishnu",
        lexeme_ids=("amarakosha:lexeme:hari",),
        tags=("probe",),
        notes="Runtime construction probe",
    )

    print("SynsetRecord construction: SUCCESS")
    report_object("SynsetRecord", synset_record)

except Exception as exc:
    synset_record = None
    print("SynsetRecord construction: FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


section("14. VARGA RECORD CONSTRUCTION")

try:
    varga_record = VargaRecord(
        identifier="amarakosha:varga:example",
        source="amarakosha",
        source_identifier="amarakosha:varga:example",
        source_version="1.0",
        kanda=Amarakanda.SVARGADI,
        varga_number=1,
        name="example",
        title="Example Varga",
        devanagari="उदाहरण",
        iast="udāharaṇa",
        transliteration="udaharana",
        description="Runtime construction probe",
        tags=("probe",),
        notes="Runtime construction probe",
    )

    print("VargaRecord construction: SUCCESS")
    report_object("VargaRecord", varga_record)

except Exception as exc:
    varga_record = None
    print("VargaRecord construction: FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------
# 12. Record builder probe
# ---------------------------------------------------------------------------

section("15. SYNSET RECORD BUILDER PROBE")

if synset_record_builder is None:
    print("SynsetRecordBuilder unavailable.")
else:
    report_source(
        "SynsetRecordBuilder",
        SynsetRecordBuilder,
        max_lines=180,
    )

    if synset_record is not None:
        print("\nAttempting record-builder construction...")

        for method_name in (
            "with_identifier",
            "with_source",
            "with_source_identifier",
            "with_source_version",
            "with_kanda",
            "with_varga",
            "with_verse",
            "with_sequence",
            "with_devanagari",
            "with_iast",
            "with_transliteration",
            "with_gloss",
            "add_lexeme_id",
        ):
            method = getattr(synset_record_builder, method_name, None)

            if method is None:
                continue

            print(f"  available method: {method_name}{inspect.signature(method)}")


# ---------------------------------------------------------------------------
# 13. Final evidence summary
# ---------------------------------------------------------------------------

section("16. BATCH 5D EVIDENCE SUMMARY")

print("Construction results:")

print(
    "  SynsetBuilder instantiable :",
    synset_builder is not None,
)

print(
    "  VargaBuilder instantiable  :",
    varga_builder is not None,
)

print(
    "  SynsetRecordBuilder        :",
    synset_record_builder is not None,
)

print(
    "  Lexeme construction        :",
    lexeme is not None,
)

print(
    "  Direct Synset construction :",
    synset is not None,
)

print(
    "  Direct Varga construction  :",
    varga is not None,
)

print(
    "  Registry construction      :",
    registry is not None,
)

print(
    "  SynsetRecord construction  :",
    synset_record is not None,
)

print(
    "  VargaRecord construction   :",
    varga_record is not None,
)


section("17. BATCH 5D DECISION GATE")

print(
    """
This probe is READ-ONLY.

Interpretation rules:

1. Do not implement _create_instance() merely because it is abstract.
2. First determine whether BaseAmarakoshaBuilder's abstraction is
   semantically required or is a stale/misaligned inherited contract.
3. Do not create a second builder abstraction.
4. Do not bypass Synset/Varga and construct canonical objects directly.
5. If direct Synset/Varga construction succeeds while builder construction
   fails, record the builder-contract mismatch explicitly.
6. If Lexeme construction succeeds, inspect how lexeme identifiers can be
   resolved from SynsetRecord.lexeme_ids.
7. If registry registration succeeds, retain AmarakoshaRegistry as the
   Amarakośa domain registration boundary.
8. Record → builder feasibility must be determined from existing APIs,
   not invented setters or fields.
"""
)

print("BATCH 5D COMPLETE")
print("=" * 118)
