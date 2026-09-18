from __future__ import annotations

"""
BATCH 5H-5E-12R
================

WorkDefinition -> CorpusSourceFactory compatibility audit.

READ-ONLY.

This audit does not create an Amarakośa provider, source, parser,
manifest, or acquisition implementation.

It determines whether the existing WorkDefinition can actually be
translated into the existing CorpusSourceFactory contract.
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


def show(obj, name: str) -> None:

    if not hasattr(obj, name):
        print(
            f"{name:24} -> <ABSENT>"
        )
        return

    try:
        value = getattr(obj, name)
    except Exception as exc:
        print(
            f"{name:24} -> ERROR {exc!r}"
        )
        return

    print(
        f"{name:24} -> {value!r}"
    )


def main() -> None:

    print("=" * 112)
    print(
        "BATCH 5H-5E-12R — "
        "WORKDEFINITION → CORPUSSOURCEFACTORY AUDIT"
    )
    print("=" * 112)

    # ------------------------------------------------------------------
    # 1. Bootstrap
    # ------------------------------------------------------------------

    section("1. PACKAGE BOOTSTRAP")

    import SanskritAI

    print(
        "SanskritAI import : PASS"
    )

    # ------------------------------------------------------------------
    # 2. Imports
    # ------------------------------------------------------------------

    section("2. EXISTING ACQUISITION ABSTRACTIONS")

    from SanskritAI.acquisition.registries.work_registry import (
        WorkRegistry,
    )

    from SanskritAI.acquisition.factories.corpus_source_factory import (
        CorpusSourceFactory,
    )

    from SanskritAI.acquisition.models.corpus_source import (
        CorpusSource,
    )

    from SanskritAI.acquisition.models.work_definition import (
        WorkDefinition,
    )

    print(
        "WorkRegistry import : PASS"
    )

    print(
        "CorpusSourceFactory import : PASS"
    )

    print(
        "CorpusSource import : PASS"
    )

    print(
        "WorkDefinition import : PASS"
    )

    # ------------------------------------------------------------------
    # 3. Registry
    # ------------------------------------------------------------------

    section("3. RESOLVE AMARAKOŚA WORK")

    registry = WorkRegistry()

    amarakosha = None

    for identifier in (
        "amarakosha",
        "Amarakosha",
        "अमरकोश",
        "amarakosa",
    ):

        try:
            candidate = registry.get(identifier)
        except Exception as exc:
            print(
                f"get({identifier!r}) -> ERROR {exc!r}"
            )
            continue

        if candidate is not None:
            amarakosha = candidate
            print(
                f"Resolved through get({identifier!r})"
            )
            break

    if amarakosha is None:
        print(
            "Amarakośa WorkDefinition could not be resolved."
        )
        print(
            "Audit cannot proceed beyond the registry boundary."
        )
        return

    print(
        "Resolved type :",
        type(amarakosha),
    )

    if not isinstance(
        amarakosha,
        WorkDefinition,
    ):
        print(
            "WARNING: resolved object is not an instance "
            "of WorkDefinition."
        )

    # ------------------------------------------------------------------
    # 4. WorkDefinition fields
    # ------------------------------------------------------------------

    section("4. WORKDEFINITION CONTRACT")

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
        show(
            amarakosha,
            name,
        )

    # ------------------------------------------------------------------
    # 5. CorpusSourceFactory API
    # ------------------------------------------------------------------

    section("5. CORPUSSOURCEFACTORY CONTRACT")

    factory_type = CorpusSourceFactory

    print(
        "Factory type :",
        factory_type,
    )

    print(
        "Factory module :",
        factory_type.__module__,
    )

    for name in (
        "create",
        "build",
        "from_work",
        "from_definition",
        "create_source",
    ):
        if hasattr(factory_type, name):
            print(
                f"{name:24} -> PRESENT"
            )
        else:
            print(
                f"{name:24} -> ABSENT"
            )

    # ------------------------------------------------------------------
    # 6. Static callable signatures
    # ------------------------------------------------------------------

    section("6. FACTORY CALLABLE DISCOVERY")

    import inspect

    for name in dir(factory_type):

        if name.startswith("_"):
            continue

        try:
            value = getattr(
                factory_type,
                name,
            )
        except Exception:
            continue

        if callable(value):

            try:
                signature = inspect.signature(
                    value
                )
            except Exception:
                signature = "<signature unavailable>"

            print(
                f"{name:32} {signature}"
            )

    # ------------------------------------------------------------------
    # 7. Existing source object contract
    # ------------------------------------------------------------------

    section("7. CORPUSSOURCE CONTRACT")

    print(
        "CorpusSource type :",
        CorpusSource,
    )

    for name in (
        "identifier",
        "format",
        "uri",
        "path",
        "metadata",
        "work",
        "work_id",
    ):
        if hasattr(
            CorpusSource,
            name,
        ):
            print(
                f"{name:24} -> PRESENT"
            )
        else:
            print(
                f"{name:24} -> ABSENT"
            )

    # ------------------------------------------------------------------
    # 8. IMPORTANT
    # ------------------------------------------------------------------

    section("8. AUDIT BOUNDARY")

    print(
        "No CorpusSourceFactory call is made automatically."
    )

    print(
        "No acquisition is performed."
    )

    print(
        "No remote source is accessed."
    )

    print(
        "No new Amarakośa class is created."
    )

    print(
        "The purpose is to establish the actual runtime "
        "WorkDefinition → Factory contract before implementation."
    )

    # ------------------------------------------------------------------
    # 9. Final
    # ------------------------------------------------------------------

    print()
    print("=" * 112)
    print(
        "BATCH 5H-5E-12R — AUDIT COMPLETE"
    )
    print("=" * 112)
    print()
    print(
        "Next implementation should be selected from the "
        "actual runtime contract discovered above."
    )
    print()


if __name__ == "__main__":
    main()

