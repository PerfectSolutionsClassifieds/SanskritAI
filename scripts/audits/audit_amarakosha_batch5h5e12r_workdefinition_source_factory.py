from __future__ import annotations

"""
BATCH 5H-5E-12R
================

WorkDefinition -> CorpusSourceFactory compatibility audit.

Repository-verified paths
-------------------------

WorkRegistry:

    SanskritAI.acquisition.metadata.registries.work_registry

WorkDefinition:

    SanskritAI.acquisition.metadata.models.work_definition

CorpusSourceFactory:

    SanskritAI.acquisition.factories.corpus_source_factory

CorpusSource:

    SanskritAI.acquisition.models.corpus_source

READ-ONLY.

No production mutation is performed.
No acquisition is performed.
No remote source is accessed.
No new Amarakośa class is created.
"""

from pathlib import Path
import inspect
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


def show_attribute(
    obj,
    name: str,
) -> None:

    if not hasattr(
        obj,
        name,
    ):
        print(
            f"{name:30} -> <ABSENT>"
        )
        return

    try:
        value = getattr(
            obj,
            name,
        )
    except Exception as exc:
        print(
            f"{name:30} -> ERROR {exc!r}"
        )
        return

    print(
        f"{name:30} -> {value!r}"
    )


def main() -> None:

    print("=" * 112)
    print(
        "BATCH 5H-5E-12R — "
        "WORKDEFINITION → CORPUSSOURCEFACTORY AUDIT"
    )
    print("=" * 112)

    # =========================================================================
    # 1. PACKAGE BOOTSTRAP
    # =========================================================================

    section("1. PACKAGE BOOTSTRAP")

    print(
        "Project root   :",
        PROJECT_ROOT,
    )

    print(
        "Package parent :",
        PACKAGE_PARENT,
    )

    if str(PACKAGE_PARENT) not in sys.path:
        raise RuntimeError(
            "Package bootstrap failed."
        )

    import SanskritAI

    print(
        "SanskritAI import : PASS"
    )

    # =========================================================================
    # 2. CORRECT REPOSITORY-VERIFIED IMPORTS
    # =========================================================================

    section("2. EXISTING ACQUISITION ABSTRACTIONS")

    from SanskritAI.acquisition.metadata.registries.work_registry import (
        WorkRegistry,
    )

    from SanskritAI.acquisition.metadata.models.work_definition import (
        WorkDefinition,
    )

    from SanskritAI.acquisition.factories.corpus_source_factory import (
        CorpusSourceFactory,
    )

    from SanskritAI.acquisition.models.corpus_source import (
        CorpusSource,
    )

    print(
        "WorkRegistry import : PASS"
    )

    print(
        "WorkDefinition import : PASS"
    )

    print(
        "CorpusSourceFactory import : PASS"
    )

    print(
        "CorpusSource import : PASS"
    )

    # =========================================================================
    # 3. RESOLVE AMARAKOŚA WORK
    # =========================================================================

    section("3. RESOLVE AMARAKOŚA WORK")

    registry = WorkRegistry()

    print(
        "WorkRegistry construction : PASS"
    )

    amarakosha = registry.get(
        "amarakosha"
    )

    print(
        "registry.get('amarakosha') ->",
        amarakosha,
    )

    if amarakosha is None:

        print(
            "Canonical identifier 'amarakosha' was not resolved."
        )

        print(
            "Trying find_work('Amarakosha')."
        )

        amarakosha = registry.find_work(
            "Amarakosha"
        )

    if amarakosha is None:

        print(
            "Amarakośa WorkDefinition could not be resolved."
        )

        print(
            "This is an AUDIT RESULT."
        )

        return

    print(
        "Resolved object type :",
        type(amarakosha),
    )

    if not isinstance(
        amarakosha,
        WorkDefinition,
    ):
        raise RuntimeError(
            "Resolved Amarakośa object is not a "
            "WorkDefinition."
        )

    print(
        "WorkDefinition type check : PASS"
    )

    # =========================================================================
    # 4. WORKDEFINITION CONTRACT
    # =========================================================================

    section("4. WORKDEFINITION CONTRACT")

    print(
        "WorkDefinition module :",
        type(amarakosha).__module__,
    )

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
    # 5. CORPUSSOURCEFACTORY CONTRACT
    # =========================================================================

    section("5. CORPUSSOURCEFACTORY CONTRACT")

    print(
        "Factory type :",
        CorpusSourceFactory,
    )

    print(
        "Factory module :",
        CorpusSourceFactory.__module__,
    )

    # =========================================================================
    # 6. FACTORY CALLABLE DISCOVERY
    # =========================================================================

    section("6. FACTORY CALLABLE DISCOVERY")

    callable_names = []

    for name in dir(
        CorpusSourceFactory
    ):

        if name.startswith("_"):
            continue

        try:
            value = getattr(
                CorpusSourceFactory,
                name,
            )
        except Exception:
            continue

        if callable(value):

            callable_names.append(
                name
            )

            try:
                signature = inspect.signature(
                    value
                )
            except Exception:
                signature = (
                    "<signature unavailable>"
                )

            print(
                f"{name:40} {signature}"
            )

    if not callable_names:
        print(
            "No public callable factory members discovered."
        )

    # =========================================================================
    # 7. CORPUSSOURCE CONTRACT
    # =========================================================================

    section("7. CORPUSSOURCE CONTRACT")

    print(
        "CorpusSource type :",
        CorpusSource,
    )

    print(
        "CorpusSource module :",
        CorpusSource.__module__,
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
                f"{name:30} -> PRESENT"
            )
        else:
            print(
                f"{name:30} -> ABSENT"
            )

    # =========================================================================
    # 8. FACTORY SOURCE INSPECTION
    # =========================================================================

    section("8. FACTORY SOURCE INSPECTION")

    factory_file = Path(
        inspect.getfile(
            CorpusSourceFactory
        )
    )

    print(
        "Factory source file :",
        factory_file,
    )

    if factory_file.exists():

        print(
            "Factory source exists : PASS"
        )

        factory_source = factory_file.read_text(
            encoding="utf-8"
        )

        print(
            "Factory source size :",
            len(factory_source),
            "characters",
        )

        print()
        print(
            "Factory source references:"
        )

        for index, line in enumerate(
            factory_source.splitlines(),
            start=1,
        ):

            if any(
                token in line
                for token in (
                    "WorkDefinition",
                    "CorpusSource",
                    "SourceFormat",
                    "create",
                    "build",
                    "from_",
                )
            ):

                print(
                    f"{index:4}: {line}"
                )

    # =========================================================================
    # 9. WORKDEFINITION → FACTORY BOUNDARY
    # =========================================================================

    section("9. WORKDEFINITION → FACTORY BOUNDARY")

    print(
        "Resolved WorkDefinition:"
    )

    print(
        "  identifier :",
        getattr(
            amarakosha,
            "identifier",
            None,
        ),
    )

    print(
        "  title      :",
        getattr(
            amarakosha,
            "title",
            None,
        ),
    )

    print(
        "  corpus_type:",
        getattr(
            amarakosha,
            "corpus_type",
            None,
        ),
    )

    print(
        "  language   :",
        getattr(
            amarakosha,
            "language",
            None,
        ),
    )

    print(
        "  script     :",
        getattr(
            amarakosha,
            "script",
            None,
        ),
    )

    print()
    print(
        "No factory construction is performed automatically."
    )

    print(
        "No acquisition request is created."
    )

    print(
        "No provider is invoked."
    )

    print(
        "No remote source is accessed."
    )

    # =========================================================================
    # 10. FINAL
    # =========================================================================

    print()
    print("=" * 112)
    print(
        "BATCH 5H-5E-12R — AUDIT COMPLETE"
    )
    print("=" * 112)
    print()

    print(
        "Repository-verified WorkRegistry path:"
    )

    print(
        "  SanskritAI.acquisition.metadata.registries.work_registry"
    )

    print()
    print(
        "Repository-verified WorkDefinition path:"
    )

    print(
        "  SanskritAI.acquisition.metadata.models.work_definition"
    )

    print()
    print(
        "CorpusSourceFactory path:"
    )

    print(
        "  SanskritAI.acquisition.factories.corpus_source_factory"
    )

    print()
    print(
        "No production mutation performed."
    )

    print(
        "No new Amarakośa abstraction created."
    )

    print(
        "No acquisition performed."
    )

    print()


if __name__ == "__main__":
    main()
