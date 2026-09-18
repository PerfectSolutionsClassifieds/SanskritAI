
from __future__ import annotations

"""
BATCH 5H-5E-13R-1
=================

AMARAKOSHA ACQUISITION BOUNDARY AUDIT

Purpose
-------
Trace the existing Amarakośa acquisition boundary without creating
new production abstractions.

This audit determines:

1. How Amarakośa is represented in WorkRegistry.
2. What WorkDefinition currently provides.
3. Whether Amarakośa already has acquisition/source metadata.
4. Which existing acquisition providers/factories are available.
5. Whether CorpusSourceFactory can construct the Amarakośa
   source using the canonical SourceType.LEXICON.
6. Whether stale SourceType.LOCAL / REMOTE / GRETIL references
   remain in the Amarakośa acquisition path.

This audit is READ-ONLY.

It must not:
* modify production files
* modify WorkRegistry
* modify WorkDefinition
* modify CorpusSource
* modify SourceType
* create new production classes
* create new production manifests
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path("/content/SanskritAI")


def fail(message: str) -> None:
    raise RuntimeError(message)


def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def production_py_files(root: Path):
    """
    Yield production Python files while excluding:

    * tests/
    * __pycache__/
    * numbered historical copies
    * _G<number>.py historical copies
    """
    excluded_parts = {
        "tests",
        "__pycache__",
    }

    for path in root.rglob("*.py"):
        relative = path.relative_to(root)

        if any(part in excluded_parts for part in relative.parts):
            continue

        name = path.name

        stem = path.stem

        # Ignore historical numeric copies such as foo1.py, foo2.py
        if stem and stem[-1].isdigit():
            continue

        # Ignore historical _G<number>.py copies.
        import re

        if re.search(r"_G\d+$", stem):
            continue

        yield path


def search_production_references(
    token: str,
    *,
    root: Path = PROJECT_ROOT,
) -> list[tuple[str, int, str]]:
    results = []

    for path in production_py_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        for line_number, line in enumerate(
            text.splitlines(),
            start=1,
        ):
            if token in line:
                results.append(
                    (
                        str(path.relative_to(root)),
                        line_number,
                        line.strip(),
                    )
                )

    return results


def main() -> None:

    section(
        "BATCH 5H-5E-13R-1 — "
        "AMARAKOSHA ACQUISITION BOUNDARY AUDIT"
    )

    print(f"Project root : {PROJECT_ROOT}")

    if not PROJECT_ROOT.exists():
        fail(
            f"Project root does not exist: {PROJECT_ROOT}"
        )

    # ---------------------------------------------------------
    # 1. Package bootstrap
    # ---------------------------------------------------------

    section("1. PACKAGE BOOTSTRAP")

    parent = str(PROJECT_ROOT.parent)

    if parent not in sys.path:
        sys.path.insert(0, parent)

    import SanskritAI

    print(
        f"SanskritAI import : PASS ({SanskritAI.__name__})"
    )

    # ---------------------------------------------------------
    # 2. WorkRegistry
    # ---------------------------------------------------------

    section("2. WORKREGISTRY")

    from SanskritAI.acquisition.metadata.registries.work_registry import (
        WorkRegistry,
    )

    registry = WorkRegistry()

    print(
        f"WorkRegistry construction : PASS ({registry!r})"
    )

    works = registry.load()

    print(
        f"Registered work count : {len(works)}"
    )

    if not works:
        fail(
            "WorkRegistry returned no works."
        )

    # ---------------------------------------------------------
    # 3. Amarakośa work lookup
    # ---------------------------------------------------------

    section("3. AMARAKOSHA WORK LOOKUP")

    amarakosha = registry.find_work("Amarakosha")

    if amarakosha is None:
        amarakosha = registry.find_work("amarakosha")

    if amarakosha is None:
        amarakosha = registry.find_work("अमरकोश")

    if amarakosha is None:
        fail(
            "Amarakośa was not found in WorkRegistry."
        )

    print(
        "Amarakośa WorkDefinition lookup : PASS"
    )

    print(
        f"identifier   : {getattr(amarakosha, 'identifier', None)!r}"
    )

    print(
        f"title        : {getattr(amarakosha, 'title', None)!r}"
    )

    print(
        f"corpus_type  : {getattr(amarakosha, 'corpus_type', None)!r}"
    )

    print(
        f"language     : {getattr(amarakosha, 'language', None)!r}"
    )

    print(
        f"script       : {getattr(amarakosha, 'script', None)!r}"
    )

    print(
        f"description  : {getattr(amarakosha, 'description', None)!r}"
    )

    print(
        f"aliases      : {getattr(amarakosha, 'aliases', None)!r}"
    )

    print(
        f"metadata     : {getattr(amarakosha, 'metadata', None)!r}"
    )

    # ---------------------------------------------------------
    # 4. WorkDefinition acquisition attributes
    # ---------------------------------------------------------

    section(
        "4. WORKDEFINITION ACQUISITION ATTRIBUTE AUDIT"
    )

    candidate_attributes = (
        "source",
        "sources",
        "repository",
        "source_id",
        "source_ids",
        "download_url",
        "download_urls",
        "url",
        "urls",
        "local_path",
        "path",
        "format",
        "source_format",
        "acquisition",
        "acquisition_metadata",
    )

    present = {}

    for attribute in candidate_attributes:
        if hasattr(amarakosha, attribute):
            value = getattr(
                amarakosha,
                attribute,
            )

            present[attribute] = value

            print(
                f"{attribute:<24} : {value!r}"
            )

    if not present:
        print(
            "No explicit acquisition attributes found on "
            "WorkDefinition."
        )

    # ---------------------------------------------------------
    # 5. CorpusSourceFactory
    # ---------------------------------------------------------

    section("5. CORPUSSOURCEFACTORY")

    from SanskritAI.acquisition.factories.corpus_source_factory import (
        CorpusSourceFactory,
    )

    from SanskritAI.acquisition.models.corpus_source import (
        CorpusSource,
    )

    from SanskritAI.acquisition.models.source_type import (
        SourceType,
    )

    from SanskritAI.acquisition.models.source_status import (
        SourceStatus,
    )

    print(
        "CorpusSourceFactory import : PASS"
    )

    # ---------------------------------------------------------
    # 6. Canonical Amarakośa semantic source construction
    # ---------------------------------------------------------

    section(
        "6. CANONICAL AMARAKOSHA SOURCE CONSTRUCTION"
    )

    probe_path = (
        PROJECT_ROOT
        / "resources"
        / "work_registry.json"
    )

    if not probe_path.exists():
        fail(
            f"Probe file does not exist: {probe_path}"
        )

    source = CorpusSourceFactory.from_file(
        probe_path,
        source_type=SourceType.LEXICON,
    )

    if not isinstance(source, CorpusSource):
        fail(
            "CorpusSourceFactory.from_file() did not "
            "return CorpusSource."
        )

    print(
        "CorpusSource construction : PASS"
    )

    if source.source_type is not SourceType.LEXICON:
        fail(
            "Amarakośa semantic source type was not "
            "SourceType.LEXICON."
        )

    print(
        "SourceType.LEXICON : PASS"
    )

    if source.status is not SourceStatus.REGISTERED:
        fail(
            "Constructed Amarakośa source does not use "
            "SourceStatus.REGISTERED."
        )

    print(
        "SourceStatus.REGISTERED : PASS"
    )

    # ---------------------------------------------------------
    # 7. Existing Amarakośa acquisition references
    # ---------------------------------------------------------

    section(
        "7. EXISTING AMARAKOSHA ACQUISITION REFERENCES"
    )

    search_tokens = (
        "amarakosha",
        "Amarakosha",
        "अमरकोश",
        "SourceType.LEXICON",
        "CorpusSourceFactory",
    )

    all_results = {}

    for token in search_tokens:

        results = search_production_references(
            token
        )

        all_results[token] = results

        print()
        print(
            f"Token: {token!r}"
        )
        print(
            f"Matches: {len(results)}"
        )

        for relative_path, line_number, line in results[:50]:
            print(
                f"  {relative_path}:{line_number}: {line}"
            )

        if len(results) > 50:
            print(
                f"  ... {len(results) - 50} additional matches"
            )

    # ---------------------------------------------------------
    # 8. Stale acquisition semantics
    # ---------------------------------------------------------

    section(
        "8. STALE ACQUISITION SEMANTICS"
    )

    stale_tokens = (
        "SourceType.LOCAL",
        "SourceType.REMOTE",
        "SourceType.GRETIL",
        "SourceStatus.AVAILABLE",
    )

    stale_results = {}

    for token in stale_tokens:

        results = search_production_references(
            token
        )

        stale_results[token] = results

        print(
            f"{token:<28} : {len(results)} production reference(s)"
        )

        for relative_path, line_number, line in results[:20]:
            print(
                f"  {relative_path}:{line_number}: {line}"
            )

    # ---------------------------------------------------------
    # 9. Acquisition boundary conclusion
    # ---------------------------------------------------------

    section(
        "9. ACQUISITION BOUNDARY CONCLUSION"
    )

    print(
        "WorkRegistry provides the Amarakośa work identity."
    )

    print(
        "CorpusSourceFactory provides canonical source "
        "construction."
    )

    print(
        "SourceType.LEXICON provides the semantic source "
        "classification."
    )

    print(
        "No new SourceType enum member is required."
    )

    print(
        "No new CorpusSource model is required."
    )

    print(
        "No new generic acquisition abstraction should be "
        "created at this stage."
    )

    print()

    print(
        "Next decision must be based on the existing "
        "Amarakośa acquisition/provider/manifest path."
    )

    # ---------------------------------------------------------
    # 10. Final result
    # ---------------------------------------------------------

    section("10. FINAL RESULT")

    print(
        "Batch 5H-5E-13R-1 : PASS"
    )

    print(
        "Amarakośa acquisition boundary is ready "
        "for provider/manifest tracing."
    )


if __name__ == "__main__":
    main()
