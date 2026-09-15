from __future__ import annotations

import importlib
import inspect
import re
import sys
from dataclasses import fields
from pathlib import Path
from typing import Any


ROOT = Path("/content/SanskritAI")

if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))


# ============================================================================
# PRODUCTION FILE FILTER
# ============================================================================

HISTORICAL_SUFFIX_RE = re.compile(
    r"(?:\d+|_G\d+)$"
)


def is_production_python_file(path: Path) -> bool:
    """
    Include only active production Python files.

    Excludes:
      - tests
      - __pycache__
      - files ending in numeric suffixes such as foo1.py / foo2.py
      - files ending in _G<number>.py
    """

    if path.suffix != ".py":
        return False

    parts = {part.lower() for part in path.parts}

    if "tests" in parts:
        return False

    if "__pycache__" in parts:
        return False

    stem = path.stem

    if HISTORICAL_SUFFIX_RE.search(stem):
        return False

    return True


# ============================================================================
# HELPERS
# ============================================================================

def section(title: str) -> None:
    print()
    print("=" * 118)
    print(title)
    print("=" * 118)


def report_object(label: str, obj: object) -> None:
    print(f"{label}:")
    print(f"  type : {type(obj)}")
    print(f"  repr : {obj!r}")


def report_class(label: str, cls: type) -> None:
    print(f"[{label}]")
    print(f"  class    : {cls}")
    print(f"  module   : {cls.__module__}")
    print(f"  qualname : {cls.__qualname__}")
    print(f"  abstract : {inspect.isabstract(cls)}")
    print(
        "  abstract methods:",
        sorted(getattr(cls, "__abstractmethods__", set())),
    )

    print("  MRO:")
    for index, item in enumerate(cls.__mro__):
        print(f"    {index}: {item}")


def report_signature(label: str, obj: object) -> None:
    print(f"{label}:")

    try:
        print(f"  {inspect.signature(obj)}")
    except (TypeError, ValueError):
        print("  <SIGNATURE UNAVAILABLE>")


def report_source(
    label: str,
    obj: object,
    max_lines: int = 120,
) -> None:
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
        print(
            f"  ... ({len(lines) - max_lines} additional lines omitted)"
        )


def report_dataclass(
    label: str,
    cls: type,
) -> None:
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


def safe_import(module_name: str) -> Any | None:
    try:
        return importlib.import_module(module_name)
    except Exception as exc:
        print(
            f"  import failed: {module_name} "
            f"-> {type(exc).__name__}: {exc}"
        )
        return None


def module_name_from_path(path: Path) -> str | None:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return None

    parts = list(relative.with_suffix("").parts)

    if not parts:
        return None

    if parts[-1] == "__init__":
        parts = parts[:-1]

    if not parts:
        return None

    return "SanskritAI." + ".".join(parts)


# ============================================================================
# DYNAMIC LEXEME DISCOVERY
# ============================================================================

def discover_lexeme_classes() -> tuple[type | None, type | None]:
    """
    Discover the existing Lexeme and LexemeMetadata classes from the
    production source tree.

    No new classes are created.

    Discovery is based on active production files only.
    """

    section("2. EXISTING LEXEME OWNERSHIP DISCOVERY")

    candidates: list[Path] = []

    for path in ROOT.rglob("*.py"):
        if not is_production_python_file(path):
            continue

        if path.stem.lower() == "lexeme":
            candidates.append(path)

    candidates.sort()

    print("Candidate production lexeme.py files:")

    if not candidates:
        print("  NONE FOUND")

    for path in candidates:
        print(f"  {path}")

    lexeme_cls: type | None = None
    metadata_cls: type | None = None

    for path in candidates:
        module_name = module_name_from_path(path)

        if not module_name:
            continue

        print()
        print(f"Inspecting module: {module_name}")

        module = safe_import(module_name)

        if module is None:
            continue

        candidate_lexeme = getattr(module, "Lexeme", None)
        candidate_metadata = getattr(
            module,
            "LexemeMetadata",
            None,
        )

        if inspect.isclass(candidate_lexeme):
            lexeme_cls = candidate_lexeme
            print(
                "  Lexeme found:",
                f"{candidate_lexeme.__module__}."
                f"{candidate_lexeme.__qualname__}",
            )

        if inspect.isclass(candidate_metadata):
            metadata_cls = candidate_metadata
            print(
                "  LexemeMetadata found:",
                f"{candidate_metadata.__module__}."
                f"{candidate_metadata.__qualname__}",
            )

        if lexeme_cls is not None:
            break

    # ------------------------------------------------------------------------
    # Fallback: search imported production modules for the class definitions.
    # This handles cases where Lexeme lives in a differently named module.
    # ------------------------------------------------------------------------

    if lexeme_cls is None:
        print()
        print(
            "No Lexeme class found in lexeme.py. "
            "Searching production modules by source text..."
        )

        for path in ROOT.rglob("*.py"):
            if not is_production_python_file(path):
                continue

            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue

            if not re.search(
                r"class\s+Lexeme\b",
                text,
            ):
                continue

            module_name = module_name_from_path(path)

            if not module_name:
                continue

            print(f"  Possible Lexeme definition: {path}")
            print(f"  module: {module_name}")

            module = safe_import(module_name)

            if module is None:
                continue

            candidate_lexeme = getattr(
                module,
                "Lexeme",
                None,
            )

            candidate_metadata = getattr(
                module,
                "LexemeMetadata",
                None,
            )

            if inspect.isclass(candidate_lexeme):
                lexeme_cls = candidate_lexeme

            if inspect.isclass(candidate_metadata):
                metadata_cls = candidate_metadata

            if lexeme_cls is not None:
                break

    print()
    print("FINAL DISCOVERY RESULT")

    if lexeme_cls is not None:
        print(
            "  Lexeme owner:",
            f"{lexeme_cls.__module__}."
            f"{lexeme_cls.__qualname__}",
        )
    else:
        print("  Lexeme owner: NOT FOUND")

    if metadata_cls is not None:
        print(
            "  LexemeMetadata owner:",
            f"{metadata_cls.__module__}."
            f"{metadata_cls.__qualname__}",
        )
    else:
        print("  LexemeMetadata owner: NOT FOUND")

    return lexeme_cls, metadata_cls


# ============================================================================
# MAIN
# ============================================================================

section("BATCH 5D — AMARAKOSHA RUNTIME CONSTRUCTION PROBE")

print(f"Repository root : {ROOT}")
print("Probe mode      : READ-ONLY")
print("Purpose         : verify existing runtime construction contracts")
print()
print(
    "Production-file filter:"
    " tests excluded,"
    " __pycache__ excluded,"
    " numeric historical suffixes excluded,"
    " _G<number> files excluded."
)


# ============================================================================
# 1. IMPORT AMARAKOSHA COMPONENTS
# ============================================================================

section("1. IMPORT EXISTING AMARAKOSHA COMPONENTS")

try:
    from SanskritAI.amarakosha.builders.base_amarakosha_builder import (
        BaseAmarakoshaBuilder,
    )
    from SanskritAI.amarakosha.builders.base_knowledge_record_builder import (
        BaseKnowledgeRecordBuilder,
    )
    from SanskritAI.amarakosha.builders.synset_builder import (
        SynsetBuilder,
    )
    from SanskritAI.amarakosha.builders.varga_builder import (
        VargaBuilder,
    )
    from SanskritAI.amarakosha.builders.synset_record_builder import (
        SynsetRecordBuilder,
    )

    from SanskritAI.amarakosha.models.synset import Synset
    from SanskritAI.amarakosha.models.varga import Varga
    from SanskritAI.amarakosha.models.synset_metadata import (
        SynsetMetadata,
    )
    from SanskritAI.amarakosha.models.varga_metadata import (
        VargaMetadata,
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

    from SanskritAI.amarakosha.enums.Amarakanda import (
        Amarakanda,
    )

    print("All Amarakośa target imports: SUCCESS")

except Exception as exc:
    print("AMARAKOSHA IMPORT FAILURE:")
    print(f"  {type(exc).__name__}: {exc}")
    raise


# ============================================================================
# 2. DISCOVER EXISTING LEXEME OWNERSHIP
# ============================================================================

Lexeme, LexemeMetadata = discover_lexeme_classes()


# ============================================================================
# 3. BASE BUILDER CONTRACT
# ============================================================================

section("3. BASE AMARAKOSHA BUILDER CONTRACT")

report_class(
    "BaseAmarakoshaBuilder",
    BaseAmarakoshaBuilder,
)

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


# ============================================================================
# 4. SYNSET BUILDER
# ============================================================================

section("4. SYNSET BUILDER")

report_class(
    "SynsetBuilder",
    SynsetBuilder,
)

report_signature(
    "SynsetBuilder.__init__",
    SynsetBuilder.__init__,
)

report_source(
    "SynsetBuilder",
    SynsetBuilder,
    max_lines=180,
)

try:
    synset_builder = SynsetBuilder()

    print()
    print("SynsetBuilder(): SUCCESS")
    report_object(
        "SynsetBuilder instance",
        synset_builder,
    )

except Exception as exc:
    synset_builder = None

    print()
    print("SynsetBuilder(): FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


# ============================================================================
# 5. VARGA BUILDER
# ============================================================================

section("5. VARGA BUILDER")

report_class(
    "VargaBuilder",
    VargaBuilder,
)

report_signature(
    "VargaBuilder.__init__",
    VargaBuilder.__init__,
)

report_source(
    "VargaBuilder",
    VargaBuilder,
    max_lines=180,
)

try:
    varga_builder = VargaBuilder()

    print()
    print("VargaBuilder(): SUCCESS")
    report_object(
        "VargaBuilder instance",
        varga_builder,
    )

except Exception as exc:
    varga_builder = None

    print()
    print("VargaBuilder(): FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


# ============================================================================
# 6. SYNSET RECORD BUILDER
# ============================================================================

section("6. SYNSET RECORD BUILDER")

report_class(
    "SynsetRecordBuilder",
    SynsetRecordBuilder,
)

report_signature(
    "SynsetRecordBuilder.__init__",
    SynsetRecordBuilder.__init__,
)

report_source(
    "SynsetRecordBuilder",
    SynsetRecordBuilder,
    max_lines=220,
)

try:
    synset_record_builder = SynsetRecordBuilder()

    print()
    print("SynsetRecordBuilder(): SUCCESS")
    report_object(
        "SynsetRecordBuilder instance",
        synset_record_builder,
    )

except Exception as exc:
    synset_record_builder = None

    print()
    print("SynsetRecordBuilder(): FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


# ============================================================================
# 7. LEXEME CONSTRUCTION
# ============================================================================

section("7. LEXEME CONSTRUCTION")

if Lexeme is None:
    print(
        "Lexeme class could not be discovered from the active production "
        "source tree."
    )
    print(
        "Lexeme construction probe: SKIPPED "
        "(no class invented or substituted)"
    )

    lexeme = None
    lexeme_metadata = None

else:
    report_class(
        "Lexeme",
        Lexeme,
    )

    report_signature(
        "Lexeme.__init__",
        Lexeme.__init__,
    )

    report_source(
        "Lexeme",
        Lexeme,
        max_lines=140,
    )

    if LexemeMetadata is not None:
        report_dataclass(
            "LexemeMetadata",
            LexemeMetadata,
        )

        report_signature(
            "LexemeMetadata.__init__",
            LexemeMetadata.__init__,
        )

    else:
        print()
        print("LexemeMetadata class: NOT FOUND")

    lexeme = None
    lexeme_metadata = None

    # ------------------------------------------------------------------------
    # Try a conservative constructor based only on existing signature.
    # ------------------------------------------------------------------------

    try:
        metadata_kwargs: dict[str, object] = {}

        if LexemeMetadata is not None:
            metadata_signature = inspect.signature(
                LexemeMetadata
            )

            parameters = metadata_signature.parameters

            if "lemma" in parameters:
                metadata_kwargs["lemma"] = "हरि"

            if "transliteration" in parameters:
                metadata_kwargs["transliteration"] = "hari"

            if "language" in parameters:
                metadata_kwargs["language"] = "sanskrit"

            if "script" in parameters:
                metadata_kwargs["script"] = "devanagari"

            lexeme_metadata = LexemeMetadata(
                **metadata_kwargs
            )

            print()
            print(
                "LexemeMetadata construction: SUCCESS"
            )
            report_object(
                "LexemeMetadata",
                lexeme_metadata,
            )

            lexeme_signature = inspect.signature(
                Lexeme
            )

            lexeme_kwargs: dict[str, object] = {}

            if "identifier" in lexeme_signature.parameters:
                lexeme_kwargs["identifier"] = (
                    "amarakosha:lexeme:hari"
                )

            if "metadata" in lexeme_signature.parameters:
                lexeme_kwargs["metadata"] = lexeme_metadata

            lexeme = Lexeme(
                **lexeme_kwargs
            )

            print()
            print("Lexeme construction: SUCCESS")
            report_object(
                "Lexeme",
                lexeme,
            )

        else:
            print(
                "Lexeme construction: SKIPPED "
                "(LexemeMetadata unavailable)"
            )

    except Exception as exc:
        print()
        print("Lexeme construction: FAILURE")
        print(f"  {type(exc).__name__}: {exc}")


# ============================================================================
# 8. SYNSET DIRECT CONSTRUCTION
# ============================================================================

section("8. SYNSET DIRECT CONSTRUCTION")

report_class(
    "Synset",
    Synset,
)

report_dataclass(
    "SynsetMetadata",
    SynsetMetadata,
)

report_signature(
    "Synset.__init__",
    Synset.__init__,
)

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

    children = []

    if lexeme is not None:
        children.append(lexeme)

    synset = Synset(
        identifier="amarakosha:synset:hari",
        metadata=synset_metadata,
        children=children,
    )

    print("Direct Synset construction: SUCCESS")

    report_object(
        "SynsetMetadata",
        synset_metadata,
    )

    report_object(
        "Synset",
        synset,
    )

except Exception as exc:
    synset = None

    print("Direct Synset construction: FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


# ============================================================================
# 9. VARGA DIRECT CONSTRUCTION
# ============================================================================

section("9. VARGA DIRECT CONSTRUCTION")

report_class(
    "Varga",
    Varga,
)

report_dataclass(
    "VargaMetadata",
    VargaMetadata,
)

report_signature(
    "Varga.__init__",
    Varga.__init__,
)

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

    children = []

    if synset is not None:
        children.append(synset)

    varga = Varga(
        identifier="amarakosha:varga:example",
        metadata=varga_metadata,
        children=children,
    )

    print("Direct Varga construction: SUCCESS")

    report_object(
        "VargaMetadata",
        varga_metadata,
    )

    report_object(
        "Varga",
        varga,
    )

except Exception as exc:
    varga = None

    print("Direct Varga construction: FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


# ============================================================================
# 10. BUILDER INTERNAL STATE
# ============================================================================

section("10. BUILDER INTERNAL STATE")

if synset_builder is not None:

    print("[SynsetBuilder internal state]")

    for name in (
        "_identifier",
        "_metadata",
        "_lexemes",
        "_instance",
    ):
        if hasattr(synset_builder, name):
            print(
                f"  {name} = "
                f"{getattr(synset_builder, name)!r}"
            )

else:
    print(
        "SynsetBuilder instance unavailable."
    )


if varga_builder is not None:

    print()
    print("[VargaBuilder internal state]")

    for name in (
        "_identifier",
        "_metadata",
        "_synsets",
        "_instance",
    ):
        if hasattr(varga_builder, name):
            print(
                f"  {name} = "
                f"{getattr(varga_builder, name)!r}"
            )

else:
    print(
        "VargaBuilder instance unavailable."
    )


# ============================================================================
# 11. BUILDER CONTRACT COMPARISON
# ============================================================================

section("11. BUILDER CONTRACT COMPARISON")

for label, cls in (
    ("SynsetBuilder", SynsetBuilder),
    ("VargaBuilder", VargaBuilder),
):

    print()
    print(f"[{label}]")

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

        method = getattr(
            cls,
            method_name,
            None,
        )

        if method is None:
            print(
                f"  {method_name}: MISSING"
            )
            continue

        try:
            owner = method.__qualname__
        except Exception:
            owner = "<UNKNOWN>"

        try:
            signature = inspect.signature(method)
        except (TypeError, ValueError):
            signature = "<UNAVAILABLE>"

        print(
            f"  {method_name}: "
            f"owner={owner}, "
            f"signature={signature}"
        )


# ============================================================================
# 12. EXISTING FLUENT SYNSET BUILDER PROBE
# ============================================================================

section("12. SYNSET FLUENT BUILDER PROBE")

if synset_builder is None:

    print(
        "SynsetBuilder unavailable; "
        "fluent probe skipped."
    )

else:

    try:
        configured = (
            synset_builder
            .with_identifier(
                "amarakosha:synset:hari"
            )
            .with_metadata(
                SynsetMetadata(
                    lemma="हरि",
                    transliteration="hari",
                    kanda=Amarakanda.SVARGADI,
                    varga="example",
                    verse_number=1,
                    synset_identifier=(
                        "amarakosha:synset:hari"
                    ),
                )
            )
        )

        if lexeme is not None:
            configured.add_lexeme(
                lexeme
            )

        print(
            "Fluent SynsetBuilder configuration: SUCCESS"
        )

        try:
            built = configured.build()

            print(
                "SynsetBuilder.build(): SUCCESS"
            )

            report_object(
                "Built Synset",
                built,
            )

        except Exception as exc:
            print(
                "SynsetBuilder.build(): FAILURE"
            )
            print(
                f"  {type(exc).__name__}: {exc}"
            )

    except Exception as exc:
        print(
            "Fluent SynsetBuilder configuration: FAILURE"
        )
        print(
            f"  {type(exc).__name__}: {exc}"
        )


# ============================================================================
# 13. EXISTING FLUENT VARGA BUILDER PROBE
# ============================================================================

section("13. VARGA FLUENT BUILDER PROBE")

if varga_builder is None:

    print(
        "VargaBuilder unavailable; "
        "fluent probe skipped."
    )

else:

    try:
        configured = (
            varga_builder
            .with_identifier(
                "amarakosha:varga:example"
            )
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
            configured.add_synset(
                synset
            )

        print(
            "Fluent VargaBuilder configuration: SUCCESS"
        )

        try:
            built = configured.build()

            print(
                "VargaBuilder.build(): SUCCESS"
            )

            report_object(
                "Built Varga",
                built,
            )

        except Exception as exc:
            print(
                "VargaBuilder.build(): FAILURE"
            )
            print(
                f"  {type(exc).__name__}: {exc}"
            )

    except Exception as exc:
        print(
            "Fluent VargaBuilder configuration: FAILURE"
        )
        print(
            f"  {type(exc).__name__}: {exc}"
        )


# ============================================================================
# 14. REGISTRY PROBE
# ============================================================================

section("14. AMARAKOSHA REGISTRY PROBE")

report_class(
    "AmarakoshaRegistry",
    AmarakoshaRegistry,
)

report_signature(
    "AmarakoshaRegistry.__init__",
    AmarakoshaRegistry.__init__,
)

try:
    registry = AmarakoshaRegistry()

    print(
        "AmarakoshaRegistry(): SUCCESS"
    )

    report_object(
        "Registry",
        registry,
    )

except Exception as exc:
    registry = None

    print(
        "AmarakoshaRegistry(): FAILURE"
    )
    print(
        f"  {type(exc).__name__}: {exc}"
    )


if registry is not None:

    if synset is not None:

        try:
            registry.add(synset)

            print(
                "registry.add(Synset): SUCCESS"
            )

            print(
                "  exists:",
                registry.exists(
                    synset.identifier
                ),
            )

            print(
                "  get:",
                registry.get(
                    synset.identifier
                ),
            )

        except Exception as exc:
            print(
                "registry.add(Synset): FAILURE"
            )
            print(
                f"  {type(exc).__name__}: {exc}"
            )

    if varga is not None:

        try:
            registry.add(varga)

            print(
                "registry.add(Varga): SUCCESS"
            )

            print(
                "  exists:",
                registry.exists(
                    varga.identifier
                ),
            )

            print(
                "  get:",
                registry.get(
                    varga.identifier
                ),
            )

        except Exception as exc:
            print(
                "registry.add(Varga): FAILURE"
            )
            print(
                f"  {type(exc).__name__}: {exc}"
            )

    print()
    print("Registry contents:")

    try:
        for identifier, obj in registry.items():
            print(
                f"  {identifier!r} "
                f"-> {type(obj).__name__}"
            )

    except Exception as exc:
        print(
            "  registry.items() failure:"
        )
        print(
            f"    {type(exc).__name__}: {exc}"
        )

    try:
        print(
            "  synsets:",
            [
                obj.identifier
                for obj in registry.synsets()
            ],
        )

    except Exception as exc:
        print(
            "  synsets() failure:",
            exc,
        )

    try:
        print(
            "  vargas:",
            [
                obj.identifier
                for obj in registry.vargas()
            ],
        )

    except Exception as exc:
        print(
            "  vargas() failure:",
            exc,
        )


# ============================================================================
# 15. RECORD CONSTRUCTION
# ============================================================================

section("15. SYNSET RECORD CONSTRUCTION")

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
        lexeme_ids=(
            "amarakosha:lexeme:hari",
        ),
        tags=("probe",),
        notes="Runtime construction probe",
    )

    print(
        "SynsetRecord construction: SUCCESS"
    )

    report_object(
        "SynsetRecord",
        synset_record,
    )

except Exception as exc:

    synset_record = None

    print(
        "SynsetRecord construction: FAILURE"
    )
    print(
        f"  {type(exc).__name__}: {exc}"
    )


section("16. VARGA RECORD CONSTRUCTION")

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

    print(
        "VargaRecord construction: SUCCESS"
    )

    report_object(
        "VargaRecord",
        varga_record,
    )

except Exception as exc:

    varga_record = None

    print(
        "VargaRecord construction: FAILURE"
    )
    print(
        f"  {type(exc).__name__}: {exc}"
    )


# ============================================================================
# 17. RECORD BUILDER API
# ============================================================================

section("17. SYNSET RECORD BUILDER API")

if synset_record_builder is None:

    print(
        "SynsetRecordBuilder unavailable."
    )

else:

    for method_name in dir(
        synset_record_builder
    ):

        if method_name.startswith("_"):
            continue

        try:
            attribute = getattr(
                synset_record_builder,
                method_name,
            )
        except Exception:
            continue

        if not callable(attribute):
            continue

        if method_name in {
            "build",
            "build_many",
            "build_validated",
            "validate",
            "reset",
            "instance",
            "from_instance",
            "clone",
        } or method_name.startswith(
            "with_"
        ) or method_name.startswith(
            "add_"
        ):

            try:
                print(
                    f"  {method_name}"
                    f"{inspect.signature(attribute)}"
                )
            except (TypeError, ValueError):
                print(
                    f"  {method_name}"
                )


# ============================================================================
# 18. FINAL EVIDENCE SUMMARY
# ============================================================================

section("18. BATCH 5D EVIDENCE SUMMARY")

print(
    "Existing Lexeme ownership:"
)

print(
    "  Lexeme found          :",
    Lexeme is not None,
)

print(
    "  LexemeMetadata found  :",
    LexemeMetadata is not None,
)

print()

print(
    "Construction results:"
)

print(
    "  SynsetBuilder instance :",
    synset_builder is not None,
)

print(
    "  VargaBuilder instance  :",
    varga_builder is not None,
)

print(
    "  SynsetRecordBuilder    :",
    synset_record_builder is not None,
)

print(
    "  Lexeme construction    :",
    lexeme is not None,
)

print(
    "  Synset construction    :",
    synset is not None,
)

print(
    "  Varga construction     :",
    varga is not None,
)

print(
    "  Registry construction  :",
    registry is not None,
)

print(
    "  SynsetRecord           :",
    synset_record is not None,
)

print(
    "  VargaRecord            :",
    varga_record is not None,
)


# ============================================================================
# 19. ARCHITECTURAL INTERPRETATION
# ============================================================================

section("19. BATCH 5D DECISION GATE")

print(
    """
READ-ONLY INTERPRETATION RULES

1. Lexeme ownership must come from the existing production tree.
   No replacement Lexeme class is introduced.

2. If SynsetBuilder/VargaBuilder remain abstract while their concrete
   build() methods already construct Synset/Varga directly, this is
   evidence of an inherited builder-contract mismatch.

3. The _create_instance() requirement must not be removed or implemented
   until BaseBuilder / NodeBuilder semantics demonstrate why it exists.

4. If direct Synset/Varga construction succeeds while concrete builder
   construction fails, the discrepancy must be treated as architectural
   evidence, not as a reason for an immediate patch.

5. If Lexeme construction succeeds, determine whether SynsetRecord.lexeme_ids
   can be resolved through an existing repository/registry boundary.

6. If no existing Lexeme resolver is found, do not invent one during this
   probe.

7. If registry.add(Synset) and registry.add(Varga) succeed, retain
   AmarakoshaRegistry as the existing Amarakośa registration boundary.

8. Record → Builder feasibility must be based only on existing builder APIs.

9. No canonical dictionary objects are constructed by this probe.

10. No Amarakośa adapter is designed or implemented by this probe.
"""
)

print()

print(
    "BATCH 5D STATUS:"
)

if (
    synset is not None
    and varga is not None
    and registry is not None
):
    print(
        "  DIRECT DOMAIN CONSTRUCTION = VERIFIED"
    )
else:
    print(
        "  DIRECT DOMAIN CONSTRUCTION = PARTIAL / BLOCKED"
    )

if (
    synset_builder is None
    or varga_builder is None
):
    print(
        "  BUILDER CONTRACT = REQUIRES FOLLOW-UP AUDIT"
    )
else:
    print(
        "  BUILDER CONTRACT = RUNTIME-CONSTRUCTIBLE"
    )

if Lexeme is None:
    print(
        "  LEXEME OWNERSHIP = UNRESOLVED"
    )
else:
    print(
        "  LEXEME OWNERSHIP = IDENTIFIED"
    )

print(
    "  CANONICAL ADAPTER = BLOCKED"
)

print()
print("BATCH 5D COMPLETE")
print("=" * 118)
