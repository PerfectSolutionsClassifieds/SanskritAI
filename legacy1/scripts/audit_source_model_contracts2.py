
"""
SanskritAI — Active Source Model Contract Comparison Audit

Purpose
-------
Compare ONLY active production Source model implementations.

Excluded:
    - tests
    - scripts
    - cache directories
    - historical numbered copies (*1.py, *2.py, ...)

Target models:
    CorpusSource
    CanonicalSource
    LexicalSource
    MonierWilliamsSource

The script compares:
    - decorators
    - bases
    - fields
    - methods
    - properties

It does NOT modify production code.
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
class Contract:
    name: str
    module: str
    file: Path
    line: int
    bases: set[str]
    fields: set[str]
    methods: set[str]
    properties: set[str]
    decorators: set[str]


def module_name(path: Path) -> str:

    relative = path.relative_to(PROJECT_ROOT)

    parts = list(relative.with_suffix("").parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]

    return ".".join(parts)


def excluded(path: Path) -> bool:

    if any(
        part in EXCLUDED_PARTS
        for part in path.parts
    ):
        return True

    if NUMBERED_COPY_PATTERN.match(path.stem):
        return True

    return False


def expression_name(
    node: ast.expr,
) -> str:

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        return node.attr

    return ast.unparse(node)


def inspect_class(
    node: ast.ClassDef,
    module: str,
    path: Path,
) -> Contract:

    bases = {
        expression_name(base)
        for base in node.bases
    }

    fields: set[str] = set()
    methods: set[str] = set()
    properties: set[str] = set()
    decorators: set[str] = set()

    for decorator in node.decorator_list:

        decorators.add(
            expression_name(decorator)
        )

    for item in node.body:

        if isinstance(item, ast.AnnAssign):

            if isinstance(
                item.target,
                ast.Name,
            ):
                fields.add(
                    item.target.id
                )

        elif isinstance(item, ast.Assign):

            for target in item.targets:

                if isinstance(
                    target,
                    ast.Name,
                ):
                    fields.add(
                        target.id
                    )

        elif isinstance(
            item,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):

            methods.add(item.name)

            for decorator in item.decorator_list:

                if isinstance(
                    decorator,
                    ast.Name,
                ):

                    if decorator.id == "property":
                        properties.add(
                            item.name
                        )

                elif isinstance(
                    decorator,
                    ast.Attribute,
                ):

                    if decorator.attr == "property":
                        properties.add(
                            item.name
                        )

    return Contract(
        name=node.name,
        module=module,
        file=path,
        line=node.lineno,
        bases=bases,
        fields=fields,
        methods=methods,
        properties=properties,
        decorators=decorators,
    )


def scan() -> list[Contract]:

    contracts: list[Contract] = []

    for path in PROJECT_ROOT.rglob("*.py"):

        if excluded(path):
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

        module = module_name(path)

        for node in tree.body:

            if not isinstance(
                node,
                ast.ClassDef,
            ):
                continue

            if node.name not in TARGET_NAMES:
                continue

            contracts.append(
                inspect_class(
                    node,
                    module,
                    path,
                )
            )

    return sorted(
        contracts,
        key=lambda item: (
            item.name,
            item.module,
        ),
    )


def compare_attribute(
    contracts: list[Contract],
    attribute: str,
) -> None:

    values = {
        contract.module:
        getattr(contract, attribute)
        for contract in contracts
    }

    modules = sorted(values)

    if not modules:
        return

    common = set.intersection(
        *(
            values[module]
            for module in modules
        )
    )

    print(
        f"COMMON {attribute.upper()}:"
    )

    print(
        "  "
        + (
            ", ".join(sorted(common))
            if common
            else "(none)"
        )
    )

    print()

    print(
        f"UNIQUE {attribute.upper()} BY MODULE:"
    )

    for module in modules:

        others = [
            values[other]
            for other in modules
            if other != module
        ]

        if others:

            other_union = set.union(
                *others
            )

            unique = (
                values[module]
                - other_union
            )

        else:
            unique = values[module]

        print(
            f"  {module}: "
            + (
                ", ".join(
                    sorted(unique)
                )
                if unique
                else "(none)"
            )
        )

    print()


def print_report(
    contracts: list[Contract],
) -> None:

    print("=" * 80)
    print(
        "SANSKRITAI — ACTIVE SOURCE MODEL "
        "CONTRACT COMPARISON"
    )
    print("=" * 80)
    print()

    print(
        f"Active production definitions: "
        f"{len(contracts)}"
    )

    print()

    for contract in contracts:

        print("-" * 80)

        print(contract.name)

        print(
            f"Module      : {contract.module}"
        )

        print(
            f"File        : {contract.file}"
        )

        print(
            f"Line        : {contract.line}"
        )

        print(
            "Decorators  : "
            + (
                ", ".join(
                    sorted(
                        contract.decorators
                    )
                )
                if contract.decorators
                else "(none)"
            )
        )

        print(
            "Bases       : "
            + (
                ", ".join(
                    sorted(
                        contract.bases
                    )
                )
                if contract.bases
                else "(none)"
            )
        )

        print(
            "Fields      : "
            + (
                ", ".join(
                    sorted(
                        contract.fields
                    )
                )
                if contract.fields
                else "(none)"
            )
        )

        print(
            "Methods     : "
            + (
                ", ".join(
                    sorted(
                        contract.methods
                    )
                )
                if contract.methods
                else "(none)"
            )
        )

        print(
            "Properties  : "
            + (
                ", ".join(
                    sorted(
                        contract.properties
                    )
                )
                if contract.properties
                else "(none)"
            )
        )

        print()

    print("=" * 80)
    print("STRUCTURAL COMPARISON")
    print("=" * 80)
    print()

    for attribute in (
        "fields",
        "methods",
        "properties",
        "bases",
    ):

        compare_attribute(
            contracts,
            attribute,
        )

    print("=" * 80)
    print(
        "NUMBERED HISTORICAL COPIES: EXCLUDED"
    )
    print("=" * 80)
    print()

    print("=" * 80)
    print(
        "AUDIT COMPLETE — NO FILES MODIFIED"
    )
    print("=" * 80)


def main() -> None:

    contracts = scan()

    print_report(contracts)


if __name__ == "__main__":
    main()
