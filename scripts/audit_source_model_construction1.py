
"""
SanskritAI — Source Model Construction / Type Usage Audit

Purpose
-------
Determine how production code actually uses the source models.

For each target source model, detect:

1. Constructor calls:
       CorpusSource(...)
       CanonicalSource(...)
       LexicalSource(...)
       MonierWilliamsSource(...)

2. Type annotations:
       source: CorpusSource
       -> CorpusSource

3. Attribute/class references.

4. Import locations.

Tests are excluded.

This is a READ-ONLY architectural audit.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


PROJECT_ROOT = Path("/content/SanskritAI")

TARGETS = {
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


@dataclass
class Usage:
    model: str
    file: Path
    module: str
    line: int
    usage_type: str
    context: str


def module_name(path: Path) -> str:

    relative = path.relative_to(PROJECT_ROOT)

    parts = list(relative.with_suffix("").parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]

    return ".".join(parts)


def excluded(path: Path) -> bool:

    return any(
        part in EXCLUDED_PARTS
        for part in path.parts
    )


def annotation_contains_target(
    node: ast.AST,
    targets: set[str],
) -> str | None:

    for child in ast.walk(node):

        if isinstance(child, ast.Name):

            if child.id in targets:
                return child.id

        elif isinstance(child, ast.Attribute):

            if child.attr in targets:
                return child.attr

    return None


def scan_file(
    path: Path,
) -> list[Usage]:

    results: list[Usage] = []

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
        return results

    module = module_name(path)

    imported_names: set[str] = set()

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):

            for alias in node.names:

                if alias.name in TARGETS:

                    imported_names.add(
                        alias.asname
                        or alias.name
                    )

        elif isinstance(node, ast.Import):

            for alias in node.names:

                if alias.name in TARGETS:

                    imported_names.add(
                        alias.asname
                        or alias.name
                    )

    for node in ast.walk(tree):

        # -------------------------------------------------
        # Constructor calls
        # -------------------------------------------------

        if isinstance(node, ast.Call):

            target = None

            if isinstance(node.func, ast.Name):

                if node.func.id in TARGETS:
                    target = node.func.id

                elif node.func.id in imported_names:
                    target = node.func.id

            elif isinstance(node.func, ast.Attribute):

                if node.func.attr in TARGETS:
                    target = node.func.attr

            if target:

                results.append(
                    Usage(
                        model=target,
                        file=path,
                        module=module,
                        line=node.lineno,
                        usage_type="CONSTRUCTOR_CALL",
                        context=ast.unparse(node),
                    )
                )

        # -------------------------------------------------
        # Type annotations
        # -------------------------------------------------

        if isinstance(
            node,
            (
                ast.AnnAssign,
                ast.arg,
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):

            annotation = None

            if isinstance(
                node,
                ast.AnnAssign,
            ):
                annotation = node.annotation

            elif isinstance(
                node,
                ast.arg,
            ):
                annotation = node.annotation

            elif isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                annotation = node.returns

            if annotation is not None:

                target = annotation_contains_target(
                    annotation,
                    TARGETS,
                )

                if target:

                    results.append(
                        Usage(
                            model=target,
                            file=path,
                            module=module,
                            line=node.lineno,
                            usage_type="TYPE_ANNOTATION",
                            context=ast.unparse(annotation),
                        )
                    )

        # -------------------------------------------------
        # Direct class references
        # -------------------------------------------------

        if isinstance(node, ast.Name):

            if node.id in TARGETS:

                results.append(
                    Usage(
                        model=node.id,
                        file=path,
                        module=module,
                        line=node.lineno,
                        usage_type="CLASS_REFERENCE",
                        context=node.id,
                    )
                )

    return results


def scan() -> list[Usage]:

    results: list[Usage] = []

    for path in PROJECT_ROOT.rglob("*.py"):

        if excluded(path):
            continue

        results.extend(
            scan_file(path)
        )

    return results


def print_report(
    usages: list[Usage],
) -> None:

    print("=" * 80)
    print(
        "SANSKRITAI — SOURCE MODEL "
        "CONSTRUCTION / TYPE USAGE AUDIT"
    )
    print("=" * 80)
    print()

    for model in sorted(TARGETS):

        print("-" * 80)
        print(model)
        print("-" * 80)

        model_usages = [
            usage
            for usage in usages
            if usage.model == model
        ]

        if not model_usages:

            print(
                "  <no production usage detected>"
            )
            print()
            continue

        grouped: dict[str, list[Usage]] = {}

        for usage in model_usages:

            key = (
                f"{usage.module}"
                f"::{usage.usage_type}"
            )

            grouped.setdefault(
                key,
                [],
            ).append(usage)

        for key in sorted(grouped):

            print()
            print(f"  {key}")

            for usage in sorted(
                grouped[key],
                key=lambda item: item.line,
            ):

                print(
                    f"    line {usage.line:4d}"
                    f" : {usage.context}"
                )

        print()

    print("=" * 80)
    print("USAGE COUNTS")
    print("=" * 80)

    for model in sorted(TARGETS):

        model_usages = [
            usage
            for usage in usages
            if usage.model == model
        ]

        constructor_count = sum(
            usage.usage_type
            == "CONSTRUCTOR_CALL"
            for usage in model_usages
        )

        annotation_count = sum(
            usage.usage_type
            == "TYPE_ANNOTATION"
            for usage in model_usages
        )

        reference_count = sum(
            usage.usage_type
            == "CLASS_REFERENCE"
            for usage in model_usages
        )

        print()
        print(model)
        print(
            f"  constructor calls : "
            f"{constructor_count}"
        )
        print(
            f"  type annotations  : "
            f"{annotation_count}"
        )
        print(
            f"  class references  : "
            f"{reference_count}"
        )

    print()
    print("=" * 80)
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 80)


def main() -> None:

    usages = scan()

    print_report(usages)


if __name__ == "__main__":
    main()
