from __future__ import annotations

"""
BATCH 5H-5E-12R
SourceType ↔ CorpusSourceFactory Compatibility Audit

READ-ONLY.

Purpose
-------
Audit the canonical SourceType contract against the existing
CorpusSourceFactory and production acquisition consumers.

This audit MUST NOT:
- modify SourceType
- modify CorpusSourceFactory
- modify CorpusSource
- create new abstractions
- perform acquisition
- modify registry/work definitions

The audit explicitly checks whether LOCAL / REMOTE are stale
consumer-side references and identifies the canonical semantic
mapping already supported by the architecture.
"""

# from __future__ import annotations

import inspect
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path("/content/SanskritAI")
PACKAGE_PARENT = PROJECT_ROOT.parent


def section(title: str) -> None:
    print()
    print("-" * 112)
    print(title)
    print("-" * 112)


def bootstrap() -> None:
    if str(PACKAGE_PARENT) not in sys.path:
        sys.path.insert(0, str(PACKAGE_PARENT))


def production_python_files() -> list[Path]:
    """
    Return production Python files only.

    Ignore:
    - tests/
    - __pycache__/
    - historical numeric suffix files: *1.py, *2.py, ...
    - _G<number>.py
    """
    files: list[Path] = []

    numeric_suffix = re.compile(r".*\d+\.py$")
    generation_suffix = re.compile(r".*_G\d+\.py$")

    for path in PROJECT_ROOT.rglob("*.py"):
        relative = path.relative_to(PROJECT_ROOT)

        if "__pycache__" in relative.parts:
            continue

        if "tests" in relative.parts:
            continue

        if numeric_suffix.match(path.name):
            continue

        if generation_suffix.match(path.name):
            continue

        files.append(path)

    return sorted(files)


def find_source_type_references() -> list[tuple[Path, int, str]]:
    matches: list[tuple[Path, int, str]] = []

    pattern = re.compile(r"\bSourceType\.[A-Z][A-Z0-9_]*\b")

    for path in production_python_files():
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        for line_number, line in enumerate(text.splitlines(), start=1):
            if "SourceType." in line:
                for match in pattern.finditer(line):
                    matches.append(
                        (path, line_number, match.group(0))
                    )

    return matches


def main() -> None:
    print("=" * 112)
    print("BATCH 5H-5E-12R — SOURCETYPE COMPATIBILITY AUDIT")
    print("=" * 112)

    section("1. PACKAGE BOOTSTRAP")

    bootstrap()

    print(f"Project root   : {PROJECT_ROOT}")
    print(f"Package parent : {PACKAGE_PARENT}")

    try:
        import SanskritAI  # noqa: F401

        print("SanskritAI import : PASS")
    except Exception as exc:
        print(f"SanskritAI import : FAIL")
        print(f"Exception          : {exc!r}")
        raise

    section("2. CANONICAL SOURCETYPE IMPORT")

    from SanskritAI.acquisition.models.source_type import SourceType

    print("SourceType import : PASS")
    print(f"Module            : {SourceType.__module__}")

    section("3. CANONICAL SOURCETYPE MEMBERS")

    members = list(SourceType)

    print(f"Member count : {len(members)}")

    for member in members:
        print(f"  - {member.name:<15} = {member.value!r}")

    section("4. EXPECTED STALE MEMBERS")

    for name in (
        "LOCAL",
        "REMOTE",
    ):
        exists = hasattr(SourceType, name)
        print(f"SourceType.{name:<8} exists : {exists}")

    section("5. SEMANTIC SOURCE TYPES")

    semantic_names = (
        "LEXICON",
        "CORPUS",
        "GRAMMAR",
        "COMMENTARY",
        "ONTOLOGY",
        "METADATA",
        "DATASET",
        "COLLECTION",
        "UNKNOWN",
    )

    for name in semantic_names:
        print(
            f"SourceType.{name:<12} : "
            f"{getattr(SourceType, name, '<ABSENT>')}"
        )

    section("6. CORPUSSOURCE IMPORT")

    from SanskritAI.acquisition.models.corpus_source import CorpusSource

    print("CorpusSource import : PASS")
    print(f"Module              : {CorpusSource.__module__}")

    print()
    print("CorpusSource annotations:")

    try:
        annotations = inspect.get_annotations(
            CorpusSource,
            eval_str=True,
        )
    except Exception as exc:
        annotations = {}
        print(f"  annotation inspection failed: {exc!r}")

    for name, annotation in annotations.items():
        print(f"  {name:<20} -> {annotation!r}")

    section("7. CORPUSSOURCE FACTORY SOURCE — READ ONLY")

    factory_path = (
        PROJECT_ROOT
        / "acquisition"
        / "factories"
        / "corpus_source_factory.py"
    )

    print(f"Factory path : {factory_path}")

    source = factory_path.read_text(encoding="utf-8")

    for line_number, line in enumerate(source.splitlines(), start=1):
        if "SourceType." in line:
            print(f"{line_number:>4}: {line}")

    section("8. PRODUCTION SOURCETYPE REFERENCES")

    references = find_source_type_references()

    print(f"Reference count : {len(references)}")

    for path, line_number, reference in references:
        relative = path.relative_to(PROJECT_ROOT)

        print(
            f"{relative}:{line_number} -> {reference}"
        )

    section("9. STALE LOCAL / REMOTE REFERENCES")

    stale = [
        item
        for item in references
        if item[2] in {
            "SourceType.LOCAL",
            "SourceType.REMOTE",
        }
    ]

    print(f"Stale LOCAL/REMOTE reference count : {len(stale)}")

    for path, line_number, reference in stale:
        print(
            f"  {path.relative_to(PROJECT_ROOT)}:"
            f"{line_number} -> {reference}"
        )

    section("10. CORPUSSOURCE FACTORY IMPORT — CURRENT RUNTIME")

    try:
        from SanskritAI.acquisition.factories.corpus_source_factory import (
            CorpusSourceFactory,
        )

        print("CorpusSourceFactory import : PASS")
        print(f"Module : {CorpusSourceFactory.__module__}")

    except Exception as exc:
        print("CorpusSourceFactory import : FAIL")
        print(f"Exception : {exc!r}")

        section("11. CURRENT RUNTIME DIAGNOSIS")

        print(
            "The factory currently cannot be imported because one or more "
            "consumer-side SourceType members are absent from the canonical "
            "SourceType enum."
        )

        print()
        print("No production mutation performed.")

        return

    section("12. FACTORY PUBLIC CALLABLES")

    for name in (
        "from_file",
        "from_url",
        "from_metadata",
        "is_supported",
    ):
        member = getattr(CorpusSourceFactory, name, None)

        print(f"{name:<20} -> {member}")

        if callable(member):
            try:
                print(
                    f"  signature : "
                    f"{inspect.signature(member)}"
                )
            except Exception as exc:
                print(f"  signature : <unavailable: {exc!r}>")

    section("13. DEFAULT SOURCE TYPES")

    for method_name in (
        "from_file",
        "from_url",
    ):
        method = getattr(CorpusSourceFactory, method_name, None)

        if method is None:
            continue

        try:
            signature = inspect.signature(method)

            parameter = signature.parameters.get("source_type")

            if parameter is None:
                print(
                    f"{method_name}: source_type parameter ABSENT"
                )
            else:
                print(
                    f"{method_name}: "
                    f"default={parameter.default!r}"
                )

        except Exception as exc:
            print(
                f"{method_name}: signature inspection failed "
                f"{exc!r}"
            )

    section("14. DIAGNOSTIC CONCLUSION")

    if stale:
        print(
            "DIAGNOSIS: CorpusSourceFactory contains stale "
            "SourceType.LOCAL / SourceType.REMOTE references."
        )
        print()
        print(
            "The canonical SourceType is semantic rather than "
            "transport/location based."
        )
        print()
        print(
            "Do NOT add LOCAL or REMOTE to SourceType during this audit."
        )
        print()
        print(
            "Next step: determine the existing canonical semantic "
            "mapping for local-file and remote-URL construction "
            "before applying the smallest consumer-side repair."
        )
    else:
        print(
            "No stale SourceType.LOCAL / SourceType.REMOTE "
            "references found."
        )

    print()
    print("No production mutation performed.")
    print("No SourceType modification performed.")
    print("No CorpusSourceFactory modification performed.")
    print("No acquisition performed.")

    print()
    print("=" * 112)
    print("BATCH 5H-5E-12R — AUDIT COMPLETE")
    print("=" * 112)


if __name__ == "__main__":
    main()
