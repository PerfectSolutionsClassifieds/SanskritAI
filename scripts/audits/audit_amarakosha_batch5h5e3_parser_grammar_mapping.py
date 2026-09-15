
from __future__ import annotations

"""
SanskritAI
==========

Batch 5H-5E-3
Amarakośa Parser Grammar / Record Mapping Audit

Purpose
-------
Read-only architectural audit of the existing Amarakośa parser boundary.

This audit determines whether the repository contains sufficient concrete
evidence to implement:

    Amarakośa source
        ↓
    AmarakoshaParser
        ↓
    SynsetRecord / VargaRecord

The audit does NOT implement parser grammar.

It must not:
    - modify production parser code
    - create a new parser class
    - create a new source model
    - create new record classes
    - invent Amarakośa grammar
    - infer unsupported field mappings

Historical / duplicate implementation files are excluded from
production conclusions, including:

    * files whose stem ends in numeric suffixes
    * *_G<number>.py
    * tests
    * __pycache__

Version
-------
v0.1.0
"""

from pathlib import Path
import ast
import re
import sys
from collections import Counter


# ---------------------------------------------------------------------------
# Repository bootstrap
# ---------------------------------------------------------------------------

REPO_ROOT = Path("/content/SanskritAI")

if "/content" not in sys.path:
    sys.path.insert(0, "/content")


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

from SanskritAI.amarakosha.parsers.amarakosha_parser import (
    AmarakoshaParser,
)
from SanskritAI.amarakosha.records.synset_record import (
    SynsetRecord,
)
from SanskritAI.amarakosha.records.varga_record import (
    VargaRecord,
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEARCH_ROOTS = (
    REPO_ROOT / "amarakosha",
    REPO_ROOT / "acquisition",
    REPO_ROOT / "corpus",
    REPO_ROOT / "docs",
    REPO_ROOT / "data",
    REPO_ROOT / "resources",
)

TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".rst",
    ".xml",
    ".tei",
    ".html",
    ".htm",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
}

PYTHON_EXTENSIONS = {".py"}

SOURCE_TERMS = (
    "amarakosha",
    "amarakośa",
    "amara kosha",
    "amara-kośa",
    "amara",
)

GRAMMAR_TERMS = (
    "kanda",
    "kāṇḍa",
    "varga",
    "varga_number",
    "verse",
    "verse_number",
    "śloka",
    "sloka",
    "pada",
    "pada_number",
    "synset",
    "lexeme",
)

RECORD_TERMS = (
    "SynsetRecord",
    "VargaRecord",
    "lexeme_ids",
    "devanagari",
    "iast",
    "transliteration",
    "gloss",
    "description",
    "sequence",
    "tags",
    "notes",
)

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


# ---------------------------------------------------------------------------
# File filters
# ---------------------------------------------------------------------------

def is_historical_or_duplicate(path: Path) -> bool:
    """
    Return True when a Python file is a known historical / duplicate variant.
    """

    stem = path.stem

    if re.search(r"_G\d+$", stem, flags=re.IGNORECASE):
        return True

    if re.search(r"\d+$", stem):
        return True

    return False


def is_excluded(path: Path) -> bool:
    """
    Exclude tests, caches, audit artifacts, and historical variants.
    """

    if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
        return True

    if path.suffix.lower() == ".py" and is_historical_or_duplicate(path):
        return True

    return False


def iter_files() -> list[Path]:
    """
    Return active repository files from the audit roots.
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
    """
    Read text conservatively.
    """

    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    except Exception:
        return ""


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def preview(text: str, limit: int = 900) -> str:
    """
    Compact whitespace-normalized preview.
    """

    compact = " ".join(text.split())
    return compact[:limit]


# ---------------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------------

def executable_names(path: Path) -> list[str]:
    """
    Return executable references to relevant parser/record symbols.

    Docstrings and comments are deliberately ignored.
    """

    if path.suffix != ".py":
        return []

    text = safe_read(path)

    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        return []

    names: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id in {
                "SynsetRecord",
                "VargaRecord",
                "AmarakoshaParser",
            }:
                names.append(node.id)

        elif isinstance(node, ast.Attribute):
            if node.attr in {
                "SynsetRecord",
                "VargaRecord",
                "AmarakoshaParser",
            }:
                names.append(node.attr)

    return names


def constructor_calls(path: Path) -> list[str]:
    """
    Detect actual constructor calls for parser record classes.
    """

    if path.suffix != ".py":
        return []

    text = safe_read(path)

    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        return []

    calls: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        target = None

        if isinstance(node.func, ast.Name):
            target = node.func.id

        elif isinstance(node.func, ast.Attribute):
            target = node.func.attr

        if target in {"SynsetRecord", "VargaRecord"}:
            calls.append(target)

    return calls


# ---------------------------------------------------------------------------
# Field extraction
# ---------------------------------------------------------------------------

def dataclass_fields(cls: type) -> tuple[str, ...]:
    """
    Return dataclass field names without assuming implementation details.
    """

    try:
        return tuple(cls.__dataclass_fields__.keys())
    except AttributeError:
        return ()


# ---------------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 115)
    print("BATCH 5H-5E-3 — AMARAKOSHA PARSER GRAMMAR / RECORD MAPPING AUDIT")
    print("=" * 115)

    files = iter_files()

    # -----------------------------------------------------------------------
    # 1. Baseline
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("1. COMPONENT BASELINE")
    print("-" * 115)

    print("AmarakoshaParser :", AmarakoshaParser, "PASS")
    print("SynsetRecord     :", SynsetRecord, "PASS")
    print("VargaRecord      :", VargaRecord, "PASS")

    print(
        "Parser signature :",
        __import__("inspect").signature(
            AmarakoshaParser.parse
        ),
    )

    # -----------------------------------------------------------------------
    # 2. Record contracts
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("2. RECORD FIELD CONTRACTS")
    print("-" * 115)

    synset_fields = dataclass_fields(SynsetRecord)
    varga_fields = dataclass_fields(VargaRecord)

    print("SynsetRecord fields:")
    for field_name in synset_fields:
        print(f"  {field_name}")

    print("\nVargaRecord fields:")
    for field_name in varga_fields:
        print(f"  {field_name}")

    # -----------------------------------------------------------------------
    # 3. Active production files
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("3. ACTIVE PRODUCTION FILE INVENTORY")
    print("-" * 115)

    amarakosha_files = [
        path
        for path in files
        if "amarakosha" in path.name.lower()
        or "amarakośa" in path.name.lower()
    ]

    print("Active Amarakośa-related files:", len(amarakosha_files))

    for path in amarakosha_files:
        print(" ", path.relative_to(REPO_ROOT))

    # -----------------------------------------------------------------------
    # 4. Source-format evidence
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("4. SOURCE-FORMAT EVIDENCE")
    print("-" * 115)

    evidence_files: list[Path] = []

    for path in files:
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        text = safe_read(path)

        if not text:
            continue

        if not contains_any(text, SOURCE_TERMS):
            continue

        if not contains_any(text, GRAMMAR_TERMS):
            continue

        evidence_files.append(path)

    print(
        "Active text files containing both Amarakośa/source terms "
        "and grammar/structure terms:",
        len(evidence_files),
    )

    if not evidence_files:
        print("NO CONCRETE SOURCE-FORMAT EVIDENCE FOUND.")

    else:
        for path in evidence_files:
            text = safe_read(path)

            print("\nFILE:", path.relative_to(REPO_ROOT))

            matched_source = [
                term
                for term in SOURCE_TERMS
                if term.lower() in text.lower()
            ]

            matched_grammar = [
                term
                for term in GRAMMAR_TERMS
                if term.lower() in text.lower()
            ]

            print("Source terms :", matched_source)
            print("Grammar terms:", matched_grammar)
            print("Preview      :", preview(text))

    # -----------------------------------------------------------------------
    # 5. Parser executable references
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("5. PARSER → RECORD EXECUTABLE REFERENCES")
    print("-" * 115)

    parser_root = REPO_ROOT / "amarakosha" / "parsers"

    parser_files = []

    if parser_root.exists():
        parser_files = [
            path
            for path in parser_root.rglob("*.py")
            if not is_excluded(path)
        ]

    for path in sorted(parser_files):
        names = executable_names(path)
        calls = constructor_calls(path)

        print("\nFILE:", path.relative_to(REPO_ROOT))

        if names:
            print("Executable references:", names)
        else:
            print("Executable references: NONE")

        if calls:
            print("Record constructors   :", calls)
        else:
            print("Record constructors   : NONE")

    # -----------------------------------------------------------------------
    # 6. Record constructor evidence across repository
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("6. RECORD CONSTRUCTOR EVIDENCE ACROSS ACTIVE PRODUCTION CODE")
    print("-" * 115)

    constructor_evidence: Counter[str] = Counter()

    constructor_locations: dict[str, list[Path]] = {
        "SynsetRecord": [],
        "VargaRecord": [],
    }

    for path in files:
        if path.suffix != ".py":
            continue

        calls = constructor_calls(path)

        for call in calls:
            constructor_evidence[call] += 1
            constructor_locations[call].append(path)

    print("Constructor counts:", dict(constructor_evidence))

    for record_name, locations in constructor_locations.items():
        print(f"\n{record_name} constructor locations:")

        if not locations:
            print("  NONE")

        else:
            for path in sorted(set(locations)):
                print(" ", path.relative_to(REPO_ROOT))

    # -----------------------------------------------------------------------
    # 7. Field mapping evidence
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("7. FIELD-MAPPING EVIDENCE")
    print("-" * 115)

    field_groups = {
        "Structural identity": (
            "identifier",
            "source",
            "source_identifier",
            "source_version",
        ),
        "Amarakośa location": (
            "kanda",
            "varga",
            "varga_number",
            "verse",
            "sequence",
        ),
        "Textual representation": (
            "devanagari",
            "iast",
            "transliteration",
        ),
        "Semantic representation": (
            "gloss",
            "description",
        ),
        "Lexical linkage": (
            "lexeme_ids",
        ),
        "Metadata": (
            "tags",
            "notes",
        ),
    }

    all_text = "\n".join(
        safe_read(path)
        for path in files
        if path.suffix.lower() in TEXT_EXTENSIONS
    ).lower()

    for group_name, fields in field_groups.items():
        print(f"\n{group_name}:")

        for field_name in fields:
            present = field_name.lower() in all_text

            print(
                f"  {field_name:<20}",
                "EVIDENCE PRESENT" if present else "NO EVIDENCE",
            )

    # -----------------------------------------------------------------------
    # 8. Actual parser implementation status
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("8. CURRENT PARSER IMPLEMENTATION")
    print("-" * 115)

    parser_source_path = (
        REPO_ROOT
        / "amarakosha"
        / "parsers"
        / "amarakosha_parser.py"
    )

    parser_source = safe_read(parser_source_path)

    print(
        "Parser file:",
        parser_source_path.relative_to(REPO_ROOT),
    )

    if parser_source:
        print("Parser preview:")
        print(preview(parser_source, limit=1800))
    else:
        print("Parser source could not be read.")

    try:
        parser = AmarakoshaParser()
        parser.parse("")
        print("parse('') unexpectedly returned without error.")

    except NotImplementedError as exc:
        print("Current parse() status: NOT IMPLEMENTED")
        print("NotImplementedError:", exc)

    except Exception as exc:
        print(
            "Current parse() raised:",
            type(exc).__name__,
            str(exc),
        )

    # -----------------------------------------------------------------------
    # 9. Grammar evidence classification
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("9. GRAMMAR EVIDENCE CLASSIFICATION")
    print("-" * 115)

    print(
        "Concrete external/source-text grammar evidence :",
        "FOUND" if evidence_files else "NOT FOUND",
    )

    print(
        "Actual SynsetRecord constructor usage           :",
        "FOUND"
        if constructor_evidence.get("SynsetRecord")
        else "NOT FOUND",
    )

    print(
        "Actual VargaRecord constructor usage            :",
        "FOUND"
        if constructor_evidence.get("VargaRecord")
        else "NOT FOUND",
    )

    # -----------------------------------------------------------------------
    # 10. Mapping questions
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("10. PARSER → RECORD MAPPING QUESTIONS")
    print("-" * 115)

    questions = (
        "How is a Kanda represented in the source?",
        "How is a Varga represented in the source?",
        "How is a Varga number represented?",
        "How is a verse represented?",
        "How is sequence/pada ordering represented?",
        "How are Devanagari and IAST forms represented?",
        "How is gloss/semantic content represented?",
        "How are lexical identities represented?",
        "How are Varga boundaries detected?",
        "How are Synset boundaries detected?",
        "Can one source unit contain multiple Synsets?",
        "Can one Synset span multiple source lines?",
        "What source information must be retained as provenance?",
    )

    for question in questions:
        print("INSPECT:", question)

    # -----------------------------------------------------------------------
    # 11. Architectural decision gate
    # -----------------------------------------------------------------------

    print("\n" + "-" * 115)
    print("11. 5H-5E-3 DECISION GATE")
    print("-" * 115)

    print("Existing Parser        : PRESERVE")
    print("Existing Record Types  : PRESERVE")
    print("New Parser Class       : NOT JUSTIFIED")
    print("New Record Class       : NOT JUSTIFIED")

    if evidence_files:
        print(
            "Source Grammar         : "
            "EVIDENCE EXISTS — inspect concrete format before implementation"
        )
    else:
        print(
            "Source Grammar         : "
            "NOT ESTABLISHED — do not invent grammar"
        )

    if constructor_evidence:
        print(
            "Record Construction    : "
            "EXISTING IMPLEMENTATION EVIDENCE FOUND"
        )
    else:
        print(
            "Record Construction    : "
            "NO EXISTING PRODUCTION CONSTRUCTION EVIDENCE"
        )

    print(
        "Next implementation     : "
        "ONLY AFTER SOURCE FORMAT + GRAMMAR MAPPING IS EXPLICIT"
    )

    print("\n" + "=" * 115)
    print("BATCH 5H-5E-3 — AUDIT COMPLETE")
    print("=" * 115)


if __name__ == "__main__":
    main()
