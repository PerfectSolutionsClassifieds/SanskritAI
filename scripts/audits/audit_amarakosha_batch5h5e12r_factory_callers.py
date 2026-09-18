from __future__ import annotations

"""
BATCH 5H-5E-12R-2
CorpusSourceFactory Call-Site Semantic Audit

READ-ONLY.

Purpose
-------
Trace every active production caller of:

    CorpusSourceFactory.from_file()
    CorpusSourceFactory.from_url()
    CorpusSourceFactory.from_metadata()

Determine whether callers:
    1. explicitly provide SourceType, or
    2. rely on the stale LOCAL / REMOTE defaults.

This audit is specifically required before changing the generic
factory defaults to SourceType.UNKNOWN.

No production mutation is performed.
No acquisition is performed.
"""

# from __future__ import annotations

import re
from pathlib import Path


PROJECT_ROOT = Path("/content/SanskritAI")
PACKAGE_PARENT = PROJECT_ROOT.parent


def section(title: str) -> None:
    print()
    print("-" * 112)
    print(title)
    print("-" * 112)


def bootstrap() -> None:
    import sys

    if str(PACKAGE_PARENT) not in sys.path:
        sys.path.insert(0, str(PACKAGE_PARENT))


def production_python_files() -> list[Path]:
    """
    Production files only.

    Ignore:
    - tests/
    - __pycache__/
    - numeric historical files such as foo1.py
    - _G<number>.py
    """

    numeric_suffix = re.compile(r".*\d+\.py$")
    generation_suffix = re.compile(r".*_G\d+\.py$")

    files: list[Path] = []

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


def search_factory_calls() -> list[tuple[Path, int, str]]:
    """
    Find active CorpusSourceFactory calls.

    Obvious comments are excluded.
    """

    pattern = re.compile(
        r"CorpusSourceFactory\."
        r"(from_file|from_url|from_metadata)\s*\("
    )

    results: list[tuple[Path, int, str]] = []

    for path in production_python_files():

        try:
            lines = path.read_text(
                encoding="utf-8"
            ).splitlines()
        except Exception:
            continue

        for line_number, line in enumerate(
            lines,
            start=1,
        ):

            stripped = line.strip()

            if stripped.startswith("#"):
                continue

            code = line.split("#", 1)[0]

            if pattern.search(code):
                results.append(
                    (
                        path,
                        line_number,
                        line.rstrip(),
                    )
                )

    return results


def print_context(
    path: Path,
    line_number: int,
    radius: int = 7,
) -> None:

    try:
        lines = path.read_text(
            encoding="utf-8"
        ).splitlines()
    except Exception:
        return

    start = max(
        1,
        line_number - radius,
    )

    end = min(
        len(lines),
        line_number + radius,
    )

    for number in range(start, end + 1):

        marker = (
            ">>>"
            if number == line_number
            else "   "
        )

        print(
            f"{marker} {number:>4}: "
            f"{lines[number - 1]}"
        )


def inspect_caller_context(
    path: Path,
    line_number: int,
) -> dict[str, bool]:

    try:
        lines = path.read_text(
            encoding="utf-8"
        ).splitlines()
    except Exception:
        return {
            "source_type": False,
            "metadata": False,
            "repository": False,
        }

    start = max(
        0,
        line_number - 1,
    )

    end = min(
        len(lines),
        line_number + 20,
    )

    context = "\n".join(
        lines[start:end]
    )

    return {
        "source_type": "source_type=" in context,
        "metadata": "metadata=" in context,
        "repository": "repository" in context.lower(),
    }


def main() -> None:

    print("=" * 112)
    print(
        "BATCH 5H-5E-12R-2 — "
        "CORPUSSOURCEFACTORY CALL-SITE SEMANTIC AUDIT"
    )
    print("=" * 112)

    section("1. PACKAGE BOOTSTRAP")

    bootstrap()

    print(
        f"Project root   : {PROJECT_ROOT}"
    )

    print(
        f"Package parent : {PACKAGE_PARENT}"
    )

    import SanskritAI  # noqa: F401

    print(
        "SanskritAI import : PASS"
    )

    section("2. CANONICAL FACTORY SOURCE")

    factory_path = (
        PROJECT_ROOT
        / "acquisition"
        / "factories"
        / "corpus_source_factory.py"
    )

    factory_source = factory_path.read_text(
        encoding="utf-8"
    )

    print(
        f"Factory path : {factory_path}"
    )

    for line_number, line in enumerate(
        factory_source.splitlines(),
        start=1,
    ):

        if (
            "def from_file" in line
            or "def from_url" in line
            or "def from_metadata" in line
            or "source_type:" in line
        ):
            print(
                f"{line_number:>4}: {line}"
            )

    section("3. ACTIVE FACTORY CALL SITES")

    calls = search_factory_calls()

    print(
        f"Factory call count : {len(calls)}"
    )

    for path, line_number, line in calls:

        print()
        print(
            f"{path.relative_to(PROJECT_ROOT)}:"
            f"{line_number}"
        )
        print(
            f"Call : {line.strip()}"
        )

    section("4. CALL-SITE SEMANTIC CONTEXT")

    for path, line_number, line in calls:

        print()
        print("=" * 100)
        print(
            f"{path.relative_to(PROJECT_ROOT)}:"
            f"{line_number}"
        )
        print("=" * 100)

        print_context(
            path,
            line_number,
            radius=8,
        )

        flags = inspect_caller_context(
            path,
            line_number,
        )

        print()
        print(
            "Semantic evidence:"
        )
        print(
            f"  explicit source_type : "
            f"{flags['source_type']}"
        )
        print(
            f"  metadata             : "
            f"{flags['metadata']}"
        )
        print(
            f"  repository           : "
            f"{flags['repository']}"
        )

    section("5. STALE DEFAULT DEPENDENCY ANALYSIS")

    print(
        "The generic factory currently defines:"
    )

    print()
    print(
        "  from_file(..., "
        "source_type=SourceType.LOCAL)"
    )

    print(
        "  from_url(..., "
        "source_type=SourceType.REMOTE)"
    )

    print()
    print(
        "This section determines which active callers "
        "actually depend on those defaults."
    )

    default_dependent: list[
        tuple[Path, int, str]
    ] = []

    explicit_type: list[
        tuple[Path, int, str]
    ] = []

    for path, line_number, line in calls:

        flags = inspect_caller_context(
            path,
            line_number,
        )

        if flags["source_type"]:
            explicit_type.append(
                (
                    path,
                    line_number,
                    line,
                )
            )
        else:
            default_dependent.append(
                (
                    path,
                    line_number,
                    line,
                )
            )

    print()
    print(
        f"Callers apparently supplying "
        f"source_type : {len(explicit_type)}"
    )

    for path, line_number, line in explicit_type:

        print(
            f"  - {path.relative_to(PROJECT_ROOT)}:"
            f"{line_number}"
        )

    print()
    print(
        f"Callers apparently relying on "
        f"factory default : {len(default_dependent)}"
    )

    for path, line_number, line in default_dependent:

        print(
            f"  - {path.relative_to(PROJECT_ROOT)}:"
            f"{line_number}"
        )

    section("6. GRETIL SPECIFIC ANALYSIS")

    gretil_path = (
        PROJECT_ROOT
        / "acquisition"
        / "parsers"
        / "gretil_catalog_parser.py"
    )

    if gretil_path.exists():

        gretil_source = gretil_path.read_text(
            encoding="utf-8"
        )

        print(
            "GRETIL parser source_type reference:"
        )

        for line_number, line in enumerate(
            gretil_source.splitlines(),
            start=1,
        ):

            if (
                "source_type=" in line
                or '"repository"' in line
                or "'repository'" in line
                or "metadata" in line
            ):
                print(
                    f"{line_number:>4}: {line}"
                )

    section("7. AMARAKOSHA ACQUISITION CALLERS")

    amar_matches: list[
        tuple[Path, int, str]
    ] = []

    for path in production_python_files():

        try:
            text = path.read_text(
                encoding="utf-8"
            )
        except Exception:
            continue

        if "amarakosha" not in text.lower():
            continue

        lines = text.splitlines()

        for line_number, line in enumerate(
            lines,
            start=1,
        ):

            if (
                "CorpusSourceFactory.from_file"
                in line
                or "CorpusSourceFactory.from_url"
                in line
                or "CorpusSourceFactory.from_metadata"
                in line
            ):

                amar_matches.append(
                    (
                        path,
                        line_number,
                        line.rstrip(),
                    )
                )

    print(
        f"Amarakośa factory call count : "
        f"{len(amar_matches)}"
    )

    for path, line_number, line in amar_matches:

        print()
        print(
            f"{path.relative_to(PROJECT_ROOT)}:"
            f"{line_number}"
        )
        print(
            f"Call : {line.strip()}"
        )

        print_context(
            path,
            line_number,
            radius=5,
        )

    section("8. SEMANTIC SAFETY CONCLUSION")

    print(
        "No production mutation performed."
    )

    print(
        "No SourceType modification performed."
    )

    print(
        "No CorpusSourceFactory modification performed."
    )

    print(
        "No acquisition performed."
    )

    print()
    print(
        "The next repair should change only the stale "
        "transport/provider semantics after all active "
        "callers have been classified."
    )

    print()
    print("=" * 112)
    print(
        "BATCH 5H-5E-12R-2 — "
        "CALL-SITE AUDIT COMPLETE"
    )
    print("=" * 112)


if __name__ == "__main__":
    main()
