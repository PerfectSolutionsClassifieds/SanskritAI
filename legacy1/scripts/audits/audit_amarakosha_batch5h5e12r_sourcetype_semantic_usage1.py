from __future__ import annotations

"""
BATCH 5H-5E-12R-1
SourceType Semantic Usage Audit

READ-ONLY.

Purpose
-------
Determine the intended semantic SourceType for every active production
consumer before repairing stale LOCAL / REMOTE / GRETIL references.

This audit MUST NOT:
- modify SourceType
- modify CorpusSourceFactory
- modify CorpusSource
- modify GretilCatalogParser
- modify Monier-Williams source code
- create new abstractions
- perform acquisition

Important:
-----------
SourceType is a semantic classification:
    LEXICON
    CORPUS
    GRAMMAR
    COMMENTARY
    ONTOLOGY
    METADATA
    DATASET
    COLLECTION
    UNKNOWN

LOCAL / REMOTE describe transport/location, not semantic source type.

GRETIL describes repository/provider identity, not semantic source type.
"""


from __future__ import annotations

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
    Production Python files only.

    Excludes:
    - tests/
    - __pycache__/
    - historical numeric suffix files
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


def active_source_type_references(
    path: Path,
) -> list[tuple[int, str, str]]:
    """
    Find SourceType references while ignoring obvious comments.

    Returns:
        (line_number, reference, line)
    """
    pattern = re.compile(r"\bSourceType\.[A-Z][A-Z0-9_]*\b")

    results: list[tuple[int, str, str]] = []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return results

    for line_number, line in enumerate(lines, start=1):

        stripped = line.strip()

        # Entire-line comments.
        if stripped.startswith("#"):
            continue

        # Remove simple trailing comments for audit purposes.
        code = line.split("#", 1)[0]

        for match in pattern.finditer(code):
            results.append(
                (
                    line_number,
                    match.group(0),
                    line.rstrip(),
                )
            )

    return results


def all_active_references() -> list[tuple[Path, int, str, str]]:
    results: list[tuple[Path, int, str, str]] = []

    for path in production_python_files():
        for line_number, reference, line in active_source_type_references(path):
            results.append(
                (
                    path,
                    line_number,
                    reference,
                    line,
                )
            )

    return results


def print_file_context(
    path: Path,
    line_number: int,
    radius: int = 4,
) -> None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return

    start = max(1, line_number - radius)
    end = min(len(lines), line_number + radius)

    for number in range(start, end + 1):
        marker = ">>>" if number == line_number else "   "
        print(
            f"{marker} {number:>4}: {lines[number - 1]}"
        )


def inspect_signature(
    owner: object,
    name: str,
) -> None:
    member = getattr(owner, name, None)

    print(f"{name:<22} -> {member}")

    if callable(member):
        try:
            print(
                f"  signature : {inspect.signature(member)}"
            )
        except Exception as exc:
            print(
                f"  signature : <unavailable: {exc!r}>"
            )


def main() -> None:

    print("=" * 112)
    print(
        "BATCH 5H-5E-12R-1 — "
        "SOURCETYPE SEMANTIC USAGE AUDIT"
    )
    print("=" * 112)

    section("1. PACKAGE BOOTSTRAP")

    bootstrap()

    print(f"Project root   : {PROJECT_ROOT}")
    print(f"Package parent : {PACKAGE_PARENT}")

    import SanskritAI  # noqa: F401

    print("SanskritAI import : PASS")

    section("2. CANONICAL SOURCETYPE")

    from SanskritAI.acquisition.models.source_type import SourceType

    print("SourceType import : PASS")
    print(f"Module            : {SourceType.__module__}")

    for member in SourceType:
        print(
            f"  - {member.name:<15} = {member.value!r}"
        )

    section("3. SOURCE TYPE SEMANTIC CONTRACT")

    print(
        inspect.getdoc(SourceType)
        or "<no class docstring>"
    )

    section("4. ACTIVE PRODUCTION SOURCETYPE REFERENCES")

    references = all_active_references()

    print(
        f"Active SourceType reference count : "
        f"{len(references)}"
    )

    for path, line_number, reference, line in references:
        relative = path.relative_to(PROJECT_ROOT)

        print(
            f"{relative}:{line_number} "
            f"-> {reference}"
        )

    section("5. ACTIVE STALE REFERENCES")

    stale_names = {
        "SourceType.LOCAL",
        "SourceType.REMOTE",
        "SourceType.GRETIL",
    }

    stale = [
        item
        for item in references
        if item[2] in stale_names
    ]

    print(
        f"Active stale reference count : "
        f"{len(stale)}"
    )

    for path, line_number, reference, line in stale:
        print()
        print(
            f"{path.relative_to(PROJECT_ROOT)}:"
            f"{line_number}"
        )
        print(f"Reference : {reference}")
        print(f"Code      : {line}")

    section("6. STALE REFERENCE CONTEXT")

    for path, line_number, reference, line in stale:
        print()
        print("=" * 90)
        print(
            f"{path.relative_to(PROJECT_ROOT)}:"
            f"{line_number}"
        )
        print(f"Reference : {reference}")
        print("=" * 90)

        print_file_context(
            path,
            line_number,
            radius=5,
        )

    section("7. CORPUSSOURCE CONTRACT")

    from SanskritAI.acquisition.models.corpus_source import (
        CorpusSource,
    )

    print(
        inspect.getdoc(CorpusSource)
        or "<no class docstring>"
    )

    print()
    print("CorpusSource annotations:")

    try:
        annotations = inspect.get_annotations(
            CorpusSource,
            eval_str=True,
        )
    except Exception as exc:
        annotations = {}
        print(
            f"Annotation inspection failed: {exc!r}"
        )

    for name, annotation in annotations.items():
        print(
            f"  {name:<20} -> {annotation!r}"
        )

    section("8. CORPUSSOURCEFACTORY SOURCE CONTRACT")

    factory_path = (
        PROJECT_ROOT
        / "acquisition"
        / "factories"
        / "corpus_source_factory.py"
    )

    print(f"Factory path : {factory_path}")

    factory_source = factory_path.read_text(
        encoding="utf-8"
    )

    for line_number, line in enumerate(
        factory_source.splitlines(),
        start=1,
    ):
        if (
            "def from_file" in line
            or "def from_url" in line
            or "def from_metadata" in line
            or "SourceType." in line
            or "source_type:" in line
        ):
            print(
                f"{line_number:>4}: {line}"
            )

    section("9. FACTORY IMPORT STATUS")

    try:
        from SanskritAI.acquisition.factories.corpus_source_factory import (
            CorpusSourceFactory,
        )

        print("CorpusSourceFactory import : PASS")

    except Exception as exc:
        print("CorpusSourceFactory import : FAIL")
        print(f"Exception : {exc!r}")

        CorpusSourceFactory = None

    if CorpusSourceFactory is not None:

        section("10. FACTORY CALLABLE CONTRACTS")

        for name in (
            "from_file",
            "from_url",
            "from_metadata",
            "is_supported",
        ):
            inspect_signature(
                CorpusSourceFactory,
                name,
            )

    section("11. GRETIL PARSER CONTRACT")

    gretil_path = (
        PROJECT_ROOT
        / "acquisition"
        / "parsers"
        / "gretil_catalog_parser.py"
    )

    print(f"GRETIL parser : {gretil_path}")

    gretil_source = gretil_path.read_text(
        encoding="utf-8"
    )

    for line_number, line in enumerate(
        gretil_source.splitlines(),
        start=1,
    ):
        if (
            "SourceType." in line
            or "from_url(" in line
            or "repository" in line
            or "metadata" in line
        ):
            print(
                f"{line_number:>4}: {line}"
            )

    section("12. MONIER-WILLIAMS SOURCE CONTRACT")

    mw_path = (
        PROJECT_ROOT
        / "acquisition"
        / "sources"
        / "monier_williams.py"
    )

    if mw_path.exists():

        print(f"MW source : {mw_path}")

        mw_source = mw_path.read_text(
            encoding="utf-8"
        )

        for line_number, line in enumerate(
            mw_source.splitlines(),
            start=1,
        ):
            if (
                "SourceType." in line
                or "CorpusSource(" in line
                or "metadata" in line
                or "repository" in line
            ):
                print(
                    f"{line_number:>4}: {line}"
                )

    else:
        print(
            "MW source file not found at expected path."
        )

    section("13. WORK REGISTRY SEMANTIC EVIDENCE")

    from SanskritAI.acquisition.metadata.registries.work_registry import (
        WorkRegistry,
    )

    registry = WorkRegistry()

    print(
        f"Registry : {registry!r}"
    )

    for identifier in (
        "amarakosha",
        "vacaspatyam",
        "shabdakalpadruma",
        "srimad_bhagavatam",
        "shiva_purana",
        "mahabharata",
        "ramayana",
    ):
        work = registry.get(identifier)

        print()
        print(
            f"{identifier}"
        )

        if work is None:
            print("  -> <NOT FOUND>")
            continue

        print(
            f"  identifier  : {work.identifier!r}"
        )
        print(
            f"  title       : {work.title!r}"
        )
        print(
            f"  corpus_type : {work.corpus_type!r}"
        )
        print(
            f"  language    : {work.language!r}"
        )
        print(
            f"  repository  : {getattr(work, 'repository', None)!r}"
        )
        print(
            f"  metadata    : {getattr(work, 'metadata', None)!r}"
        )

    section("14. SEMANTIC MAPPING QUESTIONS")

    print(
        "The following mappings are intentionally NOT guessed:"
    )

    print()
    print(
        "CorpusSourceFactory.from_file() default"
    )
    print(
        "  Current : SourceType.LOCAL"
    )
    print(
        "  Question: What semantic SourceType should "
        "the generic factory default use?"
    )

    print()
    print(
        "CorpusSourceFactory.from_url() default"
    )
    print(
        "  Current : SourceType.REMOTE"
    )
    print(
        "  Question: What semantic SourceType should "
        "the generic factory default use?"
    )

    print()
    print(
        "GretilCatalogParser"
    )
    print(
        "  Current : SourceType.GRETIL"
    )
    print(
        "  Question: What semantic SourceType should "
        "GRETIL resources use?"
    )

    print()
    print(
        "Repository identity"
    )
    print(
        "  Question: Where should GRETIL / MW / "
        "other provider identity live?"
    )

    section("15. ARCHITECTURAL SAFETY CHECK")

    print(
        "SourceType.LOCAL   : invalid semantic category"
    )
    print(
        "SourceType.REMOTE  : invalid semantic category"
    )
    print(
        "SourceType.GRETIL  : invalid semantic category"
    )

    print()
    print(
        "No enum expansion is recommended by this audit."
    )

    print()
    print(
        "No automatic mapping is applied."
    )

    print()
    print(
        "The next production repair should be based only "
        "on the existing CorpusSource / WorkDefinition / "
        "provider metadata contracts established above."
    )

    print()
    print("=" * 112)
    print(
        "BATCH 5H-5E-12R-1 — "
        "SEMANTIC AUDIT COMPLETE"
    )
    print("=" * 112)


if __name__ == "__main__":
    main()
