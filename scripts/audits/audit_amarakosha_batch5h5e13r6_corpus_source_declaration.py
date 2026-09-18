
from __future__ import annotations

"""
BATCH 5H-5E-13R-6
CorpusSource Declaration Audit / Guard

Purpose
-------
Establish whether the existing SanskritAI evidence is sufficient to construct
a canonical CorpusSource for Amarakośa.

This stage intentionally does NOT create or modify a production
Amarakośa CorpusSource declaration.

The declaration may only be created after the following are established:

    1. Canonical Amarakośa WorkDefinition identity
    2. Concrete source artifact
    3. Artifact representation / format
    4. Artifact acquisition location
    5. Existing parser/importer input contract
    6. Source metadata sufficient for CorpusSource

Canonical flow:

    WorkRegistry / WorkDefinition
            ↓
    Concrete Amarakośa artifact
            ↓
    CorpusSource
            ↓
    AcquisitionManifest
            ↓
    Runtime acquisition
            ↓
    Existing Amarakośa parser/importer

Important
---------
DO NOT invent:

    - source URL
    - repository
    - filename
    - edition
    - publisher
    - author
    - checksum
    - local path
    - acquisition provider

from Amarakośa's name alone.

Production exclusions
---------------------
Ignore:

    - tests/
    - __pycache__/
    - audit scripts themselves
    - historical duplicate Python files ending in numeric suffixes
    - *_G<number>.py
"""

from pathlib import Path
import ast
import importlib
import re
import sys
import traceback


# ============================================================================
# PATHS
# ============================================================================

REPO_ROOT = Path("/content/SanskritAI")
PROJECT_PARENT = REPO_ROOT.parent

RESOURCE_ROOT = REPO_ROOT / "resources"
AMARAKOSHA_ROOT = REPO_ROOT / "amarakosha"
SERVICES_IMPORTER_ROOT = REPO_ROOT / "services" / "importers"

HISTORICAL_SUFFIX_RE = re.compile(r".*\d+\.py$", re.IGNORECASE)
GENERATION_SUFFIX_RE = re.compile(r"_G\d+\.py$", re.IGNORECASE)


# ============================================================================
# HELPERS
# ============================================================================

def section(number: str, title: str):
    print()
    print("=" * 100)
    print(f"{number}. {title}")
    print("=" * 100)


def is_excluded(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}

    if "tests" in parts:
        return True

    if "__pycache__" in parts:
        return True

    if path.suffix.lower() == ".py":
        if HISTORICAL_SUFFIX_RE.match(path.name):
            return True

        if GENERATION_SUFFIX_RE.match(path.name):
            return True

    try:
        if path.resolve() == Path(__file__).resolve():
            return True
    except Exception:
        pass

    return False


def safe_read(path: Path) -> str:
    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    except Exception:
        return ""


def iter_production_python_files():
    roots = [
        REPO_ROOT / "acquisition",
        REPO_ROOT / "amarakosha",
        REPO_ROOT / "services",
        REPO_ROOT / "models",
        REPO_ROOT / "plugins",
    ]

    seen = set()

    for root in roots:
        if not root.exists():
            continue

        for path in root.rglob("*.py"):
            if not path.is_file():
                continue

            if is_excluded(path):
                continue

            resolved = path.resolve()

            if resolved in seen:
                continue

            seen.add(resolved)
            yield path


# ============================================================================
# PACKAGE BOOTSTRAP
# ============================================================================

def bootstrap():
    section("1", "PACKAGE BOOTSTRAP")

    print("Repository root :", REPO_ROOT)
    print("Repository exists :", REPO_ROOT.exists())
    print("Repository parent :", PROJECT_PARENT)

    if not REPO_ROOT.exists():
        raise RuntimeError(
            f"SanskritAI repository does not exist: {REPO_ROOT}"
        )

    parent = str(PROJECT_PARENT)

    if parent not in sys.path:
        sys.path.insert(0, parent)
        print("Added to sys.path :", parent)
    else:
        print("Already in sys.path :", parent)

    importlib.invalidate_caches()

    try:
        import SanskritAI

        print("SanskritAI import : PASS")
        print(
            "SanskritAI.__file__ :",
            getattr(SanskritAI, "__file__", None),
        )

    except Exception as exc:
        print("SanskritAI import : FAIL")
        print("error :", repr(exc))
        traceback.print_exc()
        raise


# ============================================================================
# CANONICAL WORK DEFINITION
# ============================================================================

def audit_work_definition():
    section("2", "CANONICAL AMARAKOSHA WORK DEFINITION")

    path = (
        REPO_ROOT
        / "acquisition"
        / "metadata"
        / "models"
        / "work_definition.py"
    )

    if not path.exists():
        print("WorkDefinition file : NOT FOUND")
        return None

    print(
        "WorkDefinition file :",
        path.relative_to(REPO_ROOT),
    )

    text = safe_read(path)

    if not text:
        print("WorkDefinition readable : NO")
        return None

    print("WorkDefinition readable : YES")

    for line_no, line in enumerate(text.splitlines(), start=1):
        lower = line.lower()

        if (
            "amarakosha" in lower
            or "amarakosa" in lower
            or "identifier" in lower
            or "alias" in lower
        ):
            print(f"  {line_no}: {line.strip()}")

    return path


# ============================================================================
# CORPUS SOURCE IMPLEMENTATION
# ============================================================================

def inspect_corpus_source():
    section("3", "CANONICAL CORPUS SOURCE IMPLEMENTATION")

    path = (
        REPO_ROOT
        / "acquisition"
        / "models"
        / "corpus_source.py"
    )

    if not path.exists():
        print("CorpusSource implementation : NOT FOUND")
        return None

    print(
        "CorpusSource file :",
        path.relative_to(REPO_ROOT),
    )

    text = safe_read(path)

    print("Readable :", bool(text))

    required_fields = [
        "source_id",
        "name",
        "source_type",
        "source_format",
        "license",
        "version",
        "edition",
        "publisher",
        "author",
        "description",
        "language",
        "status",
        "download_urls",
        "checksum",
        "checksum_algorithm",
        "local_path",
        "cache_directory",
        "tags",
        "metadata",
    ]

    found = set()

    for line_no, line in enumerate(text.splitlines(), start=1):

        for field in required_fields:
            if field in line:
                found.add(field)

    print()
    print("CorpusSource field evidence:")

    for field in required_fields:
        status = "FOUND" if field in found else "NOT FOUND"
        print(f"  {field:24} : {status}")

    return path


# ============================================================================
# SOURCE TYPE / FORMAT
# ============================================================================

def inspect_source_enums():
    section("4", "CANONICAL SOURCE TYPE / FORMAT")

    source_type_path = (
        REPO_ROOT
        / "acquisition"
        / "models"
        / "source_type.py"
    )

    source_format_path = (
        REPO_ROOT
        / "acquisition"
        / "models"
        / "source_format.py"
    )

    for path in [source_type_path, source_format_path]:

        if not path.exists():
            print(
                path.relative_to(REPO_ROOT),
                ": NOT FOUND",
            )
            continue

        print()
        print(path.relative_to(REPO_ROOT))

        text = safe_read(path)

        for line_no, line in enumerate(text.splitlines(), start=1):

            if (
                "LEXICON" in line
                or "TEXT" in line
                or "TXT" in line
                or "TEI_XML" in line
                or "UNKNOWN" in line
            ):
                print(f"  {line_no}: {line.strip()}")


# ============================================================================
# EXISTING PARSER INPUT CONTRACT
# ============================================================================

def inspect_parser_contract():
    section("5", "EXISTING AMARAKOSHA PARSER INPUT CONTRACT")

    parser_paths = [
        AMARAKOSHA_ROOT / "parsers" / "amarakosha_parser.py",
        SERVICES_IMPORTER_ROOT / "amarakosha_parser.py",
        SERVICES_IMPORTER_ROOT / "amarakosha_importer.py",
        AMARAKOSHA_ROOT / "importers" / "amarakosha_importer.py",
    ]

    discovered = []

    for path in parser_paths:

        if not path.exists():
            continue

        print()
        print(
            "FILE :",
            path.relative_to(REPO_ROOT),
        )

        text = safe_read(path)

        for line_no, line in enumerate(text.splitlines(), start=1):

            lower = line.lower()

            if any(
                token in lower
                for token in [
                    "def parse_file",
                    "def import_file",
                    "file_path",
                    "read_text",
                    "utf-8",
                    "supported_extensions",
                    "parse_text",
                    "source: str",
                ]
            ):
                print(f"  {line_no}: {line.strip()}")
                discovered.append(
                    (path, line_no, line.strip())
                )

    print()
    print(
        "Parser/importer contract evidence :",
        len(discovered),
    )

    return discovered


# ============================================================================
# CONCRETE ARTIFACT SEARCH
# ============================================================================

def find_concrete_artifacts():
    section("6", "CONCRETE AMARAKOSHA SOURCE-ARTIFACT SEARCH")

    search_roots = [
        RESOURCE_ROOT,
        REPO_ROOT / "data",
        REPO_ROOT / "datasets",
        REPO_ROOT / "corpus",
        REPO_ROOT / "acquisition",
        AMARAKOSHA_ROOT,
    ]

    candidates = []

    artifact_extensions = {
        ".txt",
        ".xml",
        ".tei",
        ".json",
        ".yaml",
        ".yml",
        ".csv",
        ".tsv",
        ".pdf",
        ".epub",
        ".html",
        ".htm",
        ".md",
        ".zip",
        ".tar",
        ".gz",
        ".tgz",
        ".xlsx",
        ".sqlite",
        ".db",
    }

    for root in search_roots:

        if not root.exists():
            continue

        for path in root.rglob("*"):

            if not path.is_file():
                continue

            if is_excluded(path):
                continue

            name = path.name.lower()

            amarakosha_name = (
                "amarakosha" in name
                or "amarakosa" in name
            )

            if not amarakosha_name:
                continue

            if path.suffix.lower() in artifact_extensions:
                candidates.append(path)

    print("Concrete filename candidates :", len(candidates))

    for path in sorted(candidates):
        print("  ", path.relative_to(REPO_ROOT))

    if not candidates:
        print()
        print(
            "NO CONCRETE AMARAKOSHA SOURCE ARTIFACT FOUND."
        )

    return candidates


# ============================================================================
# SOURCE LOCATION EVIDENCE
# ============================================================================

def find_source_location_evidence():
    section("7", "AMARAKOSHA SOURCE LOCATION EVIDENCE")

    patterns = [
        "amarakosha.txt",
        "amarakosa.txt",
        "amarakosha.xml",
        "amarakosa.xml",
        "amarakosha.json",
        "amarakosa.json",
        "amarakosha.pdf",
        "amarakosa.pdf",
        "amarakosha.zip",
        "amarakosa.zip",
        "amarakosha_url",
        "amarakosa_url",
        "source_url",
        "download_url",
        "download_urls",
        "resource_url",
        "resource_urls",
    ]

    matches = []

    for path in iter_production_python_files():

        text = safe_read(path)

        for line_no, line in enumerate(
            text.splitlines(),
            start=1,
        ):

            lower = line.lower()

            if any(
                pattern.lower() in lower
                for pattern in patterns
            ):
                matches.append(
                    (
                        path,
                        line_no,
                        line.strip(),
                    )
                )

    print("Source-location evidence :", len(matches))

    for path, line_no, line in matches[:150]:
        print(
            f"  {path.relative_to(REPO_ROOT)}:"
            f"{line_no}: {line}"
        )

    if len(matches) > 150:
        print(
            f"  ... {len(matches) - 150} additional matches omitted"
        )

    return matches


# ============================================================================
# CORPUS SOURCE FACTORY
# ============================================================================

def inspect_corpus_source_factory():
    section("8", "CORPUS SOURCE FACTORY")

    path = (
        REPO_ROOT
        / "acquisition"
        / "factories"
        / "corpus_source_factory.py"
    )

    if not path.exists():
        print("CorpusSourceFactory : NOT FOUND")
        return None

    print(
        "CorpusSourceFactory :",
        path.relative_to(REPO_ROOT),
    )

    text = safe_read(path)

    interesting = [
        "def from_file",
        "def from_url",
        "def from_metadata",
        "CorpusSource(",
        "source_type",
        "source_format",
        "download_urls",
        "local_path",
    ]

    for line_no, line in enumerate(
        text.splitlines(),
        start=1,
    ):

        if any(token in line for token in interesting):
            print(f"  {line_no}: {line.strip()}")

    return path


# ============================================================================
# DECLARATION DECISION
# ============================================================================

def declaration_decision(
    artifacts,
    location_evidence,
    parser_evidence,
):
    section("9", "CORPUS SOURCE DECLARATION DECISION")

    print("Concrete artifacts :", len(artifacts))
    print("Location evidence :", len(location_evidence))
    print("Parser evidence   :", len(parser_evidence))

    print()

    if not artifacts:
        print("DECISION : BLOCKED — concrete artifact not established.")
        print()
        print(
            "No production CorpusSource declaration should be created yet."
        )
        return False

    if not location_evidence:
        print(
            "DECISION : BLOCKED — artifact exists but acquisition "
            "location is not established."
        )
        print()
        print(
            "Do not invent download_urls or repository metadata."
        )
        return False

    if not parser_evidence:
        print(
            "DECISION : BLOCKED — parser/importer input contract "
            "not sufficiently established."
        )
        return False

    print("DECISION : EVIDENCE SUFFICIENT FOR CORPUSSOURCE CONSTRUCTION.")
    print()
    print(
        "The next implementation may construct the canonical CorpusSource "
        "using only the verified artifact/location/format evidence."
    )

    return True


# ============================================================================
# MAIN
# ============================================================================

def main():

    print("=" * 100)
    print(
        "BATCH 5H-5E-13R-6 — "
        "CORPUSSOURCE DECLARATION AUDIT / GUARD"
    )
    print("=" * 100)

    bootstrap()

    audit_work_definition()

    inspect_corpus_source()

    inspect_source_enums()

    parser_evidence = inspect_parser_contract()

    artifacts = find_concrete_artifacts()

    location_evidence = find_source_location_evidence()

    inspect_corpus_source_factory()

    ready = declaration_decision(
        artifacts=artifacts,
        location_evidence=location_evidence,
        parser_evidence=parser_evidence,
    )

    print()
    print("=" * 100)

    if ready:
        print(
            "BATCH 5H-5E-13R-6 RESULT : "
            "EVIDENCE SUFFICIENT"
        )
    else:
        print(
            "BATCH 5H-5E-13R-6 RESULT : "
            "BLOCKED — NO UNSUPPORTED DECLARATION CREATED"
        )

    print("=" * 100)


if __name__ == "__main__":
    main()
