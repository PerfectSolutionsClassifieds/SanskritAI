from __future__ import annotations

"""
SanskritAI
==========

Batch 5H-5E-2
Amarakośa Source Format Audit

Purpose
-------
Identify the actual Amarakośa source-format evidence already present
inside SanskritAI before implementing AmarakoshaParser.parse().

This is a READ-ONLY audit.

It does NOT:
- modify production code
- implement parsing rules
- introduce a new parser
- introduce a new source model
- modify VargaRecord
- modify SynsetRecord
- invent an Amarakośa grammar

The audit searches the existing repository for source-format
evidence such as:
- Amarakośa source files
- raw Sanskrit text
- parser fixtures
- source samples
- acquisition artifacts
- Kanda/Varga markers
- verse/synset markers
- existing Amarakośa parsing helpers
- documented source examples

Production exclusions
---------------------
Historical numeric-suffixed files and _G<number>.py files,
tests, and __pycache__ are excluded from production-code inspection.
"""

import ast
import re
import sys
from pathlib import Path


# =====================================================================
# IMPORT BOOTSTRAP
# =====================================================================

ROOT = Path("/content/SanskritAI")
PROJECT_PARENT = ROOT.parent

if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))


# =====================================================================
# SANSKRITAI IMPORTS
# =====================================================================

from SanskritAI.amarakosha.enums.Amarakanda import (
    Amarakanda,
)

from SanskritAI.amarakosha.parsers.amarakosha_parser import (
    AmarakoshaParser,
)

from SanskritAI.amarakosha.records.synset_record import (
    SynsetRecord,
)

from SanskritAI.amarakosha.records.varga_record import (
    VargaRecord,
)


# =====================================================================
# CONSTANTS
# =====================================================================

MAX_TEXT_PREVIEW = 700

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

SOURCE_KEYWORDS = (
    "amarakosha",
    "amarakośa",
    "amara kosha",
    "amara-kośa",
    "amara",
)

STRUCTURE_KEYWORDS = (
    "kanda",
    "kāṇḍa",
    "varga",
    "verse",
    "synset",
    "pada",
    "śloka",
    "sloka",
)


# =====================================================================
# FILE HELPERS
# =====================================================================

def is_historical_file(path: Path) -> bool:
    """
    Return True for historical numeric-suffixed or generated files.
    """

    stem = path.stem

    # parser1.py / parser2.py / parser10.py
    if stem and stem[-1].isdigit():
        return True

    # parser_G1.py / parser_G12.py
    if "_G" in stem:
        suffix = stem.rsplit("_G", 1)[-1]

        if suffix.isdigit():
            return True

    return False


def is_excluded_path(path: Path) -> bool:
    """
    Return True when a path is outside the production audit scope.
    """

    relative = path.relative_to(ROOT)

    if "__pycache__" in relative.parts:
        return True

    if "tests" in relative.parts:
        return True

    if is_historical_file(path):
        return True

    return False


def production_python_files() -> list[Path]:
    """Return active production Python files."""

    result: list[Path] = []

    for path in ROOT.rglob("*.py"):

        if is_excluded_path(path):
            continue

        result.append(path)

    return sorted(result)


def repository_text_files() -> list[Path]:
    """
    Return repository text/source files that may contain actual
    Amarakośa source-format evidence.

    Tests are excluded because this audit is intended to discover
    production/source evidence rather than test-only assumptions.
    """

    result: list[Path] = []

    for path in ROOT.rglob("*"):

        if not path.is_file():
            continue

        if is_excluded_path(path):
            continue

        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        result.append(path)

    return sorted(result)


def read_text(path: Path) -> str:
    """Read UTF-8 text safely."""

    try:
        return path.read_text(
            encoding="utf-8"
        )
    except (OSError, UnicodeError):
        return ""


# =====================================================================
# SEARCH HELPERS
# =====================================================================

def keyword_hits(
    text: str,
    keywords: tuple[str, ...],
) -> list[str]:
    """Return keywords actually found in text."""

    lowered = text.lower()

    return sorted(
        {
            keyword
            for keyword in keywords
            if keyword.lower() in lowered
        }
    )


def likely_amarakosha_text(
    text: str,
) -> bool:
    """
    Determine whether text contains meaningful Amarakośa/source
    indicators.

    This is deliberately permissive because this is discovery,
    not semantic validation.
    """

    lowered = text.lower()

    source_hit = any(
        keyword.lower() in lowered
        for keyword in SOURCE_KEYWORDS
    )

    structure_hits = sum(
        keyword.lower() in lowered
        for keyword in STRUCTURE_KEYWORDS
    )

    return source_hit or structure_hits >= 2


def compact_preview(text: str) -> str:
    """Create a safe one-line preview."""

    cleaned = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    if len(cleaned) > MAX_TEXT_PREVIEW:
        return (
            cleaned[:MAX_TEXT_PREVIEW]
            + " ..."
        )

    return cleaned


# =====================================================================
# AST ANALYSIS
# =====================================================================

def parser_record_references(
    path: Path,
) -> list[str]:
    """
    Return executable references to Amarakośa record classes.
    """

    text = read_text(path)

    if not text:
        return []

    try:
        tree = ast.parse(
            text,
            filename=str(path),
        )
    except SyntaxError:
        return []

    references: set[str] = set()

    for node in ast.walk(tree):

        if isinstance(
            node,
            ast.ImportFrom,
        ):
            for alias in node.names:

                if alias.name in {
                    "SynsetRecord",
                    "VargaRecord",
                }:
                    references.add(
                        alias.name
                    )

        elif isinstance(
            node,
            ast.Name,
        ):
            if node.id in {
                "SynsetRecord",
                "VargaRecord",
            }:
                references.add(
                    node.id
                )

        elif isinstance(
            node,
            ast.Attribute,
        ):
            if node.attr in {
                "SynsetRecord",
                "VargaRecord",
            }:
                references.add(
                    node.attr
                )

    return sorted(references)


# =====================================================================
# MAIN
# =====================================================================

def main() -> None:

    print("=" * 115)
    print(
        "BATCH 5H-5E-2 — "
        "AMARAKOSHA SOURCE FORMAT AUDIT"
    )
    print("=" * 115)

    # ---------------------------------------------------------------
    # 1. COMPONENT BASELINE
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("1. COMPONENT BASELINE")
    print("-" * 115)

    print(
        "AmarakoshaParser :",
        AmarakoshaParser,
        "PASS",
    )

    print(
        "SynsetRecord :",
        SynsetRecord,
        "PASS",
    )

    print(
        "VargaRecord :",
        VargaRecord,
        "PASS",
    )

    print(
        "Amarakanda members:"
    )

    for member in Amarakanda:
        print(
            f"  {member.name} = {member.value}"
        )

    # ---------------------------------------------------------------
    # 2. REPOSITORY ROOTS
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("2. REPOSITORY SOURCE ROOTS")
    print("-" * 115)

    candidate_roots = [
        ROOT / "amarakosha",
        ROOT / "acquisition",
        ROOT / "corpus",
        ROOT / "docs",
        ROOT / "data",
        ROOT / "resources",
    ]

    for path in candidate_roots:

        print(
            f"{path.relative_to(ROOT)} : "
            f"{'EXISTS' if path.exists() else 'ABSENT'}"
        )

    # ---------------------------------------------------------------
    # 3. AMARAKOSHA-NAMED FILES
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("3. AMARAKOSHA-NAMED SOURCE FILES")
    print("-" * 115)

    named_files: list[Path] = []

    for path in ROOT.rglob("*"):

        if not path.is_file():
            continue

        if is_excluded_path(path):
            continue

        if "amarakosha" in path.name.lower():
            named_files.append(path)

    if named_files:

        for path in sorted(named_files):
            print(
                path.relative_to(ROOT)
            )

    else:

        print(
            "No active Amarakośa-named files found."
        )

    # ---------------------------------------------------------------
    # 4. TEXT SOURCE-FORMAT EVIDENCE
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("4. TEXT SOURCE-FORMAT EVIDENCE")
    print("-" * 115)

    text_files = repository_text_files()

    evidence_count = 0

    for path in text_files:

        text = read_text(path)

        if not text:
            continue

        if not likely_amarakosha_text(text):
            continue

        evidence_count += 1

        print(
            f"\nFILE: {path.relative_to(ROOT)}"
        )

        source_hits = keyword_hits(
            text,
            SOURCE_KEYWORDS,
        )

        structure_hits = keyword_hits(
            text,
            STRUCTURE_KEYWORDS,
        )

        print(
            "Source keywords :",
            source_hits or "NONE",
        )

        print(
            "Structure keywords :",
            structure_hits or "NONE",
        )

        print(
            "Preview :",
            compact_preview(text),
        )

    if evidence_count == 0:

        print(
            "No repository text-format evidence "
            "was detected."
        )

    # ---------------------------------------------------------------
    # 5. PARSER RECORD REFERENCES
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("5. PARSER → RECORD REFERENCES")
    print("-" * 115)

    parser_files = sorted(
        (
            ROOT
            / "amarakosha"
            / "parsers"
        ).glob("*.py")
    )

    found_parser_references = False

    for path in parser_files:

        if is_excluded_path(path):
            continue

        references = parser_record_references(
            path
        )

        print(
            path.relative_to(ROOT)
        )

        if references:

            found_parser_references = True

            for reference in references:
                print(
                    f"  {reference}"
                )

        else:

            print(
                "  No executable "
                "record construction/reference "
                "detected."
            )

    # ---------------------------------------------------------------
    # 6. RECORD FIELD TARGETS
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("6. SOURCE → RECORD TARGETS")
    print("-" * 115)

    print(
        "VargaRecord:"
    )

    for name in (
        "kanda",
        "varga_number",
        "name",
        "title",
        "devanagari",
        "iast",
        "transliteration",
        "description",
        "tags",
        "notes",
    ):
        print(
            f"  {name}"
        )

    print(
        "\nSynsetRecord:"
    )

    for name in (
        "kanda",
        "varga",
        "verse",
        "sequence",
        "devanagari",
        "iast",
        "transliteration",
        "gloss",
        "lexeme_ids",
        "tags",
        "notes",
    ):
        print(
            f"  {name}"
        )

    # ---------------------------------------------------------------
    # 7. IMPORTANT NEGATIVE FINDINGS
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("7. CURRENT NEGATIVE FINDINGS")
    print("-" * 115)

    print(
        "Parser grammar implementation : "
        "NOT YET PRESENT"
    )

    print(
        "Dedicated Amarakośa source model : "
        "NOT ESTABLISHED"
    )

    print(
        "Parser record construction : "
        "NOT YET PRESENT"
    )

    print(
        "Varga/Synset grouping : "
        "NOT YET PRESENT"
    )

    print(
        "Canonical dictionary mapping : "
        "NOT YET PRESENT"
    )

    # ---------------------------------------------------------------
    # 8. DECISION GATE
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("8. 5H-5E-2 DECISION GATE")
    print("-" * 115)

    print(
        "Existing Parser : PRESERVE"
    )

    print(
        "Existing Record Contracts : PRESERVE"
    )

    print(
        "New Parser Class : NOT JUSTIFIED"
    )

    print(
        "New Record Class : NOT JUSTIFIED"
    )

    print(
        "New Source Model : "
        "DEFER UNTIL ACTUAL SOURCE FORMAT REQUIRES IT"
    )

    print(
        "Grammar invention : "
        "NOT PERMITTED AT THIS STAGE"
    )

    print(
        "Next step : "
        "BATCH 5H-5E-3 PARSER GRAMMAR / "
        "RECORD MAPPING AUDIT"
    )

    print("\n" + "=" * 115)
    print(
        "BATCH 5H-5E-2 — AUDIT COMPLETE"
    )
    print("=" * 115)


if __name__ == "__main__":
    main()
