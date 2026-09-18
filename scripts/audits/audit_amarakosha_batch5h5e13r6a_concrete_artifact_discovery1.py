from __future__ import annotations

"""
BATCH 5H-5E-13R-6A
Concrete Amarakośa Source-Artifact Discovery Audit

Purpose
-------
The preceding 13R-6 CorpusSource declaration audit established that:

    - canonical CorpusSource exists
    - SourceType.LEXICON exists
    - SourceFormat.TXT exists
    - Amarakośa parser/importer expects UTF-8 text
    - WorkDefinition identity exists
    - BUT no concrete Amarakośa source artifact was established

This audit therefore performs READ-ONLY discovery.

It does NOT:
    - create a CorpusSource
    - create an AcquisitionManifest
    - modify production code
    - modify enums
    - create providers/acquirers
    - invent a URL
    - infer a source artifact from documentation alone

It searches the repository and Git metadata for concrete evidence.

Historical/duplicate production Python files are ignored:
    *_1.py
    *_2.py
    ...
    *_G<number>.py

Tests and __pycache__ are ignored.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


# =============================================================================
# CONSTANTS
# =============================================================================

REPO_ROOT = Path("/content/SanskritAI")

SEARCH_DIRECTORIES = (
    "resources",
    "data",
    "datasets",
    "corpus",
    "acquisition",
    "amarakosha",
    "services",
    "plugins",
    "models",
)

NON_ARTIFACT_EXTENSIONS = {
    ".py",
    ".pyc",
    ".pyo",
}

LIKELY_ARTIFACT_EXTENSIONS = {
    ".txt",
    ".text",
    ".xml",
    ".tei",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
    ".tsv",
    ".sql",
    ".sqlite",
    ".db",
    ".pdf",
    ".epub",
    ".zip",
    ".tar",
    ".gz",
    ".tgz",
    ".7z",
    ".rar",
    ".md",
    ".html",
    ".htm",
}

IGNORED_DIRECTORY_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    "node_modules",
    ".venv",
    "venv",
}

DUPLICATE_PYTHON_RE = re.compile(
    r"(?:_\d+|_G\d+)\.py$",
    re.IGNORECASE,
)

AMARAKOSHA_RE = re.compile(
    r"amarak[oó]sha|amarakosa|अमरकोश|अमरकोष|amarakosha",
    re.IGNORECASE,
)

SOURCE_URL_RE = re.compile(
    r"https?://[^\s\"'<>]+",
    re.IGNORECASE,
)


# =============================================================================
# HELPERS
# =============================================================================

def print_header(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def is_ignored_path(path: Path) -> bool:
    parts = set(path.parts)

    if parts & IGNORED_DIRECTORY_NAMES:
        return True

    if "tests" in parts:
        return True

    if path.suffix.lower() == ".py" and DUPLICATE_PYTHON_RE.search(path.name):
        return True

    return False


def is_candidate_artifact(path: Path) -> bool:
    if not path.is_file():
        return False

    if is_ignored_path(path):
        return False

    if path.suffix.lower() in NON_ARTIFACT_EXTENSIONS:
        return False

    return path.suffix.lower() in LIKELY_ARTIFACT_EXTENSIONS


def safe_read_text(path: Path, limit: int = 200_000) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return handle.read(limit)
    except Exception:
        return ""


def git_output(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


# =============================================================================
# 1. PACKAGE BOOTSTRAP
# =============================================================================

print_header("BATCH 5H-5E-13R-6A — CONCRETE AMARAKOSHA ARTIFACT DISCOVERY")

print_header("1. PACKAGE / REPOSITORY BOOTSTRAP")

print("Repository root :", REPO_ROOT)
print("Repository exists :", REPO_ROOT.exists())

if not REPO_ROOT.exists():
    print("RESULT : FAIL — repository root does not exist.")
    raise SystemExit(1)

parent = REPO_ROOT.parent

if str(parent) not in sys.path:
    sys.path.insert(0, str(parent))

print("Repository parent :", parent)
print("Added to sys.path :", parent)

try:
    import SanskritAI

    print("SanskritAI import : PASS")
    print("SanskritAI.__file__ :", SanskritAI.__file__)
except Exception as exc:
    print("SanskritAI import : FAIL")
    print("error :", repr(exc))
    raise SystemExit(1)


# =============================================================================
# 2. REPOSITORY TREE — NON-PYTHON ARTIFACT INVENTORY
# =============================================================================

print_header("2. REPOSITORY NON-PYTHON ARTIFACT INVENTORY")

all_candidate_files: list[Path] = []

for directory_name in SEARCH_DIRECTORIES:
    directory = REPO_ROOT / directory_name

    if not directory.exists():
        print(f"{directory_name}/ : NOT PRESENT")
        continue

    print(f"{directory_name}/ : PRESENT")

    for path in directory.rglob("*"):
        if is_candidate_artifact(path):
            all_candidate_files.append(path)

all_candidate_files = sorted(
    set(all_candidate_files),
    key=lambda p: str(p).lower(),
)

print()
print("Candidate non-Python artifacts :", len(all_candidate_files))

for path in all_candidate_files:
    try:
        size = path.stat().st_size
    except Exception:
        size = "?"

    print(f"  {relative(path)}    size={size}")


# =============================================================================
# 3. AMARAKOSHA-NAMED ARTIFACT SEARCH
# =============================================================================

print_header("3. AMARAKOSHA-NAMED CONCRETE ARTIFACT SEARCH")

named_artifacts: list[Path] = []

for path in all_candidate_files:
    if AMARAKOSHA_RE.search(path.name):
        named_artifacts.append(path)

print("Amarakośa-named artifacts :", len(named_artifacts))

if named_artifacts:
    for path in named_artifacts:
        print("  FOUND :", relative(path))
else:
    print("NO AMARAKOSHA-NAMED NON-PYTHON ARTIFACT FOUND.")


# =============================================================================
# 4. CONTENT-BASED ARTIFACT SEARCH
# =============================================================================

print_header("4. CONTENT-BASED AMARAKOSHA ARTIFACT SEARCH")

content_matches: list[tuple[Path, list[str]]] = []

for path in all_candidate_files:
    text = safe_read_text(path)

    if not text:
        continue

    lines = text.splitlines()
    matches = []

    for index, line in enumerate(lines, start=1):
        if AMARAKOSHA_RE.search(line):
            matches.append(f"{index}: {line[:300]}")

    if matches:
        content_matches.append((path, matches[:10]))

print("Artifacts containing Amarakośa lexical clues :", len(content_matches))

for path, matches in content_matches:
    print()
    print("FILE :", relative(path))

    for match in matches:
        print(" ", match)


# =============================================================================
# 5. GIT-TRACKED ARTIFACT SEARCH
# =============================================================================

print_header("5. GIT-TRACKED NON-PYTHON ARTIFACT SEARCH")

tracked = git_output(
    "ls-files",
)

tracked_paths = []

for line in tracked.splitlines():
    if not line.strip():
        continue

    path = REPO_ROOT / line.strip()

    if not path.exists():
        continue

    if is_ignored_path(path):
        continue

    if is_candidate_artifact(path):
        tracked_paths.append(path)

tracked_paths = sorted(
    set(tracked_paths),
    key=lambda p: str(p).lower(),
)

print("Git-tracked candidate artifacts :", len(tracked_paths))

for path in tracked_paths:
    print(" ", relative(path))


# =============================================================================
# 6. GIT HISTORY SEARCH FOR AMARAKOSHA ARTIFACT NAMES
# =============================================================================

print_header("6. GIT HISTORY — AMARAKOSHA ARTIFACT NAME SEARCH")

history_name_output = git_output(
    "log",
    "--all",
    "--name-only",
    "--pretty=format:",
    "--",
    "*amarakosha*",
    "*amarakosa*",
)

history_names = sorted(
    {
        line.strip()
        for line in history_name_output.splitlines()
        if line.strip()
    },
    key=str.lower,
)

print("Historical Amarakośa-named paths :", len(history_names))

for path in history_names:
    print(" ", path)

if not history_names:
    print("NO HISTORICAL AMARAKOSHA-NAMED PATH FOUND.")


# =============================================================================
# 7. GIT HISTORY CONTENT SEARCH
# =============================================================================

print_header("7. GIT HISTORY — AMARAKOSHA CONTENT CLUES")

history_grep = git_output(
    "log",
    "--all",
    "-Samarakosha",
    "--oneline",
)

history_grep_lines = [
    line for line in history_grep.splitlines()
    if line.strip()
]

print("Commits containing -Samarakosha history matches :",
      len(history_grep_lines))

for line in history_grep_lines[:50]:
    print(" ", line)

history_grep2 = git_output(
    "log",
    "--all",
    "-Samarakosa",
    "--oneline",
)

history_grep2_lines = [
    line for line in history_grep2.splitlines()
    if line.strip()
]

print()
print("Commits containing -SAmarakosa history matches :",
      len(history_grep2_lines))

for line in history_grep2_lines[:50]:
    print(" ", line)


# =============================================================================
# 8. SOURCE URL SEARCH IN PRODUCTION ARTIFACTS
# =============================================================================

print_header("8. SOURCE URL SEARCH IN AMARAKOSHA-RELATED ARTIFACT CONTENT")

url_evidence: list[tuple[Path, str, list[str]]] = []

for path, matches in content_matches:
    text = safe_read_text(path)

    urls = SOURCE_URL_RE.findall(text)

    if urls:
        relevant_urls = []

        for url in urls:
            if AMARAKOSHA_RE.search(url):
                relevant_urls.append(url)

        if relevant_urls:
            url_evidence.append(
                (path, relative(path), sorted(set(relevant_urls)))
            )

print("Amarakośa-specific URL evidence :", len(url_evidence))

for path, rel, urls in url_evidence:
    print()
    print("FILE :", rel)

    for url in urls:
        print("  URL :", url)


# =============================================================================
# 9. SOURCE-LOCATION CLUES
# =============================================================================

print_header("9. SOURCE-LOCATION / RESOURCE-PATH CLUES")

location_clues: list[tuple[Path, str]] = []

location_terms = (
    "amarakosha.txt",
    "amarakosa.txt",
    "amarakosha/",
    "amarakosa/",
    "amarakosha",
    "amarakosa",
)

production_python_files = []

for directory_name in SEARCH_DIRECTORIES:
    directory = REPO_ROOT / directory_name

    if not directory.exists():
        continue

    for path in directory.rglob("*.py"):
        if is_ignored_path(path):
            continue
        production_python_files.append(path)

for path in sorted(set(production_python_files), key=lambda p: str(p).lower()):
    text = safe_read_text(path)

    if not text:
        continue

    for index, line in enumerate(text.splitlines(), start=1):
        lower = line.lower()

        if any(term in lower for term in location_terms):
            location_clues.append(
                (path, f"{index}: {line[:400]}")
            )

print("Production source-location clues :", len(location_clues))

for path, clue in location_clues[:100]:
    print(f"  {relative(path)}:{clue}")


# =============================================================================
# 10. ARTIFACT CLASSIFICATION
# =============================================================================

print_header("10. ARTIFACT CLASSIFICATION")

print("Named concrete artifacts       :", len(named_artifacts))
print("Content-matched artifacts      :", len(content_matches))
print("Git-tracked candidate artifacts:", len(tracked_paths))
print("Amarakośa-specific URL evidence:",
      len(url_evidence))
print("Location clues                  :", len(location_clues))


artifact_established = bool(named_artifacts)

if not artifact_established:
    # A content match can still be documentation/metadata.
    # Do not promote it automatically to a source artifact.
    print()
    print(
        "No Amarakośa-named concrete artifact has been established "
        "from repository artifact files."
    )


# =============================================================================
# 11. DECLARATION READINESS
# =============================================================================

print_header("11. 13R-6 CORPUSSOURCE DECLARATION READINESS")

if named_artifacts:
    print("CONCRETE ARTIFACT : FOUND")

    for path in named_artifacts:
        print("  artifact :", relative(path))

    if url_evidence:
        print("SOURCE LOCATION : URL EVIDENCE FOUND")
    elif location_clues:
        print("SOURCE LOCATION : PATH / CODE CLUES FOUND")
    else:
        print("SOURCE LOCATION : NOT ESTABLISHED")

    print()
    print(
        "NEXT ACTION : inspect the exact artifact and establish "
        "canonical source location before production declaration."
    )

else:
    print("CONCRETE ARTIFACT : NOT FOUND")
    print("SOURCE LOCATION   : NOT ESTABLISHED")
    print()
    print(
        "13R-6 remains BLOCKED."
    )
    print(
        "Do NOT create CorpusSource or AcquisitionManifest yet."
    )


# =============================================================================
# 12. FINAL RESULT
# =============================================================================

print_header("12. BATCH 5H-5E-13R-6A RESULT")

if named_artifacts:
    print(
        "RESULT : ARTIFACT CANDIDATE FOUND — "
        "REVIEW REQUIRED BEFORE 13R-6 PRODUCTION DECLARATION"
    )
else:
    print(
        "RESULT : BLOCKED — NO CONCRETE AMARAKOSHA ARTIFACT ESTABLISHED"
    )

print()
print("This audit is READ-ONLY.")
print("No production files were modified.")
print("No source URL was invented.")
print("No CorpusSource was created.")
print("No AcquisitionManifest was created.")
