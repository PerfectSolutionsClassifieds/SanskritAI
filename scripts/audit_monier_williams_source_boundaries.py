
"""
SanskritAI — Monier-Williams Source Boundary Audit

Purpose
-------
Audit the two Monier-Williams source concepts currently present in
the repository:

1. acquisition.sources.MonierWilliamsSource
   ----------------------------------------
   Metadata / source identity model.

2. acquisition.lexical.monier_williams.MonierWilliamsSource
   ---------------------------------------------------------
   Raw-content source contract.

The purpose is NOT to merge them automatically.

This script determines:

- where each class is defined
- its inheritance
- fields
- public methods/properties
- imports
- production consumers
- whether the implementation appears to be
  metadata-oriented or raw-content-oriented

This is an architectural READ-ONLY audit.
No production files are modified.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


PROJECT_ROOT = Path("/content/SanskritAI")

TARGETS = {
    "acquisition.sources.monier_williams": "MonierWilliamsSource",
    "acquisition.lexical.monier_williams.monier_williams_source":
        "MonierWilliamsSource",
}


@dataclass
class SourceBoundary:
    module: str
    name: str
    file: Path
    line: int
    bases: list[str] = field(default_factory=list)
    fields: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    properties: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    consumers: list[str] = field(default_factory=list)


def module_name(path: Path) -> str:
    relative = path.relative_to(PROJECT_ROOT)
    parts = list(relative.with_suffix("").parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]

    return ".".join(parts)


def expression_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        return node.attr

    return ast.unparse(node)


def get_import_name(node: ast.Import | ast.ImportFrom) -> str:
    if isinstance(node, ast.Import):
        return ", ".join(
            alias.name
            for alias in node.names
        )

    module = node.module or ""

    names = ", ".join(
        alias.name
        for alias in node.names
    )

    if module:
        return f"{module}: {names}"

    return names


def collect_class_information(
    node: ast.ClassDef,
) -> tuple[
    list[str],
    list[str],
    list[str],
    list[str],
]:
    bases: list[str] = []
    fields: list[str] = []
    methods: list[str] = []
    properties: list[str] = []

    for base in node.bases:
        bases.append(expression_name(base))

    for item in node.body:
        if isinstance(item, ast.AnnAssign):
            if isinstance(item.target, ast.Name):
                fields.append(item.target.id)

        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    fields.append(target.id)

        elif isinstance(
            item,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            methods.append(item.name)

            for decorator in item.decorator_list:
                if isinstance(decorator, ast.Name):
                    if decorator.id == "property":
                        properties.append(item.name)

                elif isinstance(decorator, ast.Attribute):
                    if decorator.attr == "property":
                        properties.append(item.name)

    return bases, fields, methods, properties


def locate_target_definitions() -> list[SourceBoundary]:
    results: list[SourceBoundary] = []

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
        except (
            OSError,
            UnicodeDecodeError,
            SyntaxError,
        ):
            continue

        current_module = module_name(path)

        if current_module not in TARGETS:
            continue

        target_name = TARGETS[current_module]

        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            if node.name != target_name:
                continue

            (
                bases,
                fields,
                methods,
                properties,
            ) = collect_class_information(node)

            imports = []

            for item in tree.body:
                if isinstance(
                    item,
                    (ast.Import, ast.ImportFrom),
                ):
                    imports.append(
                        get_import_name(item)
                    )

            results.append(
                SourceBoundary(
                    module=current_module,
                    name=node.name,
                    file=path,
                    line=node.lineno,
                    bases=bases,
                    fields=fields,
                    methods=methods,
                    properties=properties,
                    imports=imports,
                )
            )

    return results


def find_consumers(
    boundaries: list[SourceBoundary],
) -> None:
    for boundary in boundaries:
        module_path = boundary.module

        for path in PROJECT_ROOT.rglob("*.py"):
            if path == boundary.file:
                continue

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
                source = path.read_text(
                    encoding="utf-8"
                )
            except (
                OSError,
                UnicodeDecodeError,
            ):
                continue

            try:
                tree = ast.parse(source)
            except SyntaxError:
                continue

            found = False

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    ast.ImportFrom,
                ):
                    imported_module = (
                        node.module or ""
                    )

                    if imported_module == module_path:
                        for alias in node.names:
                            if (
                                alias.name
                                == boundary.name
                            ):
                                found = True

                elif isinstance(
                    node,
                    ast.Import,
                ):
                    for alias in node.names:
                        if alias.name == module_path:
                            found = True

                elif isinstance(
                    node,
                    ast.Name,
                ):
                    if node.id == boundary.name:
                        found = True

            if found:
                boundary.consumers.append(
                    str(path.relative_to(PROJECT_ROOT))
                )


def classify_boundary(
    boundary: SourceBoundary,
) -> str:

    if boundary.module == (
        "acquisition.sources.monier_williams"
    ):
        return (
            "METADATA SOURCE MODEL — "
            "describes source identity/provenance"
        )

    if boundary.module == (
        "acquisition.lexical.monier_williams.monier_williams_source"
    ):
        return (
            "RAW CONTENT SOURCE CONTRACT — "
            "provides/acquires raw dictionary content"
        )

    return "UNKNOWN"


def print_boundary(
    boundary: SourceBoundary,
    index: int,
) -> None:

    print("-" * 80)
    print(f"[{index}] {boundary.name}")
    print()

    print(f"Module      : {boundary.module}")
    print(f"File        : {boundary.file}")
    print(f"Line        : {boundary.line}")
    print(f"Boundary    : {classify_boundary(boundary)}")

    print()

    print(
        "Bases       : "
        + (
            ", ".join(boundary.bases)
            if boundary.bases
            else "(none)"
        )
    )

    print(
        "Fields      : "
        + (
            ", ".join(boundary.fields)
            if boundary.fields
            else "(none)"
        )
    )

    print(
        "Methods     : "
        + (
            ", ".join(boundary.methods)
            if boundary.methods
            else "(none)"
        )
    )

    print(
        "Properties  : "
        + (
            ", ".join(boundary.properties)
            if boundary.properties
            else "(none)"
        )
    )

    print()

    print("Consumers:")

    if boundary.consumers:
        for consumer in sorted(
            set(boundary.consumers)
        ):
            print(f"  - {consumer}")
    else:
        print("  (none detected)")

    print()


def print_comparison(
    boundaries: list[SourceBoundary],
) -> None:

    print("=" * 80)
    print("MONIER-WILLIAMS SOURCE BOUNDARY COMPARISON")
    print("=" * 80)
    print()

    for boundary in boundaries:
        print(
            f"{boundary.module}"
            f" -> {classify_boundary(boundary)}"
        )

    print()

    if len(boundaries) == 2:
        first, second = boundaries

        print("Architectural distinction:")
        print()

        print(
            f"  {first.module}"
        )
        print(
            "    = source identity / metadata"
        )
        print(
            "    = descriptive information"
        )
        print(
            "    = no raw-content acquisition contract"
        )
        print()

        print(
            f"  {second.module}"
        )
        print(
            "    = raw-content source abstraction"
        )
        print(
            "    = read()/acquire() contract"
        )
        print(
            "    = used by lexical acquisition"
        )
        print()

    print("=" * 80)


def main() -> None:

    print("=" * 80)
    print("SANSKRITAI — MONIER-WILLIAMS SOURCE BOUNDARY AUDIT")
    print("=" * 80)
    print()

    boundaries = locate_target_definitions()

    find_consumers(boundaries)

    print(
        f"Target definitions found: "
        f"{len(boundaries)}"
    )
    print()

    if not boundaries:
        print(
            "No Monier-Williams source definitions "
            "were found."
        )
        return

    for index, boundary in enumerate(
        boundaries,
        start=1,
    ):
        print_boundary(
            boundary,
            index,
        )

    print_comparison(boundaries)

    print()
    print("=" * 80)
    print("AUDIT COMPLETE — NO FILES WERE MODIFIED")
    print("=" * 80)


if __name__ == "__main__":
    main()

    
