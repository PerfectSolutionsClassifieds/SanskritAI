from __future__ import annotations

"""
BATCH 4E — AMARAKOSHA RUNTIME DATA-FLOW PROBE

This audit follows the repository's established package convention:

    /content/
        SanskritAI/
            __init__.py
            amarakosha/
            lexical/
            core/
            corpus/
            ...

Therefore:

    repository root = /content/SanskritAI
    package root     = /content
    package name     = SanskritAI

This script performs READ-ONLY runtime inspection.

It does not modify production code.
It does not create production abstractions.
It does not insert synthetic Amarakośa data.
"""

from pathlib import Path
import inspect
import sys
import traceback


# ============================================================================
# PATH BOOTSTRAP
# ============================================================================

SCRIPT_PATH = Path(__file__).resolve()

# /content/SanskritAI/scripts/audits/script.py
#
# parents[0] = audits
# parents[1] = scripts
# parents[2] = SanskritAI
# parents[3] = content

REPOSITORY_ROOT = SCRIPT_PATH.parents[2]
PACKAGE_ROOT = REPOSITORY_ROOT.parent

if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


# ============================================================================
# CONSTANTS
# ============================================================================

SEPARATOR = "=" * 90


# ============================================================================
# HELPERS
# ============================================================================

def section(title: str) -> None:
    print()
    print(SEPARATOR)
    print(title)
    print(SEPARATOR)


def safe_signature(obj) -> str:
    try:
        return str(inspect.signature(obj))
    except Exception as exc:
        return (
            f"<signature unavailable: "
            f"{type(exc).__name__}: {exc}>"
        )


def safe_source(obj) -> str:
    try:
        return inspect.getfile(obj)
    except Exception as exc:
        return (
            f"<source unavailable: "
            f"{type(exc).__name__}: {exc}>"
        )


def safe_call(label, callable_obj, *args, **kwargs):
    print()
    print(f"[PROBE] {label}")
    print(f"  callable : {callable_obj}")
    print(f"  signature: {safe_signature(callable_obj)}")

    try:
        result = callable_obj(*args, **kwargs)

        print("  status   : SUCCESS")
        print(f"  type     : {type(result).__name__}")
        print(f"  value    : {result!r}")

        return result

    except Exception as exc:
        print("  status   : ERROR")
        print(f"  exception: {type(exc).__name__}: {exc}")

        traceback.print_exc(limit=3)

        return None


def dump_annotations(cls) -> None:
    print("  annotations:")

    try:
        annotations = getattr(cls, "__annotations__", {})

        if not annotations:
            print("    <none>")
            return

        for name, annotation in annotations.items():
            print(f"    {name}: {annotation}")

    except Exception as exc:
        print(
            f"    <ERROR {type(exc).__name__}: {exc}>"
        )


def dump_public_methods(obj) -> None:
    print()
    print("  public callable methods:")

    for name in dir(obj):

        if name.startswith("_"):
            continue

        try:
            value = getattr(obj, name)
        except Exception:
            continue

        if callable(value):
            print(
                f"    {name}{safe_signature(value)}"
            )


def dump_public_attributes(obj) -> None:
    print()
    print("  public attributes:")

    for name in dir(obj):

        if name.startswith("_"):
            continue

        try:
            value = getattr(obj, name)
        except Exception as exc:
            print(
                f"    {name}: "
                f"<ERROR {type(exc).__name__}: {exc}>"
            )
            continue

        if callable(value):
            continue

        print(
            f"    {name}: "
            f"{type(value).__name__} = {value!r}"
        )


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:

    section(
        "BATCH 4E — AMARAKOSHA RUNTIME DATA-FLOW PROBE"
    )

    print(f"Repository root : {REPOSITORY_ROOT}")
    print(f"Package root    : {PACKAGE_ROOT}")
    print(f"Python          : {sys.executable}")
    print(f"Version         : {sys.version.split()[0]}")
    print()

    print("sys.path package-root check:")
    print(
        f"  {PACKAGE_ROOT} "
        f"in sys.path = {str(PACKAGE_ROOT) in sys.path}"
    )

    # ========================================================================
    # 1. PACKAGE IMPORT
    # ========================================================================

    section("1. SANskRITAI PACKAGE IMPORT")

    try:
        import SanskritAI

        print("SanskritAI import: SUCCESS")
        print(f"  module : {SanskritAI}")
        print(
            f"  file   : "
            f"{getattr(SanskritAI, '__file__', '<none>')}"
        )
        print(
            f"  path   : "
            f"{getattr(SanskritAI, '__path__', '<none>')}"
        )

    except Exception as exc:

        print("SanskritAI import: FAILURE")
        print(
            f"  exception: "
            f"{type(exc).__name__}: {exc}"
        )

        traceback.print_exc()

        raise SystemExit(1)

    # ========================================================================
    # 2. ACTIVE AMARAKOSHA IMPORTS
    # ========================================================================

    section("2. IMPORT ACTIVE AMARAKOSHA COMPONENTS")

    try:

        from SanskritAI.amarakosha.parsers.amarakosha_parser import (
            AmarakoshaParser,
        )

        from SanskritAI.amarakosha.importers.amarakosha_importer import (
            AmarakoshaImporter,
        )

        from SanskritAI.amarakosha.registries.amarakosha_registry import (
            AmarakoshaRegistry,
        )

        from SanskritAI.amarakosha.builders.synset_builder import (
            SynsetBuilder,
        )

        from SanskritAI.amarakosha.builders.varga_builder import (
            VargaBuilder,
        )

        from SanskritAI.amarakosha.records.synset_record import (
            SynsetRecord,
        )

        from SanskritAI.amarakosha.records.varga_record import (
            VargaRecord,
        )

        from SanskritAI.amarakosha.models.synset import (
            Synset,
        )

        from SanskritAI.amarakosha.models.varga import (
            Varga,
        )

        from SanskritAI.lexical.models.lexeme import (
            Lexeme,
        )

    except Exception as exc:

        print("Amarakośa import: FAILURE")
        print(
            f"  exception: "
            f"{type(exc).__name__}: {exc}"
        )

        traceback.print_exc()

        raise SystemExit(1)

    print("All selected active imports succeeded.")

    components = {
        "AmarakoshaParser": AmarakoshaParser,
        "AmarakoshaImporter": AmarakoshaImporter,
        "AmarakoshaRegistry": AmarakoshaRegistry,
        "SynsetBuilder": SynsetBuilder,
        "VargaBuilder": VargaBuilder,
        "SynsetRecord": SynsetRecord,
        "VargaRecord": VargaRecord,
        "Synset": Synset,
        "Varga": Varga,
        "Lexeme": Lexeme,
    }

    for name, cls in components.items():

        print()
        print(name)
        print(f"  module : {cls.__module__}")
        print(f"  source : {safe_source(cls)}")
        print(f"  class  : {cls}")
        print(
            "  bases  : "
            f"{[base.__name__ for base in cls.__bases__]}"
        )
        print(f"  sig    : {safe_signature(cls)}")

        dump_annotations(cls)

    # ========================================================================
    # 3. PARSER
    # ========================================================================

    section("3. AMARAKOSHA PARSER RUNTIME CONTRACT")

    parser = safe_call(
        "Instantiate AmarakoshaParser",
        AmarakoshaParser,
    )

    if parser is not None:

        dump_public_attributes(parser)
        dump_public_methods(parser)

        print()
        print("Parser methods selected for data-flow inspection:")

        selected = []

        for name in dir(parser):

            if name.startswith("_"):
                continue

            try:
                value = getattr(parser, name)
            except Exception:
                continue

            if not callable(value):
                continue

            lowered = name.lower()

            if any(
                token in lowered
                for token in (
                    "parse",
                    "load",
                    "read",
                    "extract",
                    "build",
                )
            ):
                selected.append(name)

        for name in selected:
            try:
                method = getattr(parser, name)
                print(
                    f"  {name}{safe_signature(method)}"
                )
            except Exception as exc:
                print(
                    f"  {name}: "
                    f"<ERROR {type(exc).__name__}: {exc}>"
                )

    # ========================================================================
    # 4. IMPORTER
    # ========================================================================

    section("4. AMARAKOSHA IMPORTER RUNTIME CONTRACT")

    importer = safe_call(
        "Instantiate AmarakoshaImporter",
        AmarakoshaImporter,
    )

    if importer is not None:

        dump_public_attributes(importer)
        dump_public_methods(importer)

    # ========================================================================
    # 5. REGISTRY
    # ========================================================================

    section("5. AMARAKOSHA REGISTRY RUNTIME CONTRACT")

    registry = safe_call(
        "Instantiate AmarakoshaRegistry",
        AmarakoshaRegistry,
    )

    if registry is not None:

        dump_public_attributes(registry)
        dump_public_methods(registry)

        print()
        print(
            "No synthetic Amarakośa records are inserted "
            "into the registry."
        )

    # ========================================================================
    # 6. RECORDS
    # ========================================================================

    section("6. AMARAKOSHA RECORD CONTRACTS")

    for name, cls in (
        ("SynsetRecord", SynsetRecord),
        ("VargaRecord", VargaRecord),
    ):

        print()
        print(name)
        print(f"  module : {cls.__module__}")
        print(f"  source : {safe_source(cls)}")
        print(f"  sig    : {safe_signature(cls)}")

        dump_annotations(cls)

    # ========================================================================
    # 7. BUILDERS
    # ========================================================================

    section("7. AMARAKOSHA BUILDER CONTRACTS")

    for name, cls in (
        ("SynsetBuilder", SynsetBuilder),
        ("VargaBuilder", VargaBuilder),
    ):

        print()
        print(name)
        print(f"  module : {cls.__module__}")
        print(f"  source : {safe_source(cls)}")
        print(f"  sig    : {safe_signature(cls)}")

        builder = safe_call(
            f"Instantiate {name}",
            cls,
        )

        if builder is not None:

            dump_public_attributes(builder)
            dump_public_methods(builder)

    # ========================================================================
    # 8. DOMAIN MODEL CONTRACTS
    # ========================================================================

    section("8. AMARAKOSHA DOMAIN MODEL CONTRACTS")

    for name, cls in (
        ("Synset", Synset),
        ("Varga", Varga),
        ("Lexeme", Lexeme),
    ):

        print()
        print(name)
        print(f"  module : {cls.__module__}")
        print(f"  source : {safe_source(cls)}")
        print(f"  sig    : {safe_signature(cls)}")

        dump_annotations(cls)

    # ========================================================================
    # 9. CONSTRUCTOR / FIELD SUMMARY
    # ========================================================================

    section("9. CONSTRUCTOR AND FIELD SUMMARY")

    for name, cls in components.items():

        print()
        print(f"[{name}]")

        try:
            print(
                "  constructor: "
                f"{safe_signature(cls)}"
            )
        except Exception as exc:
            print(
                f"  constructor: "
                f"<ERROR {type(exc).__name__}: {exc}>"
            )

        try:
            annotations = getattr(
                cls,
                "__annotations__",
                {},
            )

            if annotations:
                print("  fields:")

                for field_name, field_type in annotations.items():
                    print(
                        f"    {field_name}: "
                        f"{field_type}"
                    )
            else:
                print("  fields: <none>")

        except Exception as exc:
            print(
                f"  fields: "
                f"<ERROR {type(exc).__name__}: {exc}>"
            )

    # ========================================================================
    # 10. RUNTIME INTERPRETATION
    # ========================================================================

    section("10. BATCH 4E INTERPRETATION TARGETS")

    print(
        "The runtime probe is intended to establish:"
    )

    print()
    print(
        "A. Whether AmarakoshaParser produces records directly "
        "or mutates/stores parser state."
    )

    print(
        "B. Whether AmarakoshaImporter owns parser invocation "
        "and registration."
    )

    print(
        "C. Whether AmarakoshaRegistry is the runtime ownership "
        "boundary for Synset/Varga."
    )

    print(
        "D. Whether builders transform records into Synset/Varga."
    )

    print(
        "E. Which source-semantic fields survive into Synset/Varga."
    )

    print(
        "F. Whether Synset's Lexeme objects already provide the "
        "generic lexical boundary required by canonical integration."
    )

    print(
        "G. Whether an existing production object already bridges "
        "Amarakośa into canonical knowledge."
    )

    print(
        "H. What information would be lost by a future "
        "Amarakośa → CanonicalDictionary mapping."
    )

    # ========================================================================
    # END
    # ========================================================================

    section("BATCH 4E COMPLETE")

    print(
        "No production code was modified."
    )

    print(
        "No synthetic Amarakośa source records were inserted."
    )

    print(
        "Package bootstrap used the repository's established "
        "SanskritAI.* import convention."
    )


if __name__ == "__main__":
    main()
