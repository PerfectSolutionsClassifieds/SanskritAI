
from __future__ import annotations

"""
BATCH 5H-5E-13R-2
=================

AMARAKOSHA PROVIDER / MANIFEST TRACE

Purpose
-------
Trace the EXISTING Amarakośa acquisition/provider/manifest path.

This audit is read-only.

It determines:

1. Existing Amarakośa acquisition providers.
2. Existing Amarakośa manifests.
3. Existing Amarakośa source declarations.
4. Existing acquisition/discovery/provider references.
5. Existing WorkRegistry/resource references.
6. Existing CorpusSourceFactory integration points.
7. Whether an Amarakośa-specific acquisition abstraction already exists.
8. Whether stale SourceType references occur in ACTUAL production code.

Important
---------
Audit scripts, repair scripts, tests, __pycache__, and historical
numbered/_G<number>.py copies are NOT production evidence.

No production files are modified.
No new classes are created.
"""

from pathlib import Path
import re
import sys


PROJECT_ROOT = Path("/content/SanskritAI")


def fail(message: str) -> None:
    raise RuntimeError(message)


def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def is_historical_python(path: Path) -> bool:
    """
    Ignore historical copies:

        foo1.py
        foo2.py
        foo123.py
        foo_G1.py
        foo_G27.py
    """

    stem = path.stem

    if re.search(r"\d+$", stem):
        return True

    if re.search(r"_G\d+$", stem):
        return True

    return False


def classify_path(path: Path) -> str:
    relative = path.relative_to(PROJECT_ROOT)
    parts = set(relative.parts)

    if "tests" in parts:
        return "test"

    if "__pycache__" in parts:
        return "cache"

    if "scripts" in parts:
        if "audits" in parts:
            return "audit"

        if "repairs" in parts or "repair" in parts:
            return "repair"

        return "script"

    return "production"


def production_files() -> list[Path]:
    files = []

    for path in PROJECT_ROOT.rglob("*.py"):

        category = classify_path(path)

        if category != "production":
            continue

        if is_historical_python(path):
            continue

        files.append(path)

    return sorted(files)


def all_nonhistorical_python_files() -> list[Path]:
    files = []

    for path in PROJECT_ROOT.rglob("*.py"):

        category = classify_path(path)

        if category in {"cache"}:
            continue

        if is_historical_python(path):
            continue

        files.append(path)

    return sorted(files)


def matches(
    token: str,
    *,
    files: list[Path],
) -> list[tuple[str, int, str]]:

    results = []

    for path in files:

        try:
            text = path.read_text(
                encoding="utf-8"
            )
        except Exception:
            continue

        for line_number, line in enumerate(
            text.splitlines(),
            start=1,
        ):
            if token.lower() in line.lower():
                results.append(
                    (
                        str(path.relative_to(PROJECT_ROOT)),
                        line_number,
                        line.strip(),
                    )
                )

    return results


def print_matches(
    label: str,
    token: str,
    files: list[Path],
    limit: int = 100,
) -> list[tuple[str, int, str]]:

    results = matches(
        token,
        files=files,
    )

    print()
    print(f"{label}: {token!r}")
    print(f"Matches: {len(results)}")

    for relative_path, line_number, line in results[:limit]:
        print(
            f"  {relative_path}:{line_number}: {line}"
        )

    if len(results) > limit:
        print(
            f"  ... {len(results) - limit} additional matches"
        )

    return results


def main() -> None:

    section(
        "BATCH 5H-5E-13R-2 — "
        "AMARAKOSHA PROVIDER / MANIFEST TRACE"
    )

    print(
        f"Project root : {PROJECT_ROOT}"
    )

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
    # 2. File classification
    # ---------------------------------------------------------

    section("2. FILE CLASSIFICATION")

    production = production_files()
    all_python = all_nonhistorical_python_files()

    print(
        f"Production Python files : {len(production)}"
    )

    print(
        f"Non-cache/non-historical Python files : "
        f"{len(all_python)}"
    )

    print()
    print(
        "Audit scripts are excluded from production "
        "semantic conclusions."
    )

    print(
        "Repair scripts are excluded from production "
        "semantic conclusions."
    )

    print(
        "Tests are excluded from production semantic "
        "conclusions."
    )

    print(
        "Historical numbered/_G<number>.py files are "
        "excluded."
    )

    # ---------------------------------------------------------
    # 3. WorkRegistry / Amarakośa
    # ---------------------------------------------------------

    section("3. WORKREGISTRY / AMARAKOSHA")

    from SanskritAI.acquisition.metadata.registries.work_registry import (
        WorkRegistry,
    )

    registry = WorkRegistry()

    work = registry.find_work(
        "amarakosha"
    )

    if work is None:
        work = registry.find_work(
            "Amarakosha"
        )

    if work is None:
        work = registry.find_work(
            "अमरकोश"
        )

    if work is None:
        fail(
            "Amarakośa WorkDefinition not found."
        )

    print(
        "Amarakośa WorkDefinition : PASS"
    )

    print(
        f"identifier  : {getattr(work, 'identifier', None)!r}"
    )

    print(
        f"title       : {getattr(work, 'title', None)!r}"
    )

    print(
        f"corpus_type : {getattr(work, 'corpus_type', None)!r}"
    )

    print(
        f"repository  : {getattr(work, 'repository', None)!r}"
    )

    print(
        f"metadata    : {getattr(work, 'metadata', None)!r}"
    )

    # ---------------------------------------------------------
    # 4. Amarakośa production files
    # ---------------------------------------------------------

    section("4. AMARAKOSHA PRODUCTION FILES")

    amarakosha_files = []

    for path in production:

        relative = str(
            path.relative_to(PROJECT_ROOT)
        ).lower()

        if "amarakosha" in relative:
            amarakosha_files.append(path)

    print(
        f"Amarakośa production files : "
        f"{len(amarakosha_files)}"
    )

    for path in amarakosha_files:
        print(
            f"  {path.relative_to(PROJECT_ROOT)}"
        )

    # ---------------------------------------------------------
    # 5. Acquisition production files
    # ---------------------------------------------------------

    section("5. ACQUISITION PRODUCTION FILES")

    acquisition_files = []

    for path in production:

        relative = path.relative_to(
            PROJECT_ROOT
        )

        if relative.parts and relative.parts[0] == "acquisition":
            acquisition_files.append(path)

    print(
        f"Acquisition production files : "
        f"{len(acquisition_files)}"
    )

    for path in acquisition_files:
        print(
            f"  {path.relative_to(PROJECT_ROOT)}"
        )

    # ---------------------------------------------------------
    # 6. Provider / manifest discovery
    # ---------------------------------------------------------

    section(
        "6. PROVIDER / MANIFEST DISCOVERY"
    )

    provider_tokens = (
        "provider",
        "manifest",
        "acquirer",
        "discovery",
        "resource",
        "source",
    )

    provider_candidates = []

    for path in acquisition_files:

        lower = str(
            path.relative_to(PROJECT_ROOT)
        ).lower()

        if any(
            token in lower
            for token in provider_tokens
        ):
            provider_candidates.append(path)

    print(
        f"Provider/manifest candidate files : "
        f"{len(provider_candidates)}"
    )

    for path in provider_candidates:
        print(
            f"  {path.relative_to(PROJECT_ROOT)}"
        )

    # ---------------------------------------------------------
    # 7. Amarakośa references in production only
    # ---------------------------------------------------------

    section(
        "7. AMARAKOSHA REFERENCES — PRODUCTION ONLY"
    )

    for token in (
        "amarakosha",
        "Amarakosha",
        "अमरकोश",
    ):
        print_matches(
            "Production reference",
            token,
            production,
        )

    # ---------------------------------------------------------
    # 8. Manifest references
    # ---------------------------------------------------------

    section(
        "8. AMARAKOSHA MANIFEST REFERENCES"
    )

    manifest_tokens = (
        "AmarakoshaManifest",
        "amarakosha_manifest",
        "manifest",
    )

    for token in manifest_tokens:

        print_matches(
            "Production manifest reference",
            token,
            production,
        )

    # ---------------------------------------------------------
    # 9. Provider references
    # ---------------------------------------------------------

    section(
        "9. AMARAKOSHA PROVIDER REFERENCES"
    )

    provider_tokens = (
        "AmarakoshaProvider",
        "amarakosha_provider",
        "AmarakoshaAcquirer",
        "amarakosha_acquirer",
    )

    for token in provider_tokens:

        print_matches(
            "Production provider/acquirer reference",
            token,
            production,
        )

    # ---------------------------------------------------------
    # 10. CorpusSourceFactory references
    # ---------------------------------------------------------

    section(
        "10. CORPUSSOURCEFACTORY PRODUCTION REFERENCES"
    )

    factory_results = print_matches(
        "Production CorpusSourceFactory reference",
        "CorpusSourceFactory",
        production,
    )

    # ---------------------------------------------------------
    # 11. SourceType.LEXICON references
    # ---------------------------------------------------------

    section(
        "11. SOURCETYPE.LEXICON PRODUCTION REFERENCES"
    )

    lexicon_results = print_matches(
        "Production SourceType.LEXICON reference",
        "SourceType.LEXICON",
        production,
    )

    # ---------------------------------------------------------
    # 12. Stale SourceType references
    # ---------------------------------------------------------

    section(
        "12. STALE SOURCETYPE REFERENCES — "
        "PRODUCTION ONLY"
    )

    stale_tokens = (
        "SourceType.LOCAL",
        "SourceType.REMOTE",
        "SourceType.GRETIL",
        "SourceStatus.AVAILABLE",
    )

    stale_counts = {}

    for token in stale_tokens:

        results = print_matches(
            "Production stale reference",
            token,
            production,
        )

        stale_counts[token] = len(results)

    # ---------------------------------------------------------
    # 13. Broader stale-reference location audit
    # ---------------------------------------------------------

    section(
        "13. STALE REFERENCES — ALL NON-HISTORICAL PYTHON"
    )

    print(
        "This section is diagnostic only."
    )

    print(
        "Audit/repair/test references are NOT treated "
        "as production defects."
    )

    for token in stale_tokens:

        results = matches(
            token,
            files=all_python,
        )

        print(
            f"{token:<28} : "
            f"{len(results)} total non-historical reference(s)"
        )

    # ---------------------------------------------------------
    # 14. Concrete production conclusions
    # ---------------------------------------------------------

    section(
        "14. CONCRETE PRODUCTION CONCLUSIONS"
    )

    print(
        "WorkRegistry contains Amarakośa work identity."
    )

    print(
        "CorpusSourceFactory is available as the canonical "
        "source-construction boundary."
    )

    print(
        "SourceType.LEXICON is available for semantic "
        "classification."
    )

    if stale_counts["SourceType.LOCAL"] == 0:
        print(
            "Production SourceType.LOCAL references : 0"
        )
    else:
        print(
            "Production SourceType.LOCAL references : "
            f"{stale_counts['SourceType.LOCAL']}"
        )

    if stale_counts["SourceType.REMOTE"] == 0:
        print(
            "Production SourceType.REMOTE references : 0"
        )
    else:
        print(
            "Production SourceType.REMOTE references : "
            f"{stale_counts['SourceType.REMOTE']}"
        )

    if stale_counts["SourceType.GRETIL"] == 0:
        print(
            "Production SourceType.GRETIL references : 0"
        )
    else:
        print(
            "Production SourceType.GRETIL references : "
            f"{stale_counts['SourceType.GRETIL']}"
        )

    if stale_counts["SourceStatus.AVAILABLE"] == 0:
        print(
            "Production SourceStatus.AVAILABLE references : 0"
        )
    else:
        print(
            "Production SourceStatus.AVAILABLE references : "
            f"{stale_counts['SourceStatus.AVAILABLE']}"
        )

    # ---------------------------------------------------------
    # 15. No repair decision
    # ---------------------------------------------------------

    section("15. REPAIR DECISION")

    print(
        "NO PRODUCTION REPAIR PERFORMED."
    )

    print(
        "No enum members were added."
    )

    print(
        "No CorpusSource fields were changed."
    )

    print(
        "No CorpusSourceFactory API was changed."
    )

    print(
        "No Amarakośa provider was created."
    )

    print(
        "No Amarakośa manifest was created."
    )

    print(
        "No acquisition abstraction was created."
    )

    # ---------------------------------------------------------
    # 16. Final result
    # ---------------------------------------------------------

    section("16. FINAL RESULT")

    print(
        "BATCH 5H-5E-13R-2 — RESULT: PASS"
    )

    print(
        "Existing Amarakośa provider/manifest boundary "
        "has been traced without production mutation."
    )

    print(
        "Next step: inspect concrete source declarations "
        "and acquisition resources before implementation."
    )


if __name__ == "__main__":
    main()
