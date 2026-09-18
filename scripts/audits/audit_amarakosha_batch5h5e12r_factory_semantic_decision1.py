"""
Batch 5H-5E-12R-3
-----------------

CorpusSourceFactory semantic decision audit.

READ-ONLY.

Purpose
-------
Validate the semantic repair before mutating CorpusSourceFactory.

Questions
---------
1. What should from_file() mean when source_type is omitted?
2. What should from_url() mean when source_type is omitted?
3. Does LocalDirectoryProvider need an explicit SourceType?
4. What semantic SourceType should GRETIL use?
5. Is repository/provider provenance already represented separately?
6. Does any active production caller require LOCAL / REMOTE / GRETIL?

This audit intentionally does not modify production code.
"""

from __future__ import annotations

import inspect
import os
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


def source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def show_context(path: Path, start: int, end: int) -> None:
    lines = source_text(path).splitlines()

    for number in range(start, min(end, len(lines)) + 1):
        print(f"{number:4}: {lines[number - 1]}")


def main() -> None:

    section("BATCH 5H-5E-12R-3 — FACTORY SEMANTIC DECISION AUDIT")

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
    # 2. Canonical imports
    # ------------------------------------------------------------------

    section("2. CANONICAL TYPE IMPORTS")

    try:
        from SanskritAI.acquisition.models.source_type import SourceType
        from SanskritAI.acquisition.models.source_format import SourceFormat
        from SanskritAI.acquisition.models.corpus_source import CorpusSource
        from SanskritAI.acquisition.factories.corpus_source_factory import (
            CorpusSourceFactory,
        )

        print("SourceType             : PASS")
        print("SourceFormat           : PASS")
        print("CorpusSource           : PASS")
        print("CorpusSourceFactory    : PASS")

    except Exception as exc:
        print("Canonical imports : FAIL")
        print("Exception :", repr(exc))
        return

    # ------------------------------------------------------------------
    # 3. SourceType semantic contract
    # ------------------------------------------------------------------

    section("3. SOURCETYPE SEMANTIC CONTRACT")

    print(inspect.getdoc(SourceType) or "<no docstring>")

    print()
    print("Members:")
    for member in SourceType:
        print(f"  {member.name:<20} = {member.value}")

    print()
    print("Required stale members:")
    for name in ("LOCAL", "REMOTE", "GRETIL"):
        print(f"  {name:<10} :", hasattr(SourceType, name))

    # ------------------------------------------------------------------
    # 4. CorpusSource contract
    # ------------------------------------------------------------------

    section("4. CORPUSSOURCE CONTRACT")

    print(inspect.getdoc(CorpusSource) or "<no docstring>")

    print()
    print("Relevant annotations:")

    annotations = getattr(CorpusSource, "__annotations__", {})

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
    # 5. Factory defaults
    # ------------------------------------------------------------------

    section("5. CURRENT FACTORY DEFAULTS")

    file_signature = inspect.signature(CorpusSourceFactory.from_file)
    url_signature = inspect.signature(CorpusSourceFactory.from_url)

    print("from_file signature:")
    print(" ", file_signature)

    print()
    print("from_url signature:")
    print(" ", url_signature)

    print()
    print(
        "Current from_file default :",
        file_signature.parameters["source_type"].default,
    )

    print(
        "Current from_url default  :",
        url_signature.parameters["source_type"].default,
    )

    # ------------------------------------------------------------------
    # 6. LocalDirectoryProvider
    # ------------------------------------------------------------------

    section("6. LOCAL DIRECTORY PROVIDER SEMANTIC CHECK")

    provider_path = (
        PROJECT_ROOT
        / "acquisition"
        / "discovery"
        / "providers"
        / "local_directory_provider.py"
    )

    print("Provider path :", provider_path)

    if provider_path.exists():
        show_context(provider_path, 118, 140)
    else:
        print("Provider file not found.")

    print()
    print(
        "Interpretation:"
    )
    print(
        "  LocalDirectoryProvider discovers a source from a local file."
    )
    print(
        "  Local storage/transport is not itself a SourceType."
    )
    print(
        "  Therefore relying on SourceType.LOCAL is semantically invalid."
    )
    print(
        "  Candidate generic fallback: SourceType.UNKNOWN."
    )

    # ------------------------------------------------------------------
    # 7. GRETIL parser
    # ------------------------------------------------------------------

    section("7. GRETIL PARSER SEMANTIC CHECK")

    gretil_path = (
        PROJECT_ROOT
        / "acquisition"
        / "parsers"
        / "gretil_catalog_parser.py"
    )

    print("GRETIL parser path :", gretil_path)

    if gretil_path.exists():
        show_context(gretil_path, 153, 175)
        print()
        show_context(gretil_path, 228, 245)
    else:
        print("GRETIL parser file not found.")

    print()
    print("Candidate interpretation:")
    print("  SourceType.GRETIL is not a semantic category.")
    print("  GRETIL is repository/provenance information.")
    print("  The parser already exposes repository='GRETIL' metadata.")
    print("  The underlying downloadable text resource is a corpus/lexical")
    print("  resource rather than a transport category.")

    # ------------------------------------------------------------------
    # 8. Production stale references
    # ------------------------------------------------------------------

    section("8. ACTIVE PRODUCTION STALE REFERENCES")

    stale_patterns = (
        "SourceType.LOCAL",
        "SourceType.REMOTE",
        "SourceType.GRETIL",
    )

    ignored_dirs = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        "tests",
    }

    matches = []

    for path in PROJECT_ROOT.rglob("*.py"):

        relative = path.relative_to(PROJECT_ROOT)
        parts = set(relative.parts)

        if parts & ignored_dirs:
            continue

        name = path.name

        # Ignore historical numeric snapshots and generation snapshots.
        if re.search(r"\d+\.py$", name):
            continue

        if re.search(r"_G\d+\.py$", name):
            continue

        text = source_text(path)

        for number, line in enumerate(text.splitlines(), start=1):

            stripped = line.strip()

            if stripped.startswith("#"):
                continue

            for pattern in stale_patterns:

                if pattern in line:

                    matches.append(
                        (
                            str(relative),
                            number,
                            pattern,
                            line.strip(),
                        )
                    )

    if not matches:
        print("Active stale production references : 0")
    else:
        for relative, number, pattern, line in matches:
            print(
                f"{relative}:{number}: "
                f"{pattern} -> {line}"
            )

    # ------------------------------------------------------------------
    # 9. Semantic decision
    # ------------------------------------------------------------------

    section("9. SEMANTIC DECISION")

    print(
        "Decision candidate for CorpusSourceFactory.from_file():"
    )
    print(
        "  SourceType.UNKNOWN"
    )

    print()
    print(
        "Decision candidate for CorpusSourceFactory.from_url():"
    )
    print(
        "  SourceType.UNKNOWN"
    )

    print()
    print(
        "Decision candidate for GRETIL parser:"
    )
    print(
        "  SourceType.CORPUS"
    )

    print()
    print(
        "Repository provenance:"
    )
    print(
        "  Preserve metadata['repository'] = 'GRETIL'"
    )

    print()
    print(
        "SourceType enum mutation:"
    )
    print(
        "  NONE"
    )

    print()
    print(
        "Factory architecture mutation:"
    )
    print(
        "  Defaults only"
    )

    print()
    print(
        "LocalDirectoryProvider architecture mutation:"
    )
    print(
        "  NONE required if UNKNOWN remains the generic fallback"
    )

    # ------------------------------------------------------------------
    # 10. Safety conclusion
    # ------------------------------------------------------------------

    section("10. SAFETY CONCLUSION")

    print("No production files modified.")
    print("No SourceType members added.")
    print("No factory defaults changed.")
    print("No GRETIL parser changed.")
    print()
    print(
        "READY FOR MINIMAL 5H-5E-12R-4 FACTORY REPAIR."
    )

    print()
    print("=" * 100)
    print("BATCH 5H-5E-12R-3 — SEMANTIC DECISION AUDIT COMPLETE")
    print("=" * 100)


if __name__ == "__main__":
    main()
