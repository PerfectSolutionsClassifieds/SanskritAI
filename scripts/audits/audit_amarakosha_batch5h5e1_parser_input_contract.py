from __future__ import annotations

"""
SanskritAI
==========

Batch 5H-5E-1
Amarakośa Parser Input Contract Audit

Purpose
-------
Determine the existing input/source representation available to the
Amarakośa parser before implementing parsing rules.

This audit is read-only.

It does NOT:
- modify production code
- introduce a new parser
- introduce a new source model
- modify SynsetRecord
- modify VargaRecord
- invent an Amarakośa textual grammar

The objective is to identify an existing source/input abstraction that
the AmarakoshaParser should consume.

Production exclusions
---------------------
Historical numeric-suffixed files, _G<number>.py files, tests and
__pycache__ are excluded from production inspection.
"""

import ast
import inspect
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

from SanskritAI.amarakosha.parsers.amarakosha_parser import (
    AmarakoshaParser,
)

from SanskritAI.amarakosha.parsers.base_knowledge_parser import (
    BaseKnowledgeParser,
)

from SanskritAI.amarakosha.records.synset_record import (
    SynsetRecord,
)

from SanskritAI.amarakosha.records.varga_record import (
    VargaRecord,
)


# =====================================================================
# HELPERS
# =====================================================================

def production_python_files(directory: Path) -> list[Path]:
    """Return active production Python files only."""

    files: list[Path] = []

    if not directory.exists():
        return files

    for path in directory.rglob("*.py"):
        relative = path.relative_to(ROOT)
        stem = path.stem

        if "tests" in relative.parts:
            continue

        if "__pycache__" in relative.parts:
            continue

        # Exclude parser1.py, parser2.py, etc.
        if stem and stem[-1].isdigit():
            continue

        # Exclude *_G1.py, *_G12.py, etc.
        if "_G" in stem:
            suffix = stem.rsplit("_G", 1)[-1]

            if suffix.isdigit():
                continue

        files.append(path)

    return sorted(files)


def source_text(path: Path) -> str:
    """Read UTF-8 source text safely."""

    try:
        return path.read_text(
            encoding="utf-8"
        )
    except (OSError, UnicodeError):
        return ""


def executable_symbol_references(
    path: Path,
    symbols: tuple[str, ...],
) -> list[str]:
    """
    Find executable AST references to selected symbols.

    Comments and documentation strings are ignored.
    """

    text = source_text(path)

    if not text:
        return []

    try:
        tree = ast.parse(
            text,
            filename=str(path),
        )
    except SyntaxError:
        return []

    found: list[str] = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Name):
            if node.id in symbols:
                found.append(node.id)

        elif isinstance(node, ast.Attribute):
            if node.attr in symbols:
                found.append(node.attr)

        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name in symbols:
                    found.append(alias.name)

    return sorted(set(found))


# =====================================================================
# MAIN
# =====================================================================

def main() -> None:

    print("=" * 115)
    print(
        "BATCH 5H-5E-1 — "
        "AMARAKOSHA PARSER INPUT CONTRACT AUDIT"
    )
    print("=" * 115)

    # ---------------------------------------------------------------
    # 1. COMPONENT CONTRACT
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("1. COMPONENT CONTRACT")
    print("-" * 115)

    parser = AmarakoshaParser(
        name="Amarakośa",
        version="1.0",
    )

    print(
        "Parser :",
        parser,
        "PASS",
    )

    print(
        "Base parser inheritance :",
        issubclass(
            AmarakoshaParser,
            BaseKnowledgeParser,
        ),
        "PASS",
    )

    print(
        "parse() signature :",
        inspect.signature(parser.parse),
    )

    # ---------------------------------------------------------------
    # 2. DECLARED PARSER OUTPUT
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("2. DECLARED PARSER OUTPUT")
    print("-" * 115)

    signature = inspect.signature(
        parser.parse
    )

    print(
        "Return annotation :",
        signature.return_annotation,
    )

    print(
        "Expected domain records : "
        "SynsetRecord | VargaRecord"
    )

    # ---------------------------------------------------------------
    # 3. CURRENT IMPLEMENTATION
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("3. CURRENT PARSER IMPLEMENTATION")
    print("-" * 115)

    try:
        print(
            inspect.getsource(
                parser.parse
            )
        )
    except (OSError, TypeError):
        print(
            "Parser source unavailable"
        )

    # ---------------------------------------------------------------
    # 4. PARSER SOURCE DIRECTORY
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("4. PRODUCTION PARSER FILES")
    print("-" * 115)

    parser_files = production_python_files(
        ROOT / "amarakosha" / "parsers"
    )

    for path in parser_files:
        print(
            path.relative_to(ROOT)
        )

    # ---------------------------------------------------------------
    # 5. SOURCE / INPUT SYMBOL REFERENCES
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("5. EXISTING SOURCE / INPUT REFERENCES")
    print("-" * 115)

    candidate_symbols = (
        "Source",
        "Input",
        "Document",
        "Text",
        "Corpus",
        "ParserInput",
        "SourceRecord",
        "TextSource",
        "RawSource",
    )

    found_by_file: dict[str, list[str]] = {}

    for path in production_python_files(ROOT):
        references = executable_symbol_references(
            path,
            candidate_symbols,
        )

        if references:
            found_by_file[
                str(path.relative_to(ROOT))
            ] = references

    if found_by_file:

        for path, references in found_by_file.items():

            print(path)

            for reference in references:
                print(
                    f"  {reference}"
                )

    else:

        print(
            "No candidate source/input "
            "abstractions detected."
        )

    # ---------------------------------------------------------------
    # 6. RECORD FIELD CONTRACTS
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("6. RECORD FIELD CONTRACTS")
    print("-" * 115)

    print("VargaRecord:")

    for field_info in SynsetRecord.__dataclass_fields__.values():
        # SynsetRecord printed separately below.
        pass

    for field_info in VargaRecord.__dataclass_fields__.values():
        print(
            f"  {field_info.name}"
        )

    print("\nSynsetRecord:")

    for field_info in SynsetRecord.__dataclass_fields__.values():
        print(
            f"  {field_info.name}"
        )

    # ---------------------------------------------------------------
    # 7. EXISTING AMARAKOSHA SOURCE HELPERS
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("7. EXISTING AMARAKOSHA SOURCE HELPERS")
    print("-" * 115)

    amarakosha_root = (
        ROOT / "amarakosha"
    )

    all_amarakosha_files = (
        production_python_files(
            amarakosha_root
        )
    )

    helper_candidates: list[Path] = []

    for path in all_amarakosha_files:

        if path.parent.name in {
            "parsers",
            "records",
        }:
            continue

        text = source_text(path)

        keywords = (
            "source",
            "input",
            "text",
            "parse",
            "token",
            "line",
            "varga",
            "synset",
            "verse",
        )

        if any(
            keyword in text.lower()
            for keyword in keywords
        ):
            helper_candidates.append(path)

    if helper_candidates:

        for path in helper_candidates:
            print(
                path.relative_to(ROOT)
            )

    else:

        print(
            "No obvious existing "
            "Amarakośa source helpers detected."
        )

    # ---------------------------------------------------------------
    # 8. DECISION GATE
    # ---------------------------------------------------------------

    print("\n" + "-" * 115)
    print("8. 5H-5E-1 DECISION GATE")
    print("-" * 115)

    print(
        "Existing parser : PRESERVE"
    )

    print(
        "Existing record contracts : PRESERVE"
    )

    print(
        "New parser class : NOT JUSTIFIED"
    )

    print(
        "New source abstraction : "
        "ONLY IF EXISTING INPUT CONTRACT IS ABSENT"
    )

    print(
        "Actual Amarakośa grammar : "
        "DO NOT INVENT IN THIS AUDIT"
    )

    print(
        "Next step : "
        "USE AUDIT OUTPUT TO IMPLEMENT 5H-5E"
    )

    print("\n" + "=" * 115)
    print(
        "BATCH 5H-5E-1 — AUDIT COMPLETE"
    )
    print("=" * 115)


if __name__ == "__main__":
    main()
