from __future__ import annotations

"""
SanskritAI
==========

Batch 5H-5D
Amarakośa Parser → Record Semantic Audit

Purpose
-------
Read-only architectural audit of the existing Amarakośa parser and
its relationship with VargaRecord and SynsetRecord.

This audit does NOT modify production code.

Questions
---------
1. What does AmarakoshaParser currently expose?
2. What does BaseKnowledgeParser require?
3. What does parser.parse() currently do?
4. Which record fields are available to the parser?
5. Are VargaRecord and SynsetRecord compatible with the parser boundary?
6. Which parser → record mappings are already implemented?
7. Which mappings remain to be implemented?

Production exclusions
---------------------
Historical numeric-suffixed files and _G<number>.py files are not
considered production implementations by this audit.
"""

import ast
import inspect
from dataclasses import fields, is_dataclass
from pathlib import Path

from SanskritAI.amarakosha.enums.Amarakanda import Amarakanda
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


ROOT = Path("/content/SanskritAI")


def production_python_files(directory: Path) -> list[Path]:
    """Return active production Python files only."""

    files: list[Path] = []

    for path in directory.rglob("*.py"):
        relative = path.relative_to(ROOT)
        name = path.name

        if "tests" in relative.parts:
            continue

        if "__pycache__" in relative.parts:
            continue

        # Historical numbered files.
        stem = path.stem

        if stem and stem[-1:].isdigit():
            continue

        # Historical generation files such as *_G12.py.
        if "_G" in stem:
            suffix = stem.rsplit("_G", 1)[-1]
            if suffix.isdigit():
                continue

        files.append(path)

    return sorted(files)


def ast_imports_and_calls(path: Path) -> list[str]:
    """Collect executable references to parser/record symbols."""

    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except (OSError, SyntaxError):
        return []

    references: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                references.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                references.append(
                    f"{module}.{alias.name}"
                )

        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                references.append(node.func.id)

            elif isinstance(node.func, ast.Attribute):
                references.append(node.func.attr)

    return references


def print_dataclass_contract(record_type: type[object]) -> None:
    """Print the complete dataclass field contract."""

    print(f"{record_type.__name__} fields:")

    if not is_dataclass(record_type):
        print("  NOT A DATACLASS")
        return

    for field_info in fields(record_type):
        print(
            f"  {field_info.name}: "
            f"{field_info.type}"
        )


def main() -> None:
    print("=" * 115)
    print("BATCH 5H-5D — AMARAKOSHA PARSER → RECORD SEMANTIC AUDIT")
    print("=" * 115)

    # ---------------------------------------------------------
    # 1. Component resolution
    # ---------------------------------------------------------

    print("\n" + "-" * 115)
    print("1. COMPONENT RESOLUTION")
    print("-" * 115)

    print(
        "AmarakoshaParser :",
        AmarakoshaParser,
        "PASS",
    )

    print(
        "BaseKnowledgeParser :",
        BaseKnowledgeParser,
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

    # ---------------------------------------------------------
    # 2. Parser inheritance
    # ---------------------------------------------------------

    print("\n" + "-" * 115)
    print("2. PARSER INHERITANCE")
    print("-" * 115)

    print("AmarakoshaParser MRO:")

    for cls in inspect.getmro(AmarakoshaParser):
        print(f"  {cls.__module__}.{cls.__name__}")

    print(
        "BaseKnowledgeParser inheritance :",
        issubclass(
            AmarakoshaParser,
            BaseKnowledgeParser,
        ),
        "PASS"
        if issubclass(
            AmarakoshaParser,
            BaseKnowledgeParser,
        )
        else "FAIL",
    )

    # ---------------------------------------------------------
    # 3. Parser constructor
    # ---------------------------------------------------------

    print("\n" + "-" * 115)
    print("3. PARSER CONSTRUCTOR CONTRACT")
    print("-" * 115)

    print(
        "Constructor signature :",
        inspect.signature(
            AmarakoshaParser
        ),
    )

    parser = AmarakoshaParser(
        name="Amarakośa",
        version="1.0",
    )

    print(
        "Parser construction : PASS"
    )

    print(
        "Parser name :",
        parser.name,
    )

    print(
        "Parser version :",
        parser.version,
    )

    # ---------------------------------------------------------
    # 4. Parse method contract
    # ---------------------------------------------------------

    print("\n" + "-" * 115)
    print("4. PARSE METHOD CONTRACT")
    print("-" * 115)

    parse_method = getattr(
        parser,
        "parse",
        None,
    )

    print(
        "parse() exists :",
        callable(parse_method),
        "PASS"
        if callable(parse_method)
        else "FAIL",
    )

    if callable(parse_method):
        print(
            "parse() signature :",
            inspect.signature(parse_method),
        )

        try:
            source = inspect.getsource(
                parse_method
            )

            print("\nparse() source:")
            print(source)

        except (OSError, TypeError):
            print(
                "parse() source : UNAVAILABLE"
            )

    # ---------------------------------------------------------
    # 5. Record contracts
    # ---------------------------------------------------------

    print("\n" + "-" * 115)
    print("5. RECORD CONTRACTS")
    print("-" * 115)

    print_dataclass_contract(
        VargaRecord
    )

    print()

    print_dataclass_contract(
        SynsetRecord
    )

    # ---------------------------------------------------------
    # 6. Amarakośa enum contract
    # ---------------------------------------------------------

    print("\n" + "-" * 115)
    print("6. AMARAKANDA CONTRACT")
    print("-" * 115)

    print("Amarakanda members:")

    for member in Amarakanda:
        print(
            f"  {member.name} = {member.value}"
        )

    print(
        "SVARGADI available :",
        hasattr(
            Amarakanda,
            "SVARGADI",
        ),
        "PASS"
        if hasattr(
            Amarakanda,
            "SVARGADI",
        )
        else "FAIL",
    )

    # ---------------------------------------------------------
    # 7. Production parser references
    # ---------------------------------------------------------

    print("\n" + "-" * 115)
    print("7. PRODUCTION PARSER / RECORD REFERENCES")
    print("-" * 115)

    amarakosha_root = (
        ROOT / "amarakosha"
    )

    parser_files = production_python_files(
        amarakosha_root / "parsers"
    )

    record_files = production_python_files(
        amarakosha_root / "records"
    )

    print(
        "Production parser files :",
        len(parser_files),
    )

    for path in parser_files:
        print(
            "  ",
            path.relative_to(ROOT),
        )

    print(
        "Production record files :",
        len(record_files),
    )

    for path in record_files:
        print(
            "  ",
            path.relative_to(ROOT),
        )

    # ---------------------------------------------------------
    # 8. Parser → Record executable references
    # ---------------------------------------------------------

    print("\n" + "-" * 115)
    print("8. PARSER → RECORD EXECUTABLE REFERENCES")
    print("-" * 115)

    parser_record_references: dict[str, list[str]] = {}

    for path in parser_files:
        references = ast_imports_and_calls(path)

        relevant = [
            reference
            for reference in references
            if (
                "SynsetRecord" in reference
                or "VargaRecord" in reference
                or "synset_record" in reference
                or "varga_record" in reference
            )
        ]

        parser_record_references[
            str(path.relative_to(ROOT))
        ] = sorted(set(relevant))

    for path, references in parser_record_references.items():
        print(path)

        if references:
            for reference in references:
                print(
                    f"  {reference}"
                )
        else:
            print(
                "  No executable "
                "parser→record reference detected"
            )

    # ---------------------------------------------------------
    # 9. Mapping questions
    # ---------------------------------------------------------

    print("\n" + "-" * 115)
    print("9. SEMANTIC MAPPING QUESTIONS")
    print("-" * 115)

    print(
        "Kanda source → VargaRecord.kanda / "
        "SynsetRecord.kanda : INSPECT"
    )

    print(
        "Varga number → VargaRecord.varga_number : INSPECT"
    )

    print(
        "Varga identity → SynsetRecord.varga : INSPECT"
    )

    print(
        "Varga name/title → VargaRecord.name/title : INSPECT"
    )

    print(
        "Verse → SynsetRecord.verse : INSPECT"
    )

    print(
        "Sequence → SynsetRecord.sequence : INSPECT"
    )

    print(
        "Devanagari → record text fields : INSPECT"
    )

    print(
        "IAST → record text fields : INSPECT"
    )

    print(
        "Transliteration → record text fields : INSPECT"
    )

    print(
        "Gloss → SynsetRecord.gloss : INSPECT"
    )

    print(
        "Lexeme references → "
        "SynsetRecord.lexeme_ids : INSPECT"
    )

    print(
        "Provenance → source/source_identifier/"
        "source_version : INSPECT"
    )

    # ---------------------------------------------------------
    # 10. Architectural decision gate
    # ---------------------------------------------------------

    print("\n" + "-" * 115)
    print("10. 5H-5D DECISION GATE")
    print("-" * 115)

    print(
        "Parser implementation : "
        "DO NOT MODIFY IN THIS AUDIT"
    )

    print(
        "Record contracts : "
        "PRESERVE"
    )

    print(
        "New parser abstraction : "
        "NOT JUSTIFIED"
    )

    print(
        "New record abstraction : "
        "NOT JUSTIFIED"
    )

    print(
        "Next production step : "
        "BATCH 5H-5E PARSER → RECORD IMPLEMENTATION"
    )

    print("\n" + "=" * 115)
    print(
        "BATCH 5H-5D — SEMANTIC AUDIT COMPLETE"
    )
    print("=" * 115)


if __name__ == "__main__":
    main()
