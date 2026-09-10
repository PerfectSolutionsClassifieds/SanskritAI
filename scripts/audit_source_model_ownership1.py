
"""
SanskritAI — Source Model Ownership Audit

Purpose
-------
Identify every production "Source" model and determine:

1. Where the model is defined.
2. What architectural layer owns it.
3. What responsibility it appears to represent.
4. Which production modules import/use it.
5. Whether it is an identity/provenance model or an acquisition/content model.

This script is intentionally READ-ONLY.
It does not modify production code.

Target models
-------------
- CorpusSource
- CanonicalSource
- LexicalSource
- MonierWilliamsSource
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path("/content/SanskritAI")

SOURCE_MODEL_NAMES = {
    "CorpusSource",
    "CanonicalSource",
    "LexicalSource",
    "MonierWilliamsSource",
}


@dataclass
class SourceModelDefinition:
    name: str
    file: Path
    line: int
    module: str
    bases: list[str]
    fields: list[str]
    methods: list[str]


def module_name(path: Path) -> str:
    relative = path.relative_to(PROJECT_ROOT)
    parts = list(relative.with_suffix("").parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]

    return ".".join(parts)


def get_base_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        return node.attr

    return ast.unparse(node)


def extract_fields(node: ast.ClassDef) -> list[str]:
    fields: list[str] = []

    for item in node.body:
        if isinstance(item, ast.AnnAssign):
            if isinstance(item.target, ast.Name):
                fields.append(item.target.id)

        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    fields.append(target.id)

    return fields


def extract_methods(node: ast.ClassDef) -> list[str]:
    methods: list[str] = []

    for item in node.body:
        if isinstance(
            item,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            methods.append(item.name)

    return methods


def scan_definitions() -> list[SourceModelDefinition]:
    results: list[SourceModelDefinition] = []

    for path in PROJECT_ROOT.rglob("*.py"):
        if any(
            part in {
                ".git",
                "__pycache__",
                ".pytest_cache",
            }
            for part in path.parts
        ):
            continue

        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue

        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            if node.name not in SOURCE_MODEL_NAMES:
                continue

            results.append(
                SourceModelDefinition(
                    name=node.name,
                    file=path,
                    line=node.lineno,
                    module=module_name(path),
                    bases=[
                        get_base_name(base)
                        for base in node.bases
                    ],
                    fields=extract_fields(node),
                    methods=extract_methods(node),
                )
            )

    return sorted(
        results,
        key=lambda item: (
            item.name,
            str(item.file),
            item.line,
        ),
    )


def classify(definition: SourceModelDefinition) -> str:
    path = definition.file.as_posix()

    if "/acquisition/models/" in path:
        if definition.name == "CorpusSource":
            return "Generic acquisition source identity"

    if "/acquisition/knowledge/models/" in path:
        if definition.name == "CanonicalSource":
            return "Canonical provenance / source metadata"

    if "/domain/lexical/" in path:
        if definition.name == "LexicalSource":
            return "Domain lexical source identity"

    if "/lexical/models/" in path:
        if definition.name == "LexicalSource":
            return "Lexical model source metadata"

    if "/acquisition/sources/" in path:
        if definition.name == "MonierWilliamsSource":
            return "Monier-Williams source metadata"

    if "/acquisition/lexical/monier_williams/" in path:
        if definition.name == "MonierWilliamsSource":
            return "Monier-Williams raw-content source contract"

    return "Unknown / requires review"


def print_report(definitions: list[SourceModelDefinition]) -> None:
    print("=" * 80)
    print("SANSKRITAI — SOURCE MODEL OWNERSHIP AUDIT")
    print("=" * 80)
    print()

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Definitions found: {len(definitions)}")
    print()

    if not definitions:
        print("No source model definitions found.")
        return

    for index, definition in enumerate(definitions, start=1):
        print("-" * 80)
        print(f"[{index}] {definition.name}")
        print(f"File       : {definition.file}")
        print(f"Line       : {definition.line}")
        print(f"Module     : {definition.module}")
        print(f"Ownership  : {classify(definition)}")

        print(
            "Bases      : "
            + (
                ", ".join(definition.bases)
                if definition.bases
                else "(none)"
            )
        )

        print(
            "Fields     : "
            + (
                ", ".join(definition.fields)
                if definition.fields
                else "(none)"
            )
        )

        print(
            "Methods    : "
            + (
                ", ".join(definition.methods)
                if definition.methods
                else "(none)"
            )
        )

        print()

    print("=" * 80)
    print("OWNERSHIP SUMMARY")
    print("=" * 80)

    grouped: dict[str, list[SourceModelDefinition]] = {}

    for definition in definitions:
        grouped.setdefault(
            definition.name,
            [],
        ).append(definition)

    for name in sorted(grouped):
        items = grouped[name]

        print()
        print(f"{name}: {len(items)} definition(s)")

        for item in items:
            print(
                f"  - {item.module}"
                f"  -> {classify(item)}"
            )

    print()
    print("=" * 80)
    print("AUDIT COMPLETE — NO FILES WERE MODIFIED")
    print("=" * 80)


def main() -> None:
    definitions = scan_definitions()
    print_report(definitions)


if __name__ == "__main__":
    main()

    
