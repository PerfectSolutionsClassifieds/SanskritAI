"""
Batch 5H-5E-12R-3
-----------------

CorpusSourceFactory semantic decision audit.

READ-ONLY.

IMPORTANT
---------
CorpusSourceFactory is intentionally NOT imported during this audit.

The current factory contains stale references to:

    SourceType.LOCAL
    SourceType.REMOTE

Those references cause CorpusSourceFactory import-time failure because
the canonical SourceType enum now contains only semantic source types.

Therefore this audit must inspect the factory source text directly before
the factory repair is performed.

Purpose
-------
Validate the semantic repair before mutating CorpusSourceFactory.

Questions
---------
1. What should from_file() mean when source_type is omitted?
2. What should from_url() mean when source_type is omitted?
3. Does LocalDirectoryProvider need an explicit SourceType?
4. What semantic SourceType should GRETIL use?
5. Is repository/provider provenance represented separately?
6. Does any active production caller require LOCAL / REMOTE / GRETIL?

This audit intentionally does not modify production code.
"""

from __future__ import annotations

import inspect
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path("/content/SanskritAI")
PACKAGE_PARENT = PROJECT_ROOT.parent

if str(PACKAGE_PARENT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_PARENT))


def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def show_context(
    path: Path,
    start: int,
    end: int,
) -> None:

    lines = read_text(path).splitlines()

    for number in range(start, min(end, len(lines)) + 1):
        print(f"{number:4}: {lines[number - 1]}")


def active_source_lines(path: Path):
    """
    Yield non-comment source lines.

    This is intentionally conservative. It ignores complete comment
    lines but does not attempt to parse Python AST semantics.
    """

    for number, line in enumerate(
        read_text(path).splitlines(),
        start=1,
    ):

        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):
            continue

        yield number, line


def find_active_pattern(
    path: Path,
    pattern: str,
):
    results = []

    for number, line in active_source_lines(path):

        if pattern in line:
            results.append(
                (
                    number,
                    line.strip(),
                )
            )

    return results


def main() -> None:

    section(
        "BATCH 5H-5E-12R-3 — FACTORY SEMANTIC DECISION AUDIT"
    )

    print()
    print("Project root :", PROJECT_ROOT)

    # ------------------------------------------------------------------
    # 1. Package bootstrap
    # ------------------------------------------------------------------

    section("1. PACKAGE BOOTSTRAP")

    try:

        import SanskritAI  # noqa: F401

        print("SanskritAI import : PASS")

    except Exception as exc:

        print("SanskritAI import : FAIL")
        print("Exception :", repr(exc))
        return

    # ------------------------------------------------------------------
    # 2. SourceType ONLY
    #
    # DO NOT import CorpusSourceFactory here.
    # ------------------------------------------------------------------

    section("2. CANONICAL SOURCETYPE CONTRACT")

    source_type_path = (
        PROJECT_ROOT
        / "acquisition"
        / "models"
        / "source_type.py"
    )

    print("SourceType path :", source_type_path)

    if not source_type_path.exists():

        print("SourceType file : NOT FOUND")
        return

    try:

        from SanskritAI.acquisition.models.source_type import (
            SourceType,
        )

        print("SourceType import : PASS")

    except Exception as exc:

        print("SourceType import : FAIL")
        print("Exception :", repr(exc))
        return

    print()
    print("SourceType documentation:")
    print(inspect.getdoc(SourceType) or "<no docstring>")

    print()
    print("Canonical members:")

    for member in SourceType:

        print(
            f"  {member.name:<20} = {member.value}"
        )

    print()
    print("Stale transport/provider members:")

    for name in (
        "LOCAL",
        "REMOTE",
        "GRETIL",
    ):

        print(
            f"  SourceType.{name:<10} : "
            f"{hasattr(SourceType, name)}"
        )

    # ------------------------------------------------------------------
    # 3. CorpusSource source-level contract
    #
    # Again: no CorpusSourceFactory import.
    # ------------------------------------------------------------------

    section("3. CANONICAL CORPUSSOURCE CONTRACT")

    corpus_source_path = (
        PROJECT_ROOT
        / "acquisition"
        / "models"
        / "corpus_source.py"
    )

    print("CorpusSource path :", corpus_source_path)

    if not corpus_source_path.exists():

        print("CorpusSource file : NOT FOUND")
        return

    try:

        from SanskritAI.acquisition.models.corpus_source import (
            CorpusSource,
        )

        print("CorpusSource import : PASS")

    except Exception as exc:

        print("CorpusSource import : FAIL")
        print("Exception :", repr(exc))
        return

    print()
    print("CorpusSource documentation:")
    print(inspect.getdoc(CorpusSource) or "<no docstring>")

    print()
    print("Relevant annotations:")

    annotations = getattr(
        CorpusSource,
        "__annotations__",
        {},
    )

    for name in (
        "source_id",
        "name",
        "source_type",
        "source_format",
        "metadata",
        "download_urls",
        "local_path",
        "cache_directory",
    ):

        print(
            f"  {name:<20} : "
            f"{annotations.get(name, '<not declared>')}"
        )

    # ------------------------------------------------------------------
    # 4. Factory SOURCE inspection
    #
    # Critical correction:
    # The factory is inspected as source text because importing it
    # currently fails on SourceType.LOCAL / REMOTE.
    # ------------------------------------------------------------------

    section("4. CORPUSSOURCEFACTORY SOURCE INSPECTION")

    factory_path = (
        PROJECT_ROOT
        / "acquisition"
        / "factories"
        / "corpus_source_factory.py"
    )

    print("Factory path :", factory_path)

    if not factory_path.exists():

        print("Factory file : NOT FOUND")
        return

    factory_text = read_text(factory_path)

    print()
    print("Factory import status:")
    print(
        "  NOT attempted intentionally "
        "(pre-repair source inspection)"
    )

    print()
    print("Stale SourceType references:")

    stale_patterns = (
        "SourceType.LOCAL",
        "SourceType.REMOTE",
        "SourceType.GRETIL",
    )

    for pattern in stale_patterns:

        matches = find_active_pattern(
            factory_path,
            pattern,
        )

        if not matches:

            print(
                f"  {pattern:<22} : 0"
            )

        else:

            print(
                f"  {pattern:<22} : "
                f"{len(matches)}"
            )

            for number, line in matches:

                print(
                    f"      {number}: {line}"
                )

    # ------------------------------------------------------------------
    # 5. Factory method signatures from source
    # ------------------------------------------------------------------

    section("5. FACTORY METHOD DEFAULTS — SOURCE LEVEL")

    factory_lines = factory_text.splitlines()

    relevant_ranges = [
        ("from_file", 48, 85),
        ("from_url", 100, 140),
        ("from_metadata", 145, 180),
    ]

    for name, start, end in relevant_ranges:

        print()
        print("-" * 90)
        print(name)
        print("-" * 90)

        show_context(
            factory_path,
            start,
            end,
        )

    # ------------------------------------------------------------------
    # 6. LocalDirectoryProvider
    # ------------------------------------------------------------------

    section(
        "6. LOCAL DIRECTORY PROVIDER SEMANTIC CHECK"
    )

    provider_path = (
        PROJECT_ROOT
        / "acquisition"
        / "discovery"
        / "providers"
        / "local_directory_provider.py"
    )

    print("Provider path :", provider_path)

    if provider_path.exists():

        show_context(
            provider_path,
            118,
            140,
        )

    else:

        print("Provider file not found.")

    print()
    print("Semantic interpretation:")
    print(
        "  LocalDirectoryProvider discovers a source from a local file."
    )
    print(
        "  Local storage is a transport/storage characteristic."
    )
    print(
        "  SourceType describes what the source fundamentally is."
    )
    print(
        "  Therefore SourceType.LOCAL is not a valid semantic value."
    )
    print(
        "  Generic fallback candidate: SourceType.UNKNOWN."
    )

    # ------------------------------------------------------------------
    # 7. GRETIL parser
    # ------------------------------------------------------------------

    section(
        "7. GRETIL PARSER SEMANTIC CHECK"
    )

    gretil_path = (
        PROJECT_ROOT
        / "acquisition"
        / "parsers"
        / "gretil_catalog_parser.py"
    )

    print("GRETIL parser path :", gretil_path)

    if gretil_path.exists():

        show_context(
            gretil_path,
            153,
            175,
        )

        print()

        show_context(
            gretil_path,
            228,
            245,
        )

    else:

        print("GRETIL parser file not found.")

    print()
    print("Semantic interpretation:")
    print(
        "  SourceType.GRETIL is not a canonical semantic category."
    )
    print(
        "  GRETIL identifies repository/provenance."
    )
    print(
        "  The parser already exposes repository='GRETIL'."
    )
    print(
        "  Candidate semantic SourceType: SourceType.CORPUS."
    )

    # ------------------------------------------------------------------
    # 8. Active production stale references
    # ------------------------------------------------------------------

    section(
        "8. ACTIVE PRODUCTION STALE REFERENCES"
    )

    ignored_dirs = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        "tests",
    }

    stale_matches = []

    for path in PROJECT_ROOT.rglob("*.py"):

        relative = path.relative_to(PROJECT_ROOT)
        parts = set(relative.parts)

        if parts & ignored_dirs:
            continue

        name = path.name

        # Ignore historical numeric snapshots.
        if re.search(r"\d+\.py$", name):
            continue

        # Ignore generation snapshots.
        if re.search(r"_G\d+\.py$", name):
            continue

        for number, line in active_source_lines(path):

            for pattern in stale_patterns:

                if pattern in line:

                    stale_matches.append(
                        (
                            str(relative),
                            number,
                            pattern,
                            line.strip(),
                        )
                    )

    if not stale_matches:

        print(
            "Active stale production references : 0"
        )

    else:

        for (
            relative,
            number,
            pattern,
            line,
        ) in stale_matches:

            print(
                f"{relative}:{number}: "
                f"{pattern} -> {line}"
            )

    # ------------------------------------------------------------------
    # 9. Explicit semantic decision
    # ------------------------------------------------------------------

    section(
        "9. SEMANTIC DECISION"
    )

    print(
        "CorpusSourceFactory.from_file() default:"
    )
    print(
        "  Current : SourceType.LOCAL"
    )
    print(
        "  Proposed: SourceType.UNKNOWN"
    )
    print(
        "  Reason  : local storage is not semantic source type"
    )

    print()
    print(
        "CorpusSourceFactory.from_url() default:"
    )
    print(
        "  Current : SourceType.REMOTE"
    )
    print(
        "  Proposed: SourceType.UNKNOWN"
    )
    print(
        "  Reason  : remote transport is not semantic source type"
    )

    print()
    print(
        "GretilCatalogParser:"
    )
    print(
        "  Current : SourceType.GRETIL"
    )
    print(
        "  Proposed: SourceType.CORPUS"
    )
    print(
        "  Provenance remains: metadata['repository'] = 'GRETIL'"
    )

    print()
    print(
        "LocalDirectoryProvider:"
    )
    print(
        "  Current call omits source_type."
    )
    print(
        "  Result after generic factory repair: SourceType.UNKNOWN."
    )
    print(
        "  No provider-specific SourceType is required."
    )

    print()
    print(
        "SourceType enum:"
    )
    print(
        "  NO MUTATION."
    )

    # ------------------------------------------------------------------
    # 10. Safety checks
    # ------------------------------------------------------------------

    section(
        "10. SAFETY CHECKS"
    )

    print(
        "SourceType.LOCAL exists :",
        hasattr(SourceType, "LOCAL"),
    )

    print(
        "SourceType.REMOTE exists:",
        hasattr(SourceType, "REMOTE"),
    )

    print(
        "SourceType.GRETIL exists:",
        hasattr(SourceType, "GRETIL"),
    )

    print()
    print(
        "Factory source contains SourceType.LOCAL :",
        "SourceType.LOCAL" in factory_text,
    )

    print(
        "Factory source contains SourceType.REMOTE:",
        "SourceType.REMOTE" in factory_text,
    )

    # ------------------------------------------------------------------
    # 11. Final conclusion
    # ------------------------------------------------------------------

    section(
        "11. SAFETY CONCLUSION"
    )

    print("No production files modified.")
    print("No SourceType members added.")
    print("No CorpusSourceFactory changes performed.")
    print("No GRETIL parser changes performed.")
    print("No acquisition performed.")
    print()
    print(
        "CorpusSourceFactory was intentionally NOT imported."
    )
    print(
        "The current import-time AttributeError is therefore avoided."
    )
    print()
    print(
        "READY FOR MINIMAL 5H-5E-12R-4 FACTORY REPAIR."
    )

    print()
    print("=" * 100)
    print(
        "BATCH 5H-5E-12R-3 — SEMANTIC DECISION AUDIT COMPLETE"
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
