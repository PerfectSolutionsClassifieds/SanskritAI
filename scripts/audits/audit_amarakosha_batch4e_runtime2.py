from __future__ import annotations

"""
BATCH 4E — AMARAKOSHA RUNTIME DATA-FLOW PROBE

Purpose
-------
Runtime probe for the active Amarakośa production data-flow.

This audit intentionally:
- uses the repository root as the Python import root
- imports active production packages directly
- ignores historical duplicate files
- does not modify production code
- does not create new production abstractions
- probes constructors, signatures, parser/importer/registry behavior,
  and builder/record relationships

Execution
---------
From repository root:

    python scripts/audits/audit_amarakosha_batch4e_runtime.py
"""

from pathlib import Path
import inspect
import sys
import traceback


# ============================================================================
# Repository / import bootstrap
# ============================================================================

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


# ============================================================================
# Helpers
# ============================================================================

SEPARATOR = "=" * 90


def section(title: str) -> None:
    print()
    print(SEPARATOR)
    print(title)
    print(SEPARATOR)


def safe_signature(obj) -> str:
    try:
        return str(inspect.signature(obj))
    except Exception as exc:
        return f"<signature unavailable: {type(exc).__name__}: {exc}>"


def safe_source_file(obj) -> str:
    try:
        return str(inspect.getfile(obj))
    except Exception as exc:
        return f"<source unavailable: {type(exc).__name__}: {exc}>"


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


def dump_public_attributes(label: str, obj) -> None:
    print()
    print(f"[ATTRIBUTES] {label}")

    try:
        names = [
            name
            for name in dir(obj)
            if not name.startswith("_")
        ]

        for name in names:
            try:
                value = getattr(obj, name)

                if callable(value):
                    print(
                        f"  {name}: "
                        f"{type(value).__name__} "
                        f"{safe_signature(value)}"
                    )
                else:
                    print(
                        f"  {name}: "
                        f"{type(value).__name__} = {value!r}"
                    )

            except Exception as exc:
                print(
                    f"  {name}: "
                    f"<ERROR {type(exc).__name__}: {exc}>"
                )

    except Exception as exc:
        print(
            f"  <attribute inspection failed: "
            f"{type(exc).__name__}: {exc}>"
        )


# ============================================================================
# Main
# ============================================================================

def main() -> None:

    section(
        "BATCH 4E — AMARAKOSHA RUNTIME DATA-FLOW PROBE"
    )

    print(f"Repository root : {REPO_ROOT}")
    print(f"Python executable: {sys.executable}")
    print(f"Python version   : {sys.version.split()[0]}")
    print()
    print("Import root verified:")
    print(f"  {REPO_ROOT}")

    # ------------------------------------------------------------------------
    # Import active Amarakośa components
    # ------------------------------------------------------------------------

    section("1. IMPORT ACTIVE AMARAKOSHA COMPONENTS")

    try:
        from amarakosha.parsers.amarakosha_parser import (
            AmarakoshaParser,
        )

        from amarakosha.importer import (
            AmarakoshaImporter,
        )

        from amarakosha.registry import (
            AmarakoshaRegistry,
        )

        from amarakosha.builders.synset_builder import (
            SynsetBuilder,
        )

        from amarakosha.builders.varga_builder import (
            VargaBuilder,
        )

        from amarakosha.records.synset_record import (
            SynsetRecord,
        )

        from amarakosha.records.varga_record import (
            VargaRecord,
        )

    except Exception as exc:
        print()
        print("IMPORT FAILURE")
        print(f"Exception: {type(exc).__name__}: {exc}")
        print()
        print(
            "The Batch 4E probe cannot continue until the actual "
            "Amarakośa package import paths are confirmed."
        )
        print()
        traceback.print_exc()

        raise SystemExit(1)

    print("All Amarakośa imports succeeded.")

    components = {
        "AmarakoshaParser": AmarakoshaParser,
        "AmarakoshaImporter": AmarakoshaImporter,
        "AmarakoshaRegistry": AmarakoshaRegistry,
        "SynsetBuilder": SynsetBuilder,
        "VargaBuilder": VargaBuilder,
        "SynsetRecord": SynsetRecord,
        "VargaRecord": VargaRecord,
    }

    for name, obj in components.items():
        print()
        print(f"{name}")
        print(f"  module : {obj.__module__}")
        print(f"  source : {safe_source_file(obj)}")
        print(f"  class  : {obj}")
        print(f"  bases  : {[base.__name__ for base in obj.__bases__]}")
        print(f"  sig    : {safe_signature(obj)}")

    # ------------------------------------------------------------------------
    # Constructor signatures
    # ------------------------------------------------------------------------

    section("2. CONSTRUCTOR SIGNATURES")

    for name, cls in components.items():
        print()
        print(f"{name}")
        print(f"  {safe_signature(cls)}")

        try:
            print(
                "  __init__ : "
                f"{safe_signature(cls.__init__)}"
            )
        except Exception as exc:
            print(
                "  __init__ : "
                f"<ERROR {type(exc).__name__}: {exc}>"
            )

    # ------------------------------------------------------------------------
    # Parser inspection
    # ------------------------------------------------------------------------

    section("3. PARSER RUNTIME CONTRACT")

    print("AmarakoshaParser source:")
    print(f"  {safe_source_file(AmarakoshaParser)}")

    parser = safe_call(
        "Instantiate AmarakoshaParser",
        AmarakoshaParser,
    )

    if parser is not None:
        dump_public_attributes(
            "AmarakoshaParser instance",
            parser,
        )

        parser_methods = [
            name
            for name in dir(parser)
            if not name.startswith("_")
            and callable(getattr(parser, name, None))
        ]

        print()
        print("Parser callable methods:")

        for name in parser_methods:
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

    # ------------------------------------------------------------------------
    # Registry inspection
    # ------------------------------------------------------------------------

    section("4. REGISTRY RUNTIME CONTRACT")

    registry = safe_call(
        "Instantiate AmarakoshaRegistry",
        AmarakoshaRegistry,
    )

    if registry is not None:
        dump_public_attributes(
            "AmarakoshaRegistry instance",
            registry,
        )

        registry_methods = [
            name
            for name in dir(registry)
            if not name.startswith("_")
            and callable(getattr(registry, name, None))
        ]

        print()
        print("Registry callable methods:")

        for name in registry_methods:
            try:
                method = getattr(registry, name)
                print(
                    f"  {name}{safe_signature(method)}"
                )
            except Exception as exc:
                print(
                    f"  {name}: "
                    f"<ERROR {type(exc).__name__}: {exc}>"
                )

    # ------------------------------------------------------------------------
    # Importer inspection
    # ------------------------------------------------------------------------

    section("5. IMPORTER RUNTIME CONTRACT")

    print(
        "AmarakoshaImporter signature: "
        f"{safe_signature(AmarakoshaImporter)}"
    )

    print(
        "AmarakoshaImporter source: "
        f"{safe_source_file(AmarakoshaImporter)}"
    )

    importer = safe_call(
        "Instantiate AmarakoshaImporter",
        AmarakoshaImporter,
    )

    if importer is not None:
        dump_public_attributes(
            "AmarakoshaImporter instance",
            importer,
        )

    # ------------------------------------------------------------------------
    # Record inspection
    # ------------------------------------------------------------------------

    section("6. RECORD CONTRACTS")

    for name, cls in (
        ("SynsetRecord", SynsetRecord),
        ("VargaRecord", VargaRecord),
    ):
        print()
        print(name)
        print(f"  module     : {cls.__module__}")
        print(f"  source     : {safe_source_file(cls)}")
        print(f"  signature  : {safe_signature(cls)}")

        try:
            annotations = getattr(cls, "__annotations__", {})
            print("  annotations:")

            if annotations:
                for field_name, field_type in annotations.items():
                    print(
                        f"    {field_name}: "
                        f"{field_type}"
                    )
            else:
                print("    <none>")

        except Exception as exc:
            print(
                f"    <ERROR {type(exc).__name__}: {exc}>"
            )

    # ------------------------------------------------------------------------
    # Builder inspection
    # ------------------------------------------------------------------------

    section("7. BUILDER CONTRACTS")

    for name, cls in (
        ("SynsetBuilder", SynsetBuilder),
        ("VargaBuilder", VargaBuilder),
    ):
        print()
        print(name)
        print(f"  module: {cls.__module__}")
        print(f"  source: {safe_source_file(cls)}")
        print(f"  class : {safe_signature(cls)}")

        try:
            builder = cls()

            print("  instantiation: SUCCESS")

            dump_public_attributes(
                f"{name} instance",
                builder,
            )

            methods = [
                method_name
                for method_name in dir(builder)
                if not method_name.startswith("_")
                and callable(
                    getattr(builder, method_name, None)
                )
            ]

            print()
            print("  callable methods:")

            for method_name in methods:
                try:
                    method = getattr(
                        builder,
                        method_name,
                    )

                    print(
                        f"    {method_name}"
                        f"{safe_signature(method)}"
                    )

                except Exception as exc:
                    print(
                        f"    {method_name}: "
                        f"<ERROR {type(exc).__name__}: {exc}>"
                    )

        except Exception as exc:
            print(
                "  instantiation: ERROR "
                f"{type(exc).__name__}: {exc}"
            )

    # ------------------------------------------------------------------------
    # Parser empty-input probe
    # ------------------------------------------------------------------------

    section("8. PARSER EMPTY-INPUT PROBE")

    if parser is not None:

        candidate_inputs = [
            None,
            "",
            [],
        ]

        parser_methods = [
            name
            for name in dir(parser)
            if not name.startswith("_")
            and callable(getattr(parser, name, None))
        ]

        parser_methods = [
            name
            for name in parser_methods
            if any(
                token in name.lower()
                for token in (
                    "parse",
                    "load",
                    "read",
                    "extract",
                )
            )
        ]

        print(
            "Parser methods selected for conservative "
            "empty-input probing:"
        )

        for name in parser_methods:
            print(f"  {name}")

        for method_name in parser_methods:

            method = getattr(parser, method_name)

            print()
            print(
                f"--- probing parser.{method_name} ---"
            )
            print(
                f"signature: {safe_signature(method)}"
            )

            signature = inspect.signature(method)
            parameters = list(signature.parameters.values())

            # Only probe methods with at most one required positional
            # argument. Do not fabricate complex parser inputs.
            required = [
                parameter
                for parameter in parameters
                if parameter.default is inspect.Parameter.empty
                and parameter.kind
                in (
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                )
            ]

            if len(required) == 0:
                safe_call(
                    f"parser.{method_name}()",
                    method,
                )

            elif len(required) == 1:
                for value in candidate_inputs:
                    safe_call(
                        (
                            f"parser.{method_name}"
                            f"({value!r})"
                        ),
                        method,
                        value,
                    )

            else:
                print(
                    "  SKIPPED: requires multiple "
                    "positional arguments."
                )

    # ------------------------------------------------------------------------
    # Registry state probe
    # ------------------------------------------------------------------------

    section("9. REGISTRY STATE PROBE")

    if registry is not None:

        print("Initial registry state:")

        try:
            dump_public_attributes(
                "Registry initial state",
                registry,
            )
        except Exception as exc:
            print(
                f"  inspection error: "
                f"{type(exc).__name__}: {exc}"
            )

        print()
        print(
            "No synthetic Amarakośa records are inserted "
            "by this audit."
        )
        print(
            "This preserves production registry semantics "
            "and avoids fabricating source data."
        )

    # ------------------------------------------------------------------------
    # Runtime target summary
    # ------------------------------------------------------------------------

    section("10. BATCH 4E INTERPRETATION TARGETS")

    print(
        "This probe is intended to establish the following:"
    )

    print()
    print(
        "1. Whether AmarakoshaParser returns records directly "
        "or mutates another object."
    )

    print(
        "2. Whether AmarakoshaImporter owns parser invocation "
        "and registration."
    )

    print(
        "3. Whether AmarakoshaRegistry is the runtime ownership "
        "boundary for Synset/Varga objects."
    )

    print(
        "4. Whether SynsetBuilder/VargaBuilder construct the "
        "production domain objects from records."
    )

    print(
        "5. Which fields survive the runtime construction path."
    )

    print(
        "6. Whether any existing runtime object already provides "
        "a canonical-knowledge boundary."
    )

    print(
        "7. Whether Amarakośa data can be mapped to the existing "
        "canonical dictionary model without introducing duplicate "
        "dictionary abstractions."
    )

    section("BATCH 4E COMPLETE")

    print(
        "No production Amarakośa or canonical code was modified."
    )
    print(
        "The next architectural step remains Batch 5 mapping "
        "only after the runtime contract is confirmed."
    )


if __name__ == "__main__":
    main()
