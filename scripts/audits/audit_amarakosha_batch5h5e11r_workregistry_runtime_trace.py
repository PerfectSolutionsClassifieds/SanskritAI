from __future__ import annotations

"""
BATCH 5H-5E-11R
================

WorkRegistry -> WorkDefinition runtime trace.

Repository-verified paths
-------------------------

    SanskritAI.acquisition.metadata.registries.work_registry
    SanskritAI.acquisition.metadata.models.work_definition

This is a READ-ONLY runtime audit.

No production files are modified.
No registry entries are modified.
No acquisition is performed.
No new classes are created.
"""

from pathlib import Path
import sys


# =============================================================================
# 0. PACKAGE BOOTSTRAP
# =============================================================================

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
            print(f"{name:28} -> <ERROR: {exc!r}>")
            return

        print(f"{name:28} -> {value!r}")
    else:
        print(f"{name:28} -> <ABSENT>")


def main() -> None:

    print("=" * 112)
    print("BATCH 5H-5E-11R — WORKREGISTRY RUNTIME TRACE")
    print("=" * 112)

    # =========================================================================
    # 1. PACKAGE BOOTSTRAP
    # =========================================================================

    section("1. PACKAGE BOOTSTRAP")

    print("Project root   :", PROJECT_ROOT)
    print("Package parent :", PACKAGE_PARENT)

    if str(PACKAGE_PARENT) not in sys.path:
        raise RuntimeError(
            "Package bootstrap failed: /content is not on sys.path."
        )

    import SanskritAI

    print("SanskritAI import : PASS")

    # =========================================================================
    # 2. CORRECT REPOSITORY-VERIFIED IMPORT PATH
    # =========================================================================

    section("2. WORKREGISTRY IMPORT")

    from SanskritAI.acquisition.metadata.registries.work_registry import (
        WorkRegistry,
    )

    print(
        "WorkRegistry import : PASS"
    )

    print(
        "WorkRegistry module :",
        WorkRegistry.__module__,
    )

    # =========================================================================
    # 3. WORKDEFINITION IMPORT
    # =========================================================================

    section("3. WORKDEFINITION IMPORT")

    from SanskritAI.acquisition.metadata.models.work_definition import (
        WorkDefinition,
    )

    print(
        "WorkDefinition import : PASS"
    )

    print(
        "WorkDefinition module :",
        WorkDefinition.__module__,
    )

    # =========================================================================
    # 4. REGISTRY CONSTRUCTION
    # =========================================================================

    section("4. WORKREGISTRY CONSTRUCTION")

    registry = WorkRegistry()

    print(
        "WorkRegistry construction : PASS"
    )

    print(
        "Registry repr :",
        registry,
    )

    # =========================================================================
    # 5. REGISTRY RUNTIME STRUCTURE
    # =========================================================================

    section("5. WORKREGISTRY RUNTIME STRUCTURE")

    print(
        "Registry type :",
        type(registry),
    )

    print(
        "Registry module :",
        type(registry).__module__,
    )

    for name in (
        "DEFAULT_REGISTRY_PATH",
        "_registry_path",
        "load",
        "get",
        "find_work",
        "exists",
        "identifiers",
        "titles",
        "search",
        "corpus_types",
        "works_by_corpus_type",
    ):
        show_attribute(
            registry,
            name,
        )

    # =========================================================================
    # 6. DEFAULT REGISTRY PATH
    # =========================================================================

    section("6. DEFAULT REGISTRY PATH")

    registry_path = getattr(
        registry,
        "DEFAULT_REGISTRY_PATH",
        None,
    )

    print(
        "DEFAULT_REGISTRY_PATH :",
        registry_path,
    )

    private_registry_path = getattr(
        registry,
        "_registry_path",
        None,
    )

    print(
        "_registry_path         :",
        private_registry_path,
    )

    # =========================================================================
    # 7. LOAD
    # =========================================================================

    section("7. REGISTRY LOAD")

    loaded = registry.load()

    print(
        "WorkRegistry.load() : PASS"
    )

    print(
        "Returned type :",
        type(loaded),
    )

    print(
        "Returned count :",
        len(loaded),
    )

    print(
        "Returned type expected : tuple"
    )

    if not isinstance(
        loaded,
        tuple,
    ):
        raise RuntimeError(
            f"Expected WorkRegistry.load() to return tuple, "
            f"got {type(loaded)!r}"
        )

    # =========================================================================
    # 8. REGISTRY IDENTIFIERS
    # =========================================================================

    section("8. REGISTERED WORK IDENTIFIERS")

    if hasattr(
        registry,
        "identifiers",
    ):
        identifiers = registry.identifiers()

        print(
            "Identifiers type :",
            type(identifiers),
        )

        print(
            "Identifiers count :",
            len(identifiers),
        )

        for identifier in identifiers:
            print(
                "  -",
                identifier,
            )

    # =========================================================================
    # 9. AMARAKOŚA DIRECT IDENTIFIER LOOKUP
    # =========================================================================

    section("9. AMARAKOŚA DIRECT IDENTIFIER LOOKUP")

    amarakosha = registry.get(
        "amarakosha"
    )

    print(
        "registry.get('amarakosha') :",
        amarakosha,
    )

    if amarakosha is None:
        print(
            "Amarakośa was not found by canonical identifier."
        )
    else:

        print(
            "Resolved type :",
            type(amarakosha),
        )

        if not isinstance(
            amarakosha,
            WorkDefinition,
        ):
            raise RuntimeError(
                "registry.get('amarakosha') did not return "
                "a WorkDefinition."
            )

        print(
            "WorkDefinition type check : PASS"
        )

    # =========================================================================
    # 10. FIND WORK
    # =========================================================================

    section("10. FIND_WORK LOOKUP")

    for query in (
        "Amarakosha",
        "अमरकोश",
    ):

        result = registry.find_work(
            query
        )

        print(
            f"find_work({query!r}) ->",
            result,
        )

        if result is not None:
            print(
                "  type       :",
                type(result),
            )

            print(
                "  identifier :",
                result.identifier,
            )

            print(
                "  title      :",
                result.title,
            )

    # =========================================================================
    # 11. AMARAKOŚA WORKDEFINITION CONTRACT
    # =========================================================================

    section("11. AMARAKOŚA WORKDEFINITION ATTRIBUTES")

    if amarakosha is not None:

        for name in (
            "identifier",
            "title",
            "corpus_type",
            "language",
            "script",
            "description",
            "aliases",
            "metadata",
            "repository",
            "source",
            "sources",
        ):
            show_attribute(
                amarakosha,
                name,
            )

    # =========================================================================
    # 12. LOADED WORK OBJECTS
    # =========================================================================

    section("12. LOADED WORK OBJECT TYPES")

    for index, work in enumerate(
        loaded,
        start=1,
    ):

        print(
            f"{index:4}. "
            f"{type(work).__name__} "
            f"identifier={getattr(work, 'identifier', None)!r} "
            f"title={getattr(work, 'title', None)!r}"
        )

    # =========================================================================
    # 13. FINAL
    # =========================================================================

    print()
    print("=" * 112)
    print("BATCH 5H-5E-11R — TRACE COMPLETE")
    print("=" * 112)
    print()
    print("Repository path verified:")
    print(
        "  SanskritAI.acquisition.metadata.registries.work_registry"
    )
    print()
    print("WorkDefinition path verified:")
    print(
        "  SanskritAI.acquisition.metadata.models.work_definition"
    )
    print()
    print("No production mutation performed.")
    print("No WorkRegistry modification performed.")
    print("No WorkDefinition modification performed.")
    print("No acquisition performed.")
    print()


if __name__ == "__main__":
    main()
