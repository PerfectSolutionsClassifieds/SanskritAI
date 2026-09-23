
"""
SanskritAI — Production Source Model Ownership Audit

Purpose
-------
Audit ONLY active production source-model definitions.

Excluded:
- tests/
- scripts/
- .git/
- __pycache__/
- .pytest_cache/
- historical numbered copies:
      *1.py
      *2.py
      *3.py
      ...
      *10.py
      etc.

Target concepts:
    CorpusSource
    CanonicalSource
    LexicalSource
    MonierWilliamsSource

This is a READ-ONLY architectural audit.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path("/content/SanskritAI")

TARGET_NAMES = {
    "CorpusSource",
    "CanonicalSource",
    "LexicalSource",
    "MonierWilliamsSource",
}

EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "tests",
    "scripts",
}

NUMBERED_COPY_PATTERN = re.compile(r".*\d+$")


@dataclass
class SourceModel:
    name: str
    module: str
    file: Path
    line: int
    bases: list[str]
    fields: list[str]
    methods: list[str]
    properties: list[str]


def module_name(path: Path) -> str:

    relative = path.relative_to(PROJECT_ROOT)

    parts = list(relative.with_suffix("").parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]

    return ".".join(parts)


def is_excluded(path: Path) -> bool:

    if any(
        part in EXCLUDED_PARTS
        for part in path.parts
    ):
        return True

    # Ignore historical copies:
    # canonical_source1.py
    # canonical_source2.py
    # source_index4.py
    # mapper7.py
    # etc.
    if NUMBERED_COPY_PATTERN.match(path.stem):
        return True

    return False


def expression_name(node: ast.expr) -> str:

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        return node.attr

    return ast.unparse(node)


def inspect_class(
    node: ast.ClassDef,
) -> tuple[
    list[str],
    list[str],
    list[str],
    list[str],
]:

    bases = [
        expression_name(base)
        for base in node.bases
    ]

    fields: list[str] = []
    methods: list[str] = []
    properties: list[str] = []

    for item in node.body:

        if isinstance(item, ast.AnnAssign):

            if isinstance(
                item.target,
                ast.Name,
            ):
                fields.append(
                    item.target.id
                )

        elif isinstance(item, ast.Assign):

            for target in item.targets:

                if isinstance(
                    target,
                    ast.Name,
                ):
                    fields.append(
                        target.id
                    )

        elif isinstance(
            item,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):

            methods.append(item.name)

            for decorator in item.decorator_list:

                if isinstance(
                    decorator,
                    ast.Name,
                ):
                    if decorator.id == "property":
                        properties.append(
                            item.name
                        )

                elif isinstance(
                    decorator,
                    ast.Attribute,
                ):
                    if decorator.attr == "property":
                        properties.append(
                            item.name
                        )

    return (
        bases,
        fields,
        methods,
        properties,
    )


def classify(model: SourceModel) -> str:

    module = model.module

    if module == "acquisition.models.corpus_source":
        return (
            "GENERIC ACQUISITION "
            "SOURCE IDENTITY"
        )

    if module == (
        "acquisition.knowledge.models."
        "canonical_source"
    ):
        return (
            "CANONICAL PROVENANCE / "
            "SOURCE METADATA"
        )

    if module == (
        "domain.lexical.lexical_source"
    ):
        return (
            "DOMAIN LEXICAL "
            "SOURCE IDENTITY"
        )

    if module == (
        "lexical.models.lexical_source"
    ):
        return (
            "LEXICAL MODEL "
            "SOURCE METADATA"
        )

    if module == (
        "acquisition.sources.monier_williams"
    ):
        return (
            "MONIER-WILLIAMS "
            "SOURCE METADATA"
        )

    if module == (
        "acquisition.lexical.monier_williams."
        "monier_williams_source"
    ):
        return (
            "MONIER-WILLIAMS "
            "RAW CONTENT CONTRACT"
        )

    return "UNCLASSIFIED SOURCE MODEL"


def scan() -> list[SourceModel]:

    results: list[SourceModel] = []

    for path in PROJECT_ROOT.rglob("*.py"):

        if is_excluded(path):
            continue

        try:
            source = path.read_text(
                encoding="utf-8"
            )
            tree = ast.parse(source)

        except (
            OSError,
            UnicodeDecodeError,
            SyntaxError,
        ):
            continue

        current_module = module_name(path)

        for node in tree.body:

            if not isinstance(
                node,
                ast.ClassDef,
            ):
                continue

            if node.name not in TARGET_NAMES:
                continue

            (
                bases,
                fields,
                methods,
                properties,
            ) = inspect_class(node)

            results.append(
                SourceModel(
                    name=node.name,
                    module=current_module,
                    file=path,
                    line=node.lineno,
                    bases=bases,
                    fields=fields,
                    methods=methods,
                    properties=properties,
                )
            )

    return sorted(
        results,
        key=lambda item: (
            item.name,
            item.module,
        ),
    )


def print_report(
    models: list[SourceModel],
) -> None:

    print("=" * 80)
    print(
        "SANSKRITAI — PRODUCTION SOURCE "
        "MODEL OWNERSHIP AUDIT"
    )
    print("=" * 80)
    print()

    print(
        f"Production definitions found: "
        f"{len(models)}"
    )
    print()

    for index, model in enumerate(
        models,
        start=1,
    ):

        print("-" * 80)

        print(
            f"[{index}] {model.name}"
        )

        print(
            f"Module      : {model.module}"
        )

        print(
            f"File        : {model.file}"
        )

        print(
            f"Line        : {model.line}"
        )

        print(
            f"Ownership   : {classify(model)}"
        )

        print(
            "Bases       : "
            + (
                ", ".join(model.bases)
                if model.bases
                else "(none)"
            )
        )

        print(
            "Fields      : "
            + (
                ", ".join(model.fields)
                if model.fields
                else "(none)"
            )
        )

        print(
            "Methods     : "
            + (
                ", ".join(model.methods)
                if model.methods
                else "(none)"
            )
        )

        print(
            "Properties  : "
            + (
                ", ".join(model.properties)
                if model.properties
                else "(none)"
            )
        )

        print()

    print("=" * 80)
    print("CONCEPT SUMMARY")
    print("=" * 80)
    print()

    grouped: dict[
        str,
        list[SourceModel],
    ] = {}

    for model in models:

        grouped.setdefault(
            model.name,
            [],
        ).append(model)

    for name in sorted(grouped):

        items = grouped[name]

        print(
            f"{name}: "
            f"{len(items)} production definition(s)"
        )

        for item in items:

            print(
                f"  - {item.module}"
                f" -> {classify(item)}"
            )

        print()

    print("=" * 80)
    print(
        "NUMBERED HISTORICAL COPIES: EXCLUDED"
    )
    print("=" * 80)
    print()

    print(
        "Excluded pattern: "
        "*<number>.py"
    )

    print()

    print("=" * 80)
    print(
        "AUDIT COMPLETE — NO FILES MODIFIED"
    )
    print("=" * 80)


def main() -> None:

    models = scan()

    print_report(models)


if __name__ == "__main__":
    main()
