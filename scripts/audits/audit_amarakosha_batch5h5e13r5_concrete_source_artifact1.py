
from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")

PRODUCTION_ROOTS = [
    ROOT / "acquisition",
    ROOT / "amarakosha",
    ROOT / "models",
    ROOT / "plugins",
    ROOT / "services",
    ROOT / "resources",
]


HISTORICAL_SUFFIX_RE = re.compile(
    r"(?:\d+|_G\d+)$"
)


def is_excluded(path: Path) -> bool:
    """
    Exclude tests, caches, audit/repair scripts and historical files.
    """
    parts = set(path.parts)
    stem = path.stem

    if "__pycache__" in parts:
        return True

    if "tests" in parts:
        return True

    if "scripts" in parts:
        return True

    if HISTORICAL_SUFFIX_RE.search(stem):
        return True

    return False


def production_python_files() -> list[Path]:
    files: set[Path] = set()

    for root in PRODUCTION_ROOTS:
        if not root.exists():
            continue

        if root.is_file() and root.suffix == ".py":
            if not is_excluded(root):
                files.add(root)
            continue

        if root.is_dir():
            for path in root.rglob("*.py"):
                if not is_excluded(path):
                    files.add(path)

    return sorted(files)


def parse(path: Path) -> ast.AST | None:
    try:
        return ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except (SyntaxError, UnicodeDecodeError):
        return None


def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def print_section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def main() -> None:
    print("=" * 100)
    print(
        "BATCH 5H-5E-13R-5 — "
        "CONCRETE AMARAKOSHA SOURCE-ARTIFACT AUDIT"
    )
    print("=" * 100)

    # ------------------------------------------------------------------
    # 1. Package bootstrap
    # ------------------------------------------------------------------

    print_section("1. PACKAGE BOOTSTRAP")

    try:
        import SanskritAI  # noqa: F401

        print("SanskritAI import : PASS")
    except Exception as exc:
        print(
            "SanskritAI import : FAIL"
        )
        print(
            f"error : {exc!r}"
        )
        raise

    # ------------------------------------------------------------------
    # 2. WorkRegistry
    # ------------------------------------------------------------------

    print_section("2. AMARAKOSHA WORK REGISTRY IDENTITY")

    try:
        from SanskritAI.acquisition.metadata.registries.work_registry import (
            WorkRegistry,
        )

        registry = WorkRegistry()
        work = registry.find_work("amarakosha")

        if work is None:
            work = registry.find_work("Amarakosha")

        if work is None:
            work = registry.find_work("अमरकोश")

        if work is None:
            raise RuntimeError(
                "Amarakośa WorkDefinition was not found."
            )

        print("WorkRegistry construction : PASS")
        print(f"identifier   : {getattr(work, 'identifier', None)!r}")
        print(f"title        : {getattr(work, 'title', None)!r}")
        print(
            f"corpus_type  : "
            f"{getattr(work, 'corpus_type', None)!r}"
        )
        print(
            f"language     : "
            f"{getattr(work, 'language', None)!r}"
        )
        print(
            f"script       : "
            f"{getattr(work, 'script', None)!r}"
        )
        print(
            f"repository   : "
            f"{getattr(work, 'repository', None)!r}"
        )
        print(
            f"metadata     : "
            f"{getattr(work, 'metadata', None)!r}"
        )
        print(
            f"aliases      : "
            f"{getattr(work, 'aliases', None)!r}"
        )

    except Exception as exc:
        print(
            f"WorkRegistry / Amarakośa lookup : FAIL — {exc!r}"
        )
        raise

    # ------------------------------------------------------------------
    # 3. Amarakośa production files
    # ------------------------------------------------------------------

    print_section("3. AMARAKOSHA PRODUCTION FILES")

    amarakosha_files: list[Path] = []

    for path in production_python_files():
        text = safe_read_text(path)

        if not text:
            continue

        if re.search(
            r"\bAmarakosha\b|\bamarakosha\b|अमरकोश",
            text,
            flags=re.IGNORECASE,
        ):
            amarakosha_files.append(path)

    print(
        f"Production Python files containing "
        f"Amarakośa references : {len(amarakosha_files)}"
    )

    for path in amarakosha_files:
        print(
            f"  {path.relative_to(ROOT)}"
        )

    # ------------------------------------------------------------------
    # 4. Concrete artifact candidates
    # ------------------------------------------------------------------

    print_section("4. CONCRETE SOURCE-ARTIFACT CANDIDATES")

    artifact_extensions = {
        ".txt",
        ".xml",
        ".tei",
        ".html",
        ".htm",
        ".json",
        ".yaml",
        ".yml",
        ".csv",
        ".tsv",
        ".pdf",
        ".epub",
        ".zip",
        ".gz",
        ".tgz",
        ".tar",
        ".md",
    }

    artifact_candidates: list[Path] = []

    search_roots = [
        ROOT / "resources",
        ROOT / "acquisition",
        ROOT / "amarakosha",
        ROOT / "models",
        ROOT / "plugins",
        ROOT / "services",
    ]

    for search_root in search_roots:
        if not search_root.exists():
            continue

        for path in search_root.rglob("*"):
            if not path.is_file():
                continue

            if is_excluded(path):
                continue

            if path.suffix.lower() not in artifact_extensions:
                continue

            name = path.name.lower()

            if (
                "amarakosha" in name
                or "amarakosa" in name
                or "amara" in name and "kosa" in name
            ):
                artifact_candidates.append(path)

    artifact_candidates = sorted(set(artifact_candidates))

    if artifact_candidates:
        print(
            f"Concrete filename-based candidates : "
            f"{len(artifact_candidates)}"
        )

        for path in artifact_candidates:
            try:
                size = path.stat().st_size
            except OSError:
                size = "?"

            print(
                f"  {path.relative_to(ROOT)}"
                f"    size={size}"
            )
    else:
        print(
            "Concrete filename-based candidates : 0"
        )

    # ------------------------------------------------------------------
    # 5. All non-Python Amarakośa-bearing files
    # ------------------------------------------------------------------

    print_section("5. NON-PYTHON AMARAKOSHA FILE CONTENT SEARCH")

    content_candidates: list[tuple[Path, str]] = []

    for search_root in search_roots:
        if not search_root.exists():
            continue

        for path in search_root.rglob("*"):
            if not path.is_file():
                continue

            if is_excluded(path):
                continue

            if path.suffix.lower() not in artifact_extensions:
                continue

            text = safe_read_text(path)

            if not text:
                continue

            if re.search(
                r"amarakosha|amarakosa|अमरकोश",
                text,
                flags=re.IGNORECASE,
            ):
                content_candidates.append(
                    (path, text)
                )

    if content_candidates:
        print(
            f"Content-bearing artifact candidates : "
            f"{len(content_candidates)}"
        )

        for path, text in content_candidates:
            matches = list(
                re.finditer(
                    r"amarakosha|amarakosa|अमरकोश",
                    text,
                    flags=re.IGNORECASE,
                )
            )

            print(
                f"  {path.relative_to(ROOT)}"
                f"    matches={len(matches)}"
                f"    size={path.stat().st_size}"
            )
    else:
        print(
            "Content-bearing artifact candidates : 0"
        )

    # ------------------------------------------------------------------
    # 6. Acquisition declarations
    # ------------------------------------------------------------------

    print_section("6. EXISTING ACQUISITION DECLARATIONS")

    acquisition_patterns = [
        "AmarakoshaManifest",
        "amarakosha_manifest",
        "AmarakoshaProvider",
        "amarakosha_provider",
        "AmarakoshaAcquirer",
        "amarakosha_acquirer",
        "AmarakoshaSource",
        "amarakosha_source",
        "AmarakoshaDownloader",
        "amarakosha_downloader",
        "source_type=SourceType.LEXICON",
        "SourceType.LEXICON",
        "AcquisitionManifest",
        "CorpusSourceFactory",
    ]

    production_files = production_python_files()

    for pattern in acquisition_patterns:
        matches: list[tuple[Path, int, str]] = []

        for path in production_files:
            text = safe_read_text(path)

            if not text:
                continue

            for lineno, line in enumerate(
                text.splitlines(),
                start=1,
            ):
                if pattern in line:
                    matches.append(
                        (
                            path,
                            lineno,
                            line.strip(),
                        )
                    )

        print()
        print(
            f"Pattern : {pattern!r}"
        )
        print(
            f"Matches : {len(matches)}"
        )

        for path, lineno, line in matches[:30]:
            print(
                f"  {path.relative_to(ROOT)}:"
                f"{lineno}: {line}"
            )

        if len(matches) > 30:
            print(
                f"  ... {len(matches) - 30} additional matches"
            )

    # ------------------------------------------------------------------
    # 7. Resource URL / source declarations
    # ------------------------------------------------------------------

    print_section("7. AMARAKOSHA URL / RESOURCE DECLARATIONS")

    url_patterns = [
        r"https?://[^\s\"']+",
        r"(?:url|source_url|download_url|homepage)"
        r"\s*=\s*[\"'][^\"']+[\"']",
    ]

    url_matches: list[tuple[Path, int, str]] = []

    for path in production_files:
        text = safe_read_text(path)

        if not text:
            continue

        if not re.search(
            r"amarakosha|amarakosa|अमरकोश",
            text,
            flags=re.IGNORECASE,
        ):
            continue

        for lineno, line in enumerate(
            text.splitlines(),
            start=1,
        ):
            if re.search(
                r"amarakosha|amarakosa|अमरकोश",
                line,
                flags=re.IGNORECASE,
            ) and any(
                re.search(pattern, line)
                for pattern in url_patterns
            ):
                url_matches.append(
                    (
                        path,
                        lineno,
                        line.strip(),
                    )
                )

    print(
        f"Amarakośa-related URL/resource lines : "
        f"{len(url_matches)}"
    )

    for path, lineno, line in url_matches:
        print(
            f"  {path.relative_to(ROOT)}:"
            f"{lineno}: {line}"
        )

    # ------------------------------------------------------------------
    # 8. Parser/importer boundary
    # ------------------------------------------------------------------

    print_section("8. EXISTING AMARAKOSHA PARSER / IMPORTER BOUNDARY")

    parser_importer_candidates = [
        ROOT
        / "amarakosha"
        / "parsers"
        / "amarakosha_parser.py",
        ROOT
        / "amarakosha"
        / "importers"
        / "amarakosha_importer.py",
        ROOT
        / "services"
        / "importers"
        / "amarakosha_parser.py",
        ROOT
        / "services"
        / "importers"
        / "amarakosha_importer.py",
    ]

    for path in parser_importer_candidates:
        if not path.exists():
            print(
                f"  {path.relative_to(ROOT)} : ABSENT"
            )
            continue

        try:
            tree = parse(path)

            if tree is None:
                print(
                    f"  {path.relative_to(ROOT)} : "
                    "AST PARSE FAIL"
                )
            else:
                classes = [
                    node.name
                    for node in tree.body
                    if isinstance(node, ast.ClassDef)
                ]

                functions = [
                    node.name
                    for node in tree.body
                    if isinstance(
                        node,
                        (ast.FunctionDef, ast.AsyncFunctionDef),
                    )
                ]

                print(
                    f"  {path.relative_to(ROOT)} : PRESENT"
                )
                print(
                    f"      classes   : {classes}"
                )
                print(
                    f"      functions : {functions}"
                )

        except Exception as exc:
            print(
                f"  {path.relative_to(ROOT)} : "
                f"ERROR {exc!r}"
            )

    # ------------------------------------------------------------------
    # 9. Parser input/resource clues
    # ------------------------------------------------------------------

    print_section("9. PARSER RESOURCE / INPUT CLUES")

    parser_paths = [
        path
        for path in parser_importer_candidates
        if path.exists()
    ]

    for path in parser_paths:
        text = safe_read_text(path)

        print()
        print(
            f"FILE : {path.relative_to(ROOT)}"
        )

        interesting_lines = []

        for lineno, line in enumerate(
            text.splitlines(),
            start=1,
        ):
            lowered = line.lower()

            if any(
                token in lowered
                for token in (
                    "xml",
                    "tei",
                    "txt",
                    "json",
                    "csv",
                    "pdf",
                    "path",
                    "file",
                    "source",
                    "input",
                    "parse",
                    "resource",
                )
            ):
                interesting_lines.append(
                    (lineno, line.strip())
                )

        for lineno, line in interesting_lines[:80]:
            print(
                f"  {lineno}: {line}"
            )

        if len(interesting_lines) > 80:
            print(
                f"  ... "
                f"{len(interesting_lines) - 80} additional lines"
            )

    # ------------------------------------------------------------------
    # 10. Explicit prohibition check
    # ------------------------------------------------------------------

    print_section("10. NEW AMARAKOSHA ACQUISITION ABSTRACTIONS")

    forbidden_new_abstractions = [
        "class AmarakoshaProvider",
        "class AmarakoshaAcquirer",
        "class AmarakoshaDownloader",
        "class AmarakoshaSource",
        "class AmarakoshaManifest",
    ]

    found_new_abstractions: list[tuple[Path, int, str]] = []

    for path in production_files:
        text = safe_read_text(path)

        for lineno, line in enumerate(
            text.splitlines(),
            start=1,
        ):
            for token in forbidden_new_abstractions:
                if token in line:
                    found_new_abstractions.append(
                        (
                            path,
                            lineno,
                            line.strip(),
                        )
                    )

    print(
        "Existing Amarakośa-specific acquisition classes "
        "found in production:"
    )

    if found_new_abstractions:
        for path, lineno, line in found_new_abstractions:
            print(
                f"  {path.relative_to(ROOT)}:"
                f"{lineno}: {line}"
            )
    else:
        print("  None")

    # ------------------------------------------------------------------
    # 11. Final interpretation
    # ------------------------------------------------------------------

    print_section("11. AUDIT INTERPRETATION")

    print(
        "This batch is READ-ONLY."
    )
    print(
        "No CorpusSource was created."
    )
    print(
        "No AcquisitionManifest was created."
    )
    print(
        "No Amarakośa-specific downloader/provider/acquirer "
        "was created."
    )
    print(
        "The purpose is to identify the concrete source artifact "
        "and existing acquisition/import boundaries."
    )

    print()
    print("=" * 100)
    print(
        "BATCH 5H-5E-13R-5 — RESULT: AUDIT COMPLETE"
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
