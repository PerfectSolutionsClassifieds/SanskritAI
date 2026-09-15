from __future__ import annotations

from pathlib import Path
import ast
import re


REPO_ROOT = Path("/content/SanskritAI")

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "_audit",
    "tests",
}

EXCLUDED_PYTHON_PATTERNS = (
    re.compile(r".*\d+\.py$"),
    re.compile(r".*_G\d+\.py$"),
)

SOURCE_TERMS = (
    "amarakosha",
    "amarakośa",
    "amara kosha",
    "amara-kośa",
    "अमरकोश",
    "अमरकोष",
)

ACQUISITION_CLASSES = (
    "AcquisitionManifest",
    "CorpusSource",
    "AcquisitionManager",
    "SourceAcquirer",
    "DefaultSourceAcquirer",
    "SourceManifest",
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

ACQUISITION_TERMS = (
    "source_url",
    "source_urls",
    "url",
    "urls",
    "manifest",
    "provider",
    "acquire",
    "acquisition",
    "download",
    "repository",
    "catalog",
    "resource",
    "raw",
    "input",
)


def is_excluded(path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return True

    if path.suffix == ".py":
        for pattern in EXCLUDED_PYTHON_PATTERNS:
            if pattern.match(path.name):
                return True

    return False


def read_text(path: Path, limit: int = 250_000) -> str:
    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )[:limit]
    except Exception:
        return ""


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def source_matches(text: str) -> list[str]:
    lower = text.lower()
    return [
        term
        for term in SOURCE_TERMS
        if term.lower() in lower
    ]


def acquisition_matches(text: str) -> list[str]:
    lower = text.lower()
    return [
        term
        for term in ACQUISITION_TERMS
        if term.lower() in lower
    ]


def provider_matches(text: str) -> list[str]:
    lower = text.lower()
    return [
        term
        for term in PROVIDER_TERMS
        if term.lower() in lower
    ]


def python_definitions(path: Path) -> list[str]:
    if path.suffix != ".py":
        return []

    text = read_text(path)

    if not text:
        return []

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []

    results: list[str] = []

    for node in ast.walk(tree):
        if isinstance(
            node,
            (
                ast.ClassDef,
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            results.append(node.name)

    return results


print("=" * 115)
print("BATCH 5H-5E-6 — AMARAKOSHA EXISTING ACQUISITION BOUNDARY TRACE")
print("=" * 115)


# ---------------------------------------------------------------------
# 1. EXISTING ACQUISITION COMPONENTS
# ---------------------------------------------------------------------

print("\n" + "-" * 115)
print("1. EXISTING ACQUISITION COMPONENTS")
print("-" * 115)

component_candidates = []

for path in REPO_ROOT.rglob("*.py"):
    if is_excluded(path):
        continue

    text = read_text(path)

    if not text:
        continue

    definitions = python_definitions(path)

    hits = [
        name
        for name in definitions
        if name in ACQUISITION_CLASSES
    ]

    if hits:
        component_candidates.append(
            (rel(path), hits)
        )

if not component_candidates:
    print("No existing acquisition component definitions found.")
else:
    for path_name, definitions in component_candidates:
        print()
        print(f"FILE       : {path_name}")
        print(f"DEFINITIONS: {definitions}")


# ---------------------------------------------------------------------
# 2. ACQUISITION MANIFEST / CORPUS SOURCE FILES
# ---------------------------------------------------------------------

print("\n" + "-" * 115)
print("2. ACQUISITION MANIFEST / CORPUS SOURCE INVENTORY")
print("-" * 115)

manifest_files = []

for path in REPO_ROOT.rglob("*"):
    if not path.is_file():
        continue

    if is_excluded(path):
        continue

    name = path.name.lower()

    if (
        "manifest" in name
        or "corpus_source" in name
        or "source_manifest" in name
    ):
        manifest_files.append(path)

if not manifest_files:
    print("No manifest/source files found.")
else:
    for path in sorted(manifest_files):
        print(f"{rel(path)}")


# ---------------------------------------------------------------------
# 3. AMARAKOSHA + ACQUISITION CROSS-REFERENCES
# ---------------------------------------------------------------------

print("\n" + "-" * 115)
print("3. AMARAKOSHA + ACQUISITION CROSS-REFERENCES")
print("-" * 115)

cross_refs = []

for path in REPO_ROOT.rglob("*"):
    if not path.is_file():
        continue

    if is_excluded(path):
        continue

    if path.suffix.lower() not in {
        ".py",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".txt",
        ".xml",
        ".tei",
        ".html",
        ".htm",
        ".md",
        ".rst",
    }:
        continue

    text = read_text(path)

    if not text:
        continue

    source_hits = source_matches(text)
    acquisition_hits = acquisition_matches(text)

    if source_hits and acquisition_hits:
        cross_refs.append(
            (
                rel(path),
                source_hits,
                acquisition_hits,
                provider_matches(text),
            )
        )

if not cross_refs:
    print("No Amarakośa + acquisition cross-reference found.")
else:
    for path_name, sources, acquisition, providers in cross_refs:
        print()
        print(f"FILE       : {path_name}")
        print(f"SOURCE     : {sources}")
        print(f"ACQUISITION: {acquisition}")
        print(
            f"PROVIDERS  : {providers if providers else 'NONE'}"
        )


# ---------------------------------------------------------------------
# 4. AMARAKOSHA REFERENCES INSIDE ACQUISITION DIRECTORY
# ---------------------------------------------------------------------

print("\n" + "-" * 115)
print("4. AMARAKOSHA REFERENCES INSIDE acquisition/")
print("-" * 115)

acquisition_root = REPO_ROOT / "acquisition"

if not acquisition_root.exists():
    print("acquisition/ directory is missing.")
else:
    acquisition_hits = []

    for path in acquisition_root.rglob("*"):
        if not path.is_file():
            continue

        if is_excluded(path):
            continue

        text = read_text(path)

        if not text:
            continue

        source_hits = source_matches(text)

        if source_hits:
            acquisition_hits.append(
                (
                    rel(path),
                    source_hits,
                    provider_matches(text),
                    acquisition_matches(text),
                )
            )

    if not acquisition_hits:
        print(
            "No direct Amarakośa references found inside acquisition/."
        )
    else:
        for path_name, sources, providers, acquisition in acquisition_hits:
            print()
            print(f"FILE       : {path_name}")
            print(f"SOURCE     : {sources}")
            print(
                f"PROVIDERS  : "
                f"{providers if providers else 'NONE'}"
            )
            print(
                f"ACQUISITION: "
                f"{acquisition if acquisition else 'NONE'}"
            )


# ---------------------------------------------------------------------
# 5. PROVIDER INVENTORY
# ---------------------------------------------------------------------

print("\n" + "-" * 115)
print("5. EXISTING PROVIDER INVENTORY")
print("-" * 115)

provider_root = REPO_ROOT / "acquisition" / "providers"

if not provider_root.exists():
    print("acquisition/providers/ directory is missing.")
else:
    provider_files = [
        path
        for path in provider_root.rglob("*")
        if path.is_file() and not is_excluded(path)
    ]

    if not provider_files:
        print("No provider files found.")
    else:
        for path in sorted(provider_files):
            print(rel(path))


# ---------------------------------------------------------------------
# 6. PROVIDER + AMARAKOSHA CROSS-REFERENCE
# ---------------------------------------------------------------------

print("\n" + "-" * 115)
print("6. PROVIDER + AMARAKOSHA CROSS-REFERENCE")
print("-" * 115)

provider_matches_found = []

if provider_root.exists():
    for path in provider_root.rglob("*"):
        if not path.is_file():
            continue

        if is_excluded(path):
            continue

        text = read_text(path)

        if not text:
            continue

        source_hits = source_matches(text)

        if source_hits:
            provider_matches_found.append(
                (
                    rel(path),
                    source_hits,
                    provider_matches(text),
                )
            )

if not provider_matches_found:
    print(
        "No direct Amarakośa references found inside "
        "provider implementations."
    )
else:
    for path_name, sources, providers in provider_matches_found:
        print()
        print(f"FILE      : {path_name}")
        print(f"AMARAKOSHA: {sources}")
        print(f"PROVIDERS : {providers}")


# ---------------------------------------------------------------------
# 7. EXECUTABLE SOURCE URL / MANIFEST EVIDENCE
# ---------------------------------------------------------------------

print("\n" + "-" * 115)
print("7. EXECUTABLE SOURCE URL / MANIFEST EVIDENCE")
print("-" * 115)

url_pattern = re.compile(
    r"""https?://[^\s"'<>]+|ftp://[^\s"'<>]+"""
)

url_hits = []

for path in REPO_ROOT.rglob("*.py"):
    if is_excluded(path):
        continue

    text = read_text(path)

    if not text:
        continue

    source_hits = source_matches(text)

    if not source_hits:
        continue

    urls = sorted(set(url_pattern.findall(text)))

    if urls:
        url_hits.append(
            (rel(path), source_hits, urls)
        )

if not url_hits:
    print(
        "No executable Amarakośa source URLs found."
    )
else:
    for path_name, sources, urls in url_hits:
        print()
        print(f"FILE      : {path_name}")
        print(f"AMARAKOSHA: {sources}")
        for url in urls:
            print(f"URL       : {url}")


# ---------------------------------------------------------------------
# 8. ACQUISITION BOUNDARY DECISION
# ---------------------------------------------------------------------

print("\n" + "-" * 115)
print("8. ACQUISITION BOUNDARY DECISION")
print("-" * 115)

direct_acquisition_evidence = [
    item
    for item in cross_refs
    if "acquisition/" in item[0]
]

direct_provider_evidence = provider_matches_found

if direct_acquisition_evidence:
    print(
        "DIRECT AMARAKOSHA ACQUISITION EVIDENCE : FOUND"
    )
elif direct_provider_evidence:
    print(
        "AMARAKOSHA PROVIDER EVIDENCE            : FOUND"
    )
else:
    print(
        "DIRECT AMARAKOSHA ACQUISITION EVIDENCE : NOT FOUND"
    )
    print(
        "DIRECT AMARAKOSHA PROVIDER EVIDENCE    : NOT FOUND"
    )

if url_hits:
    print(
        "EXECUTABLE SOURCE URL EVIDENCE         : FOUND"
    )
else:
    print(
        "EXECUTABLE SOURCE URL EVIDENCE         : NOT FOUND"
    )


# ---------------------------------------------------------------------
# 9. FINAL ARCHITECTURAL GATE
# ---------------------------------------------------------------------

print("\n" + "-" * 115)
print("9. FINAL ARCHITECTURAL GATE")
print("-" * 115)

print("Existing acquisition architecture : PRESERVE")
print("Existing AcquisitionManifest      : PRESERVE")
print("Existing CorpusSource             : PRESERVE")
print("Existing providers                : PRESERVE")
print("Existing AcquisitionManager       : PRESERVE")
print("Existing SourceAcquirer           : PRESERVE")
print("Existing AmarakoshaParser         : PRESERVE")
print("Existing SynsetRecord/VargaRecord : PRESERVE")
print("New Amarakośa provider            : NOT JUSTIFIED YET")
print("New source model                  : NOT JUSTIFIED YET")
print("New parser grammar                : DO NOT IMPLEMENT")
print("Raw source acquisition            : DO NOT INVENT")

print("\nNEXT STEP:")
print(
    "Use the concrete acquisition evidence found above "
    "to identify the authoritative Amarakośa source boundary."
)

print(
    "Only after that boundary is established should the "
    "actual source artifact be acquired/inspected."
)

print(
    "\nBATCH 5H-5E-6 STATUS: AUDIT COMPLETE"
)

print("=" * 115)
