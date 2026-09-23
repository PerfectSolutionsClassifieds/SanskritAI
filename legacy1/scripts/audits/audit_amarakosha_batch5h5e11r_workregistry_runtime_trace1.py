from __future__ import annotations

"""
BATCH 5H-5E-11R
================

WorkRegistry -> WorkDefinition runtime trace.

Purpose
-------
Determine the actual runtime contract between:

    WorkRegistry
        |
        v
    WorkDefinition
        |
        v
    Amarakośa work identity

This is a READ-ONLY audit.

No production files are modified.
No registry entries are modified.
No new classes are created.
No acquisition is performed.
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path("/content/SanskritAI")
PACKAGE_PARENT = PROJECT_ROOT.parent

if str(PACKAGE_PARENT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_PARENT))


def section(title: str) -> None:
    print()
    print("-" * 112)
    print(title)
    print("-" * 112)


def show_attribute(obj, name: str) -> None:
    if hasattr(obj, name):
        try:
            value = getattr(obj, name)
        except Exception as exc:
            print(f"{name:24} -> <ERROR: {exc!r}>")
            return

        print(f"{name:24} -> {value!r}")
    else:
        print(f"{name:24} -> <ABSENT>")


def main() -> None:

    print("=" * 112)
    print("BATCH 5H-5E-11R — WORKREGISTRY RUNTIME TRACE")
    print("=" * 112)

    # ------------------------------------------------------------------
    # 1. Bootstrap
    # ------------------------------------------------------------------

    section("1. PACKAGE BOOTSTRAP")

    print("Project root   :", PROJECT_ROOT)
    print("Package parent :", PACKAGE_PARENT)

    import SanskritAI

    print("SanskritAI import : PASS")

    # ------------------------------------------------------------------
    # 2. WorkRegistry
    # ------------------------------------------------------------------

    section("2. WORKREGISTRY IMPORT")

    from SanskritAI.acquisition.registries.work_registry import (
        WorkRegistry,
    )

    print("WorkRegistry import : PASS")

    # ------------------------------------------------------------------
    # 3. Registry construction
    # ------------------------------------------------------------------

    section("3. WORKREGISTRY CONSTRUCTION")

    registry = WorkRegistry()

    print("WorkRegistry construction : PASS")
    print("Registry repr :", registry)

    # ------------------------------------------------------------------
    # 4. Registry class/runtime structure
    # ------------------------------------------------------------------

    section("4. WORKREGISTRY RUNTIME STRUCTURE")

    print("Registry type :", type(registry))
    print("Registry module :", type(registry).__module__)

    for name in (
        "DEFAULT_REGISTRY_PATH",
        "path",
        "works",
        "_works",
        "load",
        "get",
        "find_work",
    ):
        show_attribute(registry, name)

    # ------------------------------------------------------------------
    # 5. Registry path
    # ------------------------------------------------------------------

    section("5. DEFAULT REGISTRY PATH")

    registry_path = getattr(
        registry,
        "DEFAULT_REGISTRY_PATH",
        None,
    )

    print(
        "DEFAULT_REGISTRY_PATH :",
        registry_path,
    )

    # ------------------------------------------------------------------
    # 6. Load
    # ------------------------------------------------------------------

    section("6. REGISTRY LOAD")

    if not hasattr(registry, "load"):
        raise RuntimeError(
            "WorkRegistry.load() is not available."
        )

    try:
        loaded = registry.load()
    except Exception as exc:
        print("WorkRegistry.load() : FAIL")
        print("ERROR :", repr(exc))
        raise

    print("WorkRegistry.load() : PASS")
    print("Returned type :", type(loaded))
    print("Returned repr :", repr(loaded))

    # ------------------------------------------------------------------
    # 7. Amarakośa lookup
    # ------------------------------------------------------------------

    section("7. AMARAKOŚA WORK LOOKUP")

    if not hasattr(registry, "get"):
        raise RuntimeError(
            "WorkRegistry.get() is not available."
        )

    identifiers = (
        "amarakosha",
        "Amarakosha",
        "अमरकोश",
        "amarakosa",
    )

    for identifier in identifiers:

        try:
            result = registry.get(identifier)
        except Exception as exc:
            print(
                f"get({identifier!r}) -> ERROR: {exc!r}"
            )
            continue

        print(
            f"get({identifier!r}) -> "
            f"{result!r}"
        )

    # ------------------------------------------------------------------
    # 8. find_work
    # ------------------------------------------------------------------

    section("8. FIND_WORK LOOKUP")

    if hasattr(registry, "find_work"):

        for query in (
            "Amarakosha",
            "अमरकोश",
        ):

            try:
                result = registry.find_work(query)
            except Exception as exc:
                print(
                    f"find_work({query!r}) -> "
                    f"ERROR: {exc!r}"
                )
                continue

            print(
                f"find_work({query!r}) -> "
                f"{result!r}"
            )

    else:
        print(
            "find_work() : <ABSENT>"
        )

    # ------------------------------------------------------------------
    # 9. WorkDefinition inspection
    # ------------------------------------------------------------------

    section("9. AMARAKOŚA WORKDEFINITION ATTRIBUTES")

    amarakosha = None

    for identifier in identifiers:

        try:
            candidate = registry.get(identifier)
        except Exception:
            continue

        if candidate is not None:
            amarakosha = candidate
            print(
                "Selected lookup key :",
                identifier,
            )
            break

    if amarakosha is None:
        print(
            "Amarakośa WorkDefinition was not resolved "
            "through registry.get()."
        )
        print(
            "This is an AUDIT RESULT, not a repair."
        )
    else:

        print(
            "Resolved object type :",
            type(amarakosha),
        )

        for name in (
            "identifier",
            "id",
            "title",
            "name",
            "corpus_type",
            "language",
            "script",
            "repository",
            "metadata",
            "description",
            "source",
            "sources",
        ):
            show_attribute(
                amarakosha,
                name,
            )

    # ------------------------------------------------------------------
    # 10. Final
    # ------------------------------------------------------------------

    print()
    print("=" * 112)
    print("BATCH 5H-5E-11R — TRACE COMPLETE")
    print("=" * 112)
    print()
    print("No production mutation performed.")
    print("No WorkRegistry modification performed.")
    print("No WorkDefinition modification performed.")
    print()


if __name__ == "__main__":
    main()


