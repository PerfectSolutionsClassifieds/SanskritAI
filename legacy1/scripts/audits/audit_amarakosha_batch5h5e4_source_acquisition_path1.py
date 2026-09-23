
from __future__ import annotations

"""
SanskritAI
==========

Batch 5H-5E-4
Amarakośa Source Artifact / Acquisition Path Audit

Purpose
-------
Read-only audit to determine whether the repository already contains:

1. An actual Amarakośa source artifact,
2. An Amarakośa source URL/reference,
3. An existing acquisition manifest,
4. An existing provider/discovery path,
5. An existing downloaded/raw Amarakośa source,
6. A documented source-format specification.

This audit does NOT implement:

- AmarakośaParser.parse()
- parser grammar
- a new Amarakośa source model
- a new provider
- a new acquisition abstraction
- new record types
- canonical dictionary mapping

Historical / duplicate implementation files are excluded from
production conclusions, including:

- tests
- __pycache__
- Python files whose stem ends in digits
- *_G<number>.py
- _audit artifacts

Version
-------
v0.1.0
"""

from pathlib import Path
import ast
import re
import sys


# ---------------------------------------------------------------------------
# Repository bootstrap
# ---------------------------------------------------------------------------

REPO_ROOT = Path("/content/SanskritAI")

if "/content" not in sys.path:
    sys.path.insert(0, "/content")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEARCH_ROOTS = (
    REPO_ROOT / "acquisition",
    REPO_ROOT / "amarakosha",
    REPO_ROOT / "data",
    REPO_ROOT / "resources",
    REPO_ROOT / "docs",
    REPO_ROOT / "scripts",
)

TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".rst",
    ".json",
    ".yaml",
    ".yml",
    ".xml",
    ".tei",
    ".html",
    ".htm",
    ".csv",
    ".toml",
}

PYTHON_EXTENSIONS = {".py"}

EXCLUDED_DIR_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".coverage",
    "tests",
    "_audit",
}

SOURCE_TERMS = (
    "amarakosha",
    "amarakośa",
    "amara kosha",
    "amara-kośa",
    "अमरकोश",
    "अमरकोष",
)

ACQUISITION_TERMS = (
    "manifest",
    "provider",
    "acquire",
    "acquisition",
    "download",
    "source_url",
    "url",
    "repository",
    "catalog",
    "resource",
    "corpus",
    "raw",
    "input",
)

FORMAT_TERMS = (
    "txt",
    "xml",
    "tei",
    "html",
    "json",
    "csv",
    "text",
    "plaintext",
    "unicode",
    "devanagari",
    "iast",
    "sanskrit",
)

PROVIDER_TERMS = (
    "gretil",
    "cologne",
    "github",
    "internet_archive",
    "sarit",
    "sanskritdocuments",
    "muktabodha",
    "xml_corpus",
)


# ---------------------------------------------------------------------------
# File filtering
# ---------------------------------------------------------------------------

def is_historical_or_duplicate(path: Path) -> bool:
    """
    Exclude known historical / duplicate Python variants.
    """

    stem = path.stem

    if re.search(r"_G\d+$", stem, flags=re.IGNORECASE):
        return True

    if re.search(r"\d+$", stem):
        return True

    return False


def is_excluded(path: Path) -> bool:
    """
    Exclude tests, caches and audit artifacts.
    """

    if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
        return True

    if path.suffix.lower() == ".py" and is_historical_or_duplicate(path):
        return True

    return False


def iter_files() -> list[Path]:
    """
    Return active repository files under the audit roots.
    """

    results: list[Path] = []

    for root in SEARCH_ROOTS:
        if not root.exists():
            continue

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if is_excluded(path):
                continue

            results.append(path)

    return sorted(set(results))


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def safe_read(path: Path) -> str:
    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    except Exception:
        return ""


def contains_any(
    text: str,
    terms: tuple[str, ...],
) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def matched_terms(
    text: str,
    terms: tuple[str, ...],
) -> list[str]:
    lowered = text.lower()

    return [
        term
        for term in terms
        if term.lower() in lowered
    ]


def preview(
    text: str,
    limit: int = 1400,
) -> str:
    compact = " ".join(text.split())
    return compact[:limit]


# ---------------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------------

def executable_symbol_references(
    path: Path,
) -> list[str]:
    """
    Return executable references to Amarakośa/acquisition symbols.

    Docstrings/comments are not treated as executable evidence.
    """

    if path.suffix != ".py":
        return []

    text = safe_read(path)

    try:
        tree = ast.parse(
            text,
            filename=str(path),
        )
    except SyntaxError:
        return []

    references: list[str] = []

    interesting = {
        "Amarakosha",
        "AmarakoshaParser",
        "AmarakoshaImporter",
        "AmarakoshaRegistry",
        "SourceManifest",
        "AcquisitionManager",
        "DefaultSourceAcquirer",
        "SourceAcquisitionRequest",
    }

    for node in ast.walk(tree):

        if isinstance(node, ast.Name):
            if node.id in interesting:
                references.append(node.id)

        elif isinstance(node, ast.Attribute):
            if node.attr in interesting:
                references.append(node.attr)

    return references


def url_like_strings(path: Path) -> list[str]:
    """
    Extract URL-like string literals from active Python source.
    """

    if path.suffix != ".py":
        return []

    text = safe_read(path)

    try:
        tree = ast.parse(
            text,
            filename=str(path),
        )
    except SyntaxError:
        return []

    urls: list[str] = []

    for node in ast.walk(tree):

        if not isinstance(node, ast.Constant):
            continue

        if not isinstance(node.value, str):
            continue

        value = node.value.strip()

        if value.startswith(
            (
                "http://",
                "https://",
                "ftp://",
            )
        ):
            urls.append(value)

    return urls


# ---------------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------------

def main() -> None:

    print("=" * 115)
    print(
        "BATCH 5H-5E-4 — AMARAKOSHA SOURCE ARTIFACT / "
        "ACQUISITION PATH AUDIT"
    )
    print("=" * 115)

    files = iter_files()

    # -----------------------------------------------------------------------
    # 1. Repository baseline
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("1. REPOSITORY SOURCE ROOTS")
    print("-" * 115)

    for root in SEARCH_ROOTS:
        print(
            f"{root.relative_to(REPO_ROOT):<25}",
            "EXISTS" if root.exists() else "MISSING",
        )

    # -----------------------------------------------------------------------
    # 2. Amarakośa source artifact candidates
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("2. AMARAKOSHA SOURCE ARTIFACT CANDIDATES")
    print("-" * 115)

    source_candidates: list[Path] = []

    for path in files:

        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        text = safe_read(path)

        if not text:
            continue

        if not contains_any(text, SOURCE_TERMS):
            continue

        source_candidates.append(path)

    print(
        "Text files containing Amarakośa source identity:",
        len(source_candidates),
    )

    for path in source_candidates:

        text = safe_read(path)

        print("\nFILE:", path.relative_to(REPO_ROOT))
        print(
            "Source terms:",
            matched_terms(text, SOURCE_TERMS),
        )
        print("Preview:", preview(text))

    # -----------------------------------------------------------------------
    # 3. Actual Sanskrit text candidates
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("3. POSSIBLE RAW SANSKRIT SOURCE TEXT")
    print("-" * 115)

    devanagari_pattern = re.compile(
        r"[\u0900-\u097F]{4,}"
    )

    sanskrit_candidates: list[Path] = []

    for path in files:

        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        text = safe_read(path)

        if not text:
            continue

        devanagari_matches = devanagari_pattern.findall(text)

        if len(devanagari_matches) < 3:
            continue

        if contains_any(text, SOURCE_TERMS):
            sanskrit_candidates.append(path)

    print(
        "Files containing both Amarakośa identity and "
        "substantial Devanagari text:",
        len(sanskrit_candidates),
    )

    for path in sanskrit_candidates:

        text = safe_read(path)
        matches = devanagari_pattern.findall(text)

        print("\nFILE:", path.relative_to(REPO_ROOT))
        print(
            "Devanagari sample:",
            " | ".join(matches[:12]),
        )

    # -----------------------------------------------------------------------
    # 4. Acquisition-related evidence
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("4. ACQUISITION / MANIFEST EVIDENCE")
    print("-" * 115)

    acquisition_candidates: list[Path] = []

    for path in files:

        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        text = safe_read(path)

        if not text:
            continue

        if (
            contains_any(text, SOURCE_TERMS)
            and contains_any(text, ACQUISITION_TERMS)
        ):
            acquisition_candidates.append(path)

    print(
        "Files containing Amarakośa + acquisition/source terms:",
        len(acquisition_candidates),
    )

    for path in acquisition_candidates:

        text = safe_read(path)

        print("\nFILE:", path.relative_to(REPO_ROOT))
        print(
            "Source terms:",
            matched_terms(text, SOURCE_TERMS),
        )
        print(
            "Acquisition terms:",
            matched_terms(text, ACQUISITION_TERMS),
        )
        print("Preview:", preview(text))

    # -----------------------------------------------------------------------
    # 5. Provider evidence
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("5. PROVIDER / SOURCE REGISTRY EVIDENCE")
    print("-" * 115)

    provider_hits: dict[str, list[Path]] = {
        provider: []
        for provider in PROVIDER_TERMS
    }

    for path in files:

        if path.suffix.lower() not in (
            TEXT_EXTENSIONS | PYTHON_EXTENSIONS
        ):
            continue

        text = safe_read(path)

        if not text:
            continue

        if not contains_any(text, SOURCE_TERMS):
            continue

        lowered = text.lower()

        for provider in PROVIDER_TERMS:
            if provider.lower() in lowered:
                provider_hits[provider].append(path)

    for provider, locations in provider_hits.items():

        if not locations:
            continue

        print(f"\nPROVIDER: {provider}")

        for path in sorted(set(locations)):
            print(
                " ",
                path.relative_to(REPO_ROOT),
            )

    # -----------------------------------------------------------------------
    # 6. Python acquisition architecture
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("6. EXECUTABLE ACQUISITION ARCHITECTURE REFERENCES")
    print("-" * 115)

    python_files = [
        path
        for path in files
        if path.suffix == ".py"
    ]

    executable_hits = 0

    for path in python_files:

        references = executable_symbol_references(path)

        if not references:
            continue

        executable_hits += 1

        print("\nFILE:", path.relative_to(REPO_ROOT))
        print(
            "Executable references:",
            sorted(set(references)),
        )

    print(
        "\nPython files with relevant executable references:",
        executable_hits,
    )

    # -----------------------------------------------------------------------
    # 7. URL evidence
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("7. SOURCE URL EVIDENCE")
    print("-" * 115)

    url_hits: list[tuple[Path, str]] = []

    for path in python_files:

        urls = url_like_strings(path)

        if not urls:
            continue

        text = safe_read(path)

        if not contains_any(text, SOURCE_TERMS):
            continue

        for url in urls:
            url_hits.append((path, url))

    if not url_hits:
        print(
            "No executable Amarakośa-related URL literals found."
        )

    else:

        for path, url in url_hits:
            print(
                path.relative_to(REPO_ROOT),
                "->",
                url,
            )

    # -----------------------------------------------------------------------
    # 8. Format evidence
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("8. SOURCE FORMAT EVIDENCE")
    print("-" * 115)

    format_hits: dict[str, list[Path]] = {
        term: []
        for term in FORMAT_TERMS
    }

    for path in files:

        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        text = safe_read(path)

        if not contains_any(text, SOURCE_TERMS):
            continue

        lowered = text.lower()

        for term in FORMAT_TERMS:

            if term.lower() in lowered:
                format_hits[term].append(path)

    for term, locations in format_hits.items():

        if not locations:
            continue

        print(
            f"{term:<15}",
            len(set(locations)),
            "file(s)",
        )

    # -----------------------------------------------------------------------
    # 9. Source artifact classification
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("9. SOURCE ARTIFACT CLASSIFICATION")
    print("-" * 115)

    print(
        "Actual raw Amarakośa source text:",
        "FOUND"
        if sanskrit_candidates
        else "NOT FOUND",
    )

    print(
        "Amarakośa acquisition reference:",
        "FOUND"
        if acquisition_candidates
        else "NOT FOUND",
    )

    print(
        "Executable Amarakośa source URL:",
        "FOUND"
        if url_hits
        else "NOT FOUND",
    )

    # -----------------------------------------------------------------------
    # 10. Architectural decision gate
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("10. 5H-5E-4 DECISION GATE")
    print("-" * 115)

    print("Existing acquisition architecture : PRESERVE")
    print("Existing parser                  : PRESERVE")
    print("Existing record contracts        : PRESERVE")
    print("New source model                 : NOT JUSTIFIED YET")
    print("New provider                     : NOT JUSTIFIED YET")
    print("New parser grammar               : DO NOT IMPLEMENT YET")

    if sanskrit_candidates:

        print(
            "Actual source artifact          : "
            "FOUND — inspect exact artifact next"
        )

    else:

        print(
            "Actual source artifact          : "
            "NOT FOUND IN ACTIVE REPOSITORY"
        )

    if acquisition_candidates:

        print(
            "Acquisition path                : "
            "EVIDENCE FOUND — inspect existing path next"
        )

    else:

        print(
            "Acquisition path                : "
            "NOT ESTABLISHED FOR AMARAKOSHA"
        )

    if url_hits:

        print(
            "Source URL                      : "
            "EVIDENCE FOUND"
        )

    else:

        print(
            "Source URL                      : "
            "NOT ESTABLISHED"
        )

    print(
        "\nNext step : "
        "Determine the concrete Amarakośa source artifact and "
        "its existing acquisition boundary before implementing parse()."
    )

    print("\n" + "=" * 115)
    print("BATCH 5H-5E-4 — AUDIT COMPLETE")
    print("=" * 115)


if __name__ == "__main__":
    main()
