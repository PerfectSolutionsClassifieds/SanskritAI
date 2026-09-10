
"""
SanskritAI — Source Model Construction / Type Usage Audit

Purpose
-------
Determine how ACTIVE production code uses source models.

Detect:
    - constructor calls
    - type annotations
    - class references

Excluded:
    - tests
    - scripts
    - cache directories
    - historical numbered copies (*1.py, *2.py, ...)
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
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

NUMBERED_COPY_PATTERN = re.compile(r".*\d+$")


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

    if any(
        part in EXCLUDED_PARTS
        for part in path.parts
    ):
        return True

    if NUMBERED_COPY_PATTERN.match(path.stem):
        return True

    return False


def annotation_targets(
    node: ast.AST,
) -> set[str]:

    found: set[str] = set()

    for child in ast.walk(node):

        if isinstance(child, ast.Name):

            if child.id in TARGETS:
                found.add(child.id)

        elif isinstance(
            child,
            ast.Attribute,
        ):

            if child.attr in TARGETS:
                found.add(child.attr)

    return found


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

    for node in ast.walk(tree):

        # -------------------------------------------------
        # Constructor calls
        # -------------------------------------------------

        if isinstance(node, ast.Call):

            target = None

            if isinstance(
                node.func,
                ast.Name,
            ):

                if node.func.id in TARGETS:
                    target = node.func.id

            elif isinstance(
                node.func,
                ast.Attribute,
            ):

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

            targets = annotation_targets(
                annotation
            )

            for target in sorted(targets):

                results.append(
                    Usage(
                        model=target,
                        file=path,
                        module=module,
                        line=node.lineno,
                        usage_type="TYPE_ANNOTATION",
                        context=ast.unparse(
                            annotation
                        ),
                    )
                )

        # -------------------------------------------------
        # Class references
        # -------------------------------------------------

        if isinstance(
            node,
            ast.Name,
        ):

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
        "SANSKRITAI — ACTIVE SOURCE MODEL "
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
                "  <no active production usage detected>"
            )
            print()
            continue

        grouped: dict[
            tuple[str, str],
            list[Usage],
        ] = {}

        for usage in model_usages:

            key = (
                usage.module,
                usage.usage_type,
            )

            grouped.setdefault(
                key,
                [],
            ).append(usage)

        for (
            module,
            usage_type,
        ) in sorted(grouped):

            print()
            print(
                f"  {module}::{usage_type}"
            )

            for usage in sorted(
                grouped[
                    (module, usage_type)
                ],
                key=lambda item: item.line,
            ):

                print(
                    f"    line {usage.line:4d}"
                    f" : {usage.context}"
                )

        print()

    print("=" * 80)
    print("ACTIVE USAGE COUNTS")
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

    usages = scan()

    print_report(usages)


if __name__ == "__main__":
    main()
