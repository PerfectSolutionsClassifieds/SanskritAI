
from __future__ import annotations

"""
BATCH 5H-5E-13R-5
Concrete Amarakośa Source-Artifact Audit

Purpose
-------
Read-only audit to identify the concrete Amarakośa source artifact and determine
whether the existing SanskritAI repository already contains enough concrete
source/acquisition evidence to proceed toward:

    WorkRegistry
        ↓
    Amarakośa WorkDefinition
        ↓
    Concrete source artifact
        ↓
    CorpusSource
        ↓
    AcquisitionManifest
        ↓
    SourceAcquirer
        ↓
    AcquisitionResult
        ↓
    Existing Amarakośa parser/importer
        ↓
    Canonical lexical bridge

This audit MUST NOT modify production code.

Production-scope exclusions
---------------------------
Ignore:
    - tests/
    - __pycache__/
    - audit scripts themselves
    - historical / duplicate Python files ending in numeric suffixes
      such as foo1.py, foo2.py, etc.
    - files matching *_G<number>.py

Important
---------
This is an artifact-identification audit.

It does NOT create:
    - AmarakośaProvider
    - AmarakośaAcquirer
    - AmarakośaDownloader
    - AmarakośaSource
    - AmarakośaManifest
    - new acquisition abstractions

Those decisions must wait until the concrete source artifact is established.
"""

from pathlib import Path
import ast
import importlib
import os
import re
import sys
import traceback


# ============================================================================
# PATHS
# ============================================================================

REPO_ROOT = Path("/content/SanskritAI")
PROJECT_PARENT = REPO_ROOT.parent

SCRIPTS_DIR = REPO_ROOT / "scripts"
AUDITS_DIR = SCRIPTS_DIR / "audits"

# Production areas relevant to this audit.
PRODUCTION_ROOTS = [
    REPO_ROOT / "amarakosha",
    REPO_ROOT / "acquisition",
    REPO_ROOT / "resources",
    REPO_ROOT / "models",
    REPO_ROOT / "plugins",
    REPO_ROOT / "services",
]


# ============================================================================
# PRODUCTION FILE FILTER
# ============================================================================

HISTORICAL_SUFFIX_RE = re.compile(r".*\d+\.py$", re.IGNORECASE)
GENERATION_SUFFIX_RE = re.compile(r"_G\d+\.py$", re.IGNORECASE)


def is_excluded_path(path: Path) -> bool:
    """
    Return True when a path is outside the intended production audit scope.
    """

    parts_lower = {part.lower() for part in path.parts}

    if "tests" in parts_lower:
        return True

    if "__pycache__" in parts_lower:
        return True

    if path.suffix.lower() == ".py":
        name = path.name

        if HISTORICAL_SUFFIX_RE.match(name):
            return True

        if GENERATION_SUFFIX_RE.match(name):
            return True

    # Never inspect this audit script itself.
    try:
        if path.resolve() == Path(__file__).resolve():
            return True
    except Exception:
        pass

    return False


def iter_production_files():
    """
    Yield production files from the audit roots.
    """

    seen = set()

    for root in PRODUCTION_ROOTS:
        if not root.exists():
            continue

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if is_excluded_path(path):
                continue

            try:
                resolved = path.resolve()
            except Exception:
                resolved = path

            if resolved in seen:
                continue

            seen.add(resolved)
            yield path


def iter_production_python_files():
    for path in iter_production_files():
        if path.suffix.lower() == ".py":
            yield path


# ============================================================================
# SAFE FILE READING
# ============================================================================

def safe_read_text(path: Path) -> str:
    """
    Read text files safely.

    Binary artifacts such as PDF/ZIP/TAR are intentionally not decoded here.
    This audit identifies concrete artifacts and textual declarations; it does
    not perform binary-content extraction.
    """

    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


# ============================================================================
# PACKAGE BOOTSTRAP
# ============================================================================

def bootstrap_package():
    """
    Make /content available so that:

        import SanskritAI

    resolves:

        /content/SanskritAI

    This is the correct package-parent relationship for the Colab layout.
    """

    print("=" * 100)
    print("1. PACKAGE BOOTSTRAP")
    print("=" * 100)

    print(f"Repository root : {REPO_ROOT}")
    print(f"Repository exists : {REPO_ROOT.exists()}")
    print(f"Repository parent : {PROJECT_PARENT}")
    print(f"Parent exists : {PROJECT_PARENT.exists()}")

    if not REPO_ROOT.exists():
        print("SanskritAI repository : FAIL")
        print(f"Missing repository root: {REPO_ROOT}")
        raise RuntimeError("SanskritAI repository root does not exist.")

    # The Python import path must contain the PARENT of the package.
    parent_str = str(PROJECT_PARENT)

    if parent_str not in sys.path:
        sys.path.insert(0, parent_str)
        print(f"Added to sys.path : {parent_str}")
    else:
        print(f"Already in sys.path : {parent_str}")

    print("sys.path[0] :", sys.path[0])

    try:
        importlib.invalidate_caches()

        import SanskritAI  # noqa: F401

        print("SanskritAI import : PASS")
        print("SanskritAI.__file__ :", getattr(SanskritAI, "__file__", None))

    except Exception as exc:
        print("SanskritAI import : FAIL")
        print("error :", repr(exc))
        traceback.print_exc()
        raise


# ============================================================================
# SECTION HELPERS
# ============================================================================

def section(number: str, title: str):
    print()
    print("=" * 100)
    print(f"{number}. {title}")
    print("=" * 100)


def print_matches(label: str, matches, max_items: int = 100):
    print(f"{label} : {len(matches)}")

    for path, line_no, line in matches[:max_items]:
        print(f"  {path}:{line_no}: {line.strip()}")

    if len(matches) > max_items:
        print(f"  ... {len(matches) - max_items} additional matches omitted")


# ============================================================================
# WORKREGISTRY
# ============================================================================

def audit_workregistry():
    section("2", "AMARAKOSHA WORKREGISTRY IDENTITY")

    try:
        module = importlib.import_module(
            "SanskritAI.acquisition.registries.work_registry"
        )

        print("WorkRegistry module : PASS")
        print("module :", module)

    except Exception as exc:
        print("WorkRegistry module : FAIL")
        print("error :", repr(exc))
        return

    registry_cls = getattr(module, "WorkRegistry", None)

    if registry_cls is None:
        print("WorkRegistry class : NOT FOUND")
        return

    print("WorkRegistry class : PASS")

    registry = None

    try:
        registry = registry_cls()
        print("WorkRegistry construction : PASS")
    except Exception as exc:
        print("WorkRegistry construction : FAIL")
        print("error :", repr(exc))
        return

    identifiers = [
        "amarakosha",
        "amara_kosha",
        "amara-kosha",
        "amarakosa",
    ]

    for identifier in identifiers:
        try:
            result = registry.get(identifier)

            print()
            print(f"lookup({identifier!r}) :")
            print("  result :", result)

        except Exception as exc:
            print(f"lookup({identifier!r}) : ERROR")
            print("  error :", repr(exc))


# ============================================================================
# AMARAKOSHA PRODUCTION FILES
# ============================================================================

def audit_amarakosha_files():
    section("3", "AMARAKOSHA PRODUCTION FILE INVENTORY")

    matches = []

    for path in iter_production_files():
        try:
            relative = path.relative_to(REPO_ROOT)
        except ValueError:
            relative = path

        text_name = str(relative).lower()

        if "amarakosha" in text_name or "amarakosa" in text_name:
            matches.append(path)

    print("Amarakośa production files :", len(matches))

    for path in sorted(matches):
        try:
            print("  ", path.relative_to(REPO_ROOT))
        except ValueError:
            print("  ", path)


# ============================================================================
# CONCRETE ARTIFACT CANDIDATES
# ============================================================================

def audit_filename_candidates():
    section("4", "CONCRETE SOURCE-ARTIFACT FILENAME CANDIDATES")

    candidates = []

    artifact_extensions = {
        ".txt",
        ".xml",
        ".tei",
        ".tei.xml",
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
        ".markdown",
        ".zip",
        ".tar",
        ".gz",
        ".tgz",
        ".7z",
        ".rar",
        ".xlsx",
        ".sql",
        ".sqlite",
        ".db",
    }

    for path in iter_production_files():
        name_lower = path.name.lower()

        is_amarakosha_name = (
            "amarakosha" in name_lower
            or "amarakosa" in name_lower
            or ("amara" in name_lower and "kosa" in name_lower)
        )

        if not is_amarakosha_name:
            continue

        if path.suffix.lower() in artifact_extensions:
            candidates.append(path)
            continue

        # Also retain files whose complete name strongly resembles an
        # Amarakośa source artifact even when the suffix is unusual.
        candidates.append(path)

    print("Candidate files :", len(candidates))

    for path in sorted(candidates):
        try:
            relative = path.relative_to(REPO_ROOT)
        except ValueError:
            relative = path

        print("  ", relative)


# ============================================================================
# NON-PYTHON TEXTUAL ARTIFACT SEARCH
# ============================================================================

def audit_non_python_artifacts():
    section("5", "NON-PYTHON ARTIFACT CONTENT SEARCH")

    patterns = [
        "amarakosha",
        "amarakosa",
        "अमरकोश",
        "amara kosha",
        "amara-kośa",
        "amara kosa",
    ]

    all_matches = []

    for path in iter_production_files():

        if path.suffix.lower() == ".py":
            continue

        # Skip obvious binary formats for this textual scan.
        if path.suffix.lower() in {
            ".pdf",
            ".zip",
            ".tar",
            ".gz",
            ".tgz",
            ".7z",
            ".rar",
            ".epub",
            ".xlsx",
            ".sqlite",
            ".db",
        }:
            continue

        text = safe_read_text(path)

        if not text:
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            lower_line = line.lower()

            for pattern in patterns:
                if pattern.lower() in lower_line:
                    all_matches.append((path, line_no, line))
                    break

    print_matches(
        "Amarakośa textual artifact/content matches",
        sorted(
            all_matches,
            key=lambda item: (
                str(item[0]),
                item[1],
            ),
        ),
    )


# ============================================================================
# ACQUISITION DECLARATIONS
# ============================================================================

def audit_acquisition_declarations():
    section("6", "EXISTING AMARAKOSHA ACQUISITION DECLARATIONS")

    patterns = [
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

    all_matches = []

    for path in iter_production_python_files():

        text = safe_read_text(path)

        if not text:
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):

            for pattern in patterns:
                if pattern in line:
                    all_matches.append((path, line_no, line))
                    break

    print_matches(
        "Acquisition declaration matches",
        sorted(
            all_matches,
            key=lambda item: (
                str(item[0]),
                item[1],
            ),
        ),
    )


# ============================================================================
# URL / RESOURCE DECLARATIONS
# ============================================================================

def audit_url_resource_declarations():
    section("7", "AMARAKOSHA URL / RESOURCE DECLARATIONS")

    patterns = [
        "amarakosha",
        "amarakosa",
        "http://",
        "https://",
        "download_url",
        "download_urls",
        "source_url",
        "source_urls",
        "resource_url",
        "resource_urls",
        "local_path",
        "cache_directory",
    ]

    all_matches = []

    for path in iter_production_python_files():

        text = safe_read_text(path)

        if not text:
            continue

        # Only report lines which are plausibly Amarakośa-related.
        for line_no, line in enumerate(text.splitlines(), start=1):

            lower_line = line.lower()

            if "amarakosha" not in lower_line and "amarakosa" not in lower_line:
                continue

            if any(pattern.lower() in lower_line for pattern in patterns):
                all_matches.append((path, line_no, line))

    print_matches(
        "Amarakośa URL/resource declarations",
        sorted(
            all_matches,
            key=lambda item: (
                str(item[0]),
                item[1],
            ),
        ),
    )


# ============================================================================
# PARSER / IMPORTER BOUNDARY
# ============================================================================

def audit_parser_importer_boundary():
    section("8", "EXISTING AMARAKOSHA PARSER / IMPORTER BOUNDARY")

    candidates = [
        REPO_ROOT / "amarakosha" / "parsers" / "amarakosha_parser.py",
        REPO_ROOT / "amarakosha" / "importers" / "amarakosha_importer.py",
        REPO_ROOT / "services" / "importers" / "amarakosha_parser.py",
        REPO_ROOT / "services" / "importers" / "amarakosha_importer.py",
    ]

    for path in candidates:

        if not path.exists():
            print(f"{path.relative_to(REPO_ROOT)} : NOT FOUND")
            continue

        print(f"{path.relative_to(REPO_ROOT)} : EXISTS")

        text = safe_read_text(path)

        if not text:
            print("  readable text : NO")
            continue

        print("  readable text : YES")
        print("  lines :", len(text.splitlines()))

        clues = [
            "parse",
            "import",
            "source",
            "resource",
            "file",
            "path",
            "text",
            "record",
        ]

        found = []

        for line_no, line in enumerate(text.splitlines(), start=1):
            lower_line = line.lower()

            if any(clue in lower_line for clue in clues):
                found.append((path, line_no, line))

        for _, line_no, line in found[:40]:
            print(f"    {line_no}: {line.strip()}")

        if len(found) > 40:
            print(f"    ... {len(found) - 40} additional lines omitted")


# ============================================================================
# PARSER RESOURCE CLUES
# ============================================================================

def audit_parser_resource_clues():
    section("9", "AMARAKOSHA PARSER RESOURCE / INPUT CLUES")

    parser_paths = [
        REPO_ROOT / "amarakosha" / "parsers",
        REPO_ROOT / "amarakosha" / "importers",
        REPO_ROOT / "services" / "importers",
    ]

    patterns = [
        "Path(",
        "open(",
        "read_text",
        "read_bytes",
        "parse(",
        "source",
        "resource",
        "file_path",
        "local_path",
        "input_path",
        "filename",
        "url",
        "download",
    ]

    all_matches = []

    for root in parser_paths:

        if not root.exists():
            continue

        for path in root.rglob("*.py"):

            if is_excluded_path(path):
                continue

            text = safe_read_text(path)

            for line_no, line in enumerate(text.splitlines(), start=1):

                if any(pattern.lower() in line.lower() for pattern in patterns):
                    all_matches.append((path, line_no, line))

    print_matches(
        "Parser/importer resource clues",
        sorted(
            all_matches,
            key=lambda item: (
                str(item[0]),
                item[1],
            ),
        ),
        max_items=150,
    )


# ============================================================================
# NEW AMARAKOSHA-SPECIFIC ACQUISITION ABSTRACTIONS
# ============================================================================

def audit_specific_acquisition_abstractions():
    section("10", "AMARAKOSHA-SPECIFIC ACQUISITION ABSTRACTIONS")

    patterns = [
        "class AmarakoshaProvider",
        "class AmarakoshaAcquirer",
        "class AmarakoshaDownloader",
        "class AmarakoshaSource",
        "class AmarakoshaManifest",
        "amarakosha_provider",
        "amarakosha_acquirer",
        "amarakosha_downloader",
        "amarakosha_source",
        "amarakosha_manifest",
    ]

    matches = []

    for path in iter_production_python_files():

        text = safe_read_text(path)

        for line_no, line in enumerate(text.splitlines(), start=1):

            if any(pattern in line for pattern in patterns):
                matches.append((path, line_no, line))

    print_matches(
        "Amarakośa-specific acquisition abstraction matches",
        sorted(
            matches,
            key=lambda item: (
                str(item[0]),
                item[1],
            ),
        ),
    )

    if not matches:
        print()
        print("No Amarakośa-specific acquisition abstraction detected.")
        print("This is expected at this audit stage.")


# ============================================================================
# AST SOURCE ARTIFACT CLUES
# ============================================================================

def audit_ast_artifact_clues():
    section("11", "PYTHON AST SOURCE-ARTIFACT CLUES")

    interesting_nodes = []

    for path in iter_production_python_files():

        text = safe_read_text(path)

        if not text:
            continue

        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError:
            continue
        except Exception:
            continue

        for node in ast.walk(tree):

            if isinstance(node, ast.Constant):
                if isinstance(node.value, str):

                    value = node.value

                    lower_value = value.lower()

                    if (
                        "amarakosha" in lower_value
                        or "amarakosa" in lower_value
                        or "http://" in lower_value
                        or "https://" in lower_value
                    ):
                        interesting_nodes.append(
                            (
                                path,
                                getattr(node, "lineno", 0),
                                value,
                            )
                        )

    print("AST string artifact clues :", len(interesting_nodes))

    for path, line_no, value in interesting_nodes[:150]:
        print(
            f"  {path.relative_to(REPO_ROOT)}:{line_no}: "
            f"{value!r}"
        )

    if len(interesting_nodes) > 150:
        print(
            f"  ... {len(interesting_nodes) - 150} "
            "additional AST clues omitted"
        )


# ============================================================================
# CONCLUSION
# ============================================================================

def conclusion():
    section("12", "READ-ONLY AUDIT CONCLUSION")

    print(
        """
The purpose of 13R-5 is to establish concrete source-artifact evidence before
introducing any Amarakośa-specific acquisition abstraction.

Interpret the evidence using the following decision sequence:

    A. Concrete source artifact identified
           ↓
    B. Artifact representation / format identified
           ↓
    C. Artifact acquisition location identified
           ↓
    D. Existing parser/importer input contract identified
           ↓
    E. Generic CorpusSource / AcquisitionManifest can be populated
           ↓
    F. Only then determine whether an Amarakośa-specific adapter/manifest/
       provider/acquirer is actually required.

DO NOT create new Amarakośa acquisition classes merely because none exist.

A missing Amarakośa-specific provider is not itself a defect.

The key question is:

    "What exact source artifact does the existing Amarakośa parser/importer
     expect, and where does that artifact come from?"

Binary artifacts such as PDF/ZIP/TAR are intentionally not decoded by this
initial textual audit. If the audit identifies a binary artifact candidate,
the next step should inspect that concrete artifact itself rather than infer
its contents from its filename.
"""
    )


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 100)
    print("BATCH 5H-5E-13R-5 — CONCRETE AMARAKOSHA SOURCE-ARTIFACT AUDIT")
    print("=" * 100)

    # MUST happen before importing SanskritAI.
    bootstrap_package()

    audit_workregistry()
    audit_amarakosha_files()
    audit_filename_candidates()
    audit_non_python_artifacts()
    audit_acquisition_declarations()
    audit_url_resource_declarations()
    audit_parser_importer_boundary()
    audit_parser_resource_clues()
    audit_specific_acquisition_abstractions()
    audit_ast_artifact_clues()
    conclusion()

    print()
    print("=" * 100)
    print("BATCH 5H-5E-13R-5 COMPLETE")
    print("=" * 100)


if __name__ == "__main__":
    main()
