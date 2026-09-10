from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGET_MODULE = (
    "acquisition.knowledge.models.canonical_source"
)

TARGET_SYMBOL = "CanonicalSource"

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
}


# ---------------------------------------------------------------------------
# FILE FILTERING
# ---------------------------------------------------------------------------

def is_historical(path: Path) -> bool:
    stem = path.stem

    if "_G" in stem:
        tail = stem.rsplit("_G", 1)[-1]
        if tail.isdigit():
            return True

    if stem and stem[-1].isdigit():
        return True

    return False


def production_python_files() -> list[Path]:
    result: list[Path] = []

    for path in ROOT.rglob("*.py"):

        if any(
            part in EXCLUDED_DIRS
            for part in path.parts
        ):
            continue

        if "tests" in path.parts:
            continue

        if is_historical(path):
            continue

        result.append(path)

    return sorted(result)


# ---------------------------------------------------------------------------
# MODULE RESOLUTION
# ---------------------------------------------------------------------------

def module_name_from_path(path: Path) -> str:
    relative = path.relative_to(ROOT)

    return ".".join(
        [
            "SanskritAI",
            *relative.with_suffix("").parts,
        ]
    )


def normalize_module(module: str) -> str:
    prefix = "SanskritAI."

    if module.startswith(prefix):
        return module[len(prefix):]

    return module


def resolve_relative_import(
    current_module: str,
    imported_module: str | None,
    level: int,
) -> str:

    current_parts = current_module.split(".")
    package_parts = current_parts[:-1]

    base = package_parts[
        : len(package_parts) - level + 1
    ]

    if imported_module:
        base.extend(imported_module.split("."))

    return ".".join(base)


# ---------------------------------------------------------------------------
# IMPORT BINDINGS
# ---------------------------------------------------------------------------

def target_bindings(
    tree: ast.AST,
    current_module: str,
) -> dict[str, str]:

    bindings: dict[str, str] = {}

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):

            module = node.module or ""

            if node.level:
                module = resolve_relative_import(
                    current_module,
                    node.module,
                    node.level,
                )

            module = normalize_module(module)

            if module != TARGET_MODULE:
                continue

            for alias in node.names:

                if alias.name == TARGET_SYMBOL:

                    local_name = (
                        alias.asname
                        or alias.name
                    )

                    bindings[local_name] = (
                        f"{module}.{alias.name}"
                    )

        elif isinstance(node, ast.Import):

            for alias in node.names:

                normalized = normalize_module(
                    alias.name
                )

                if normalized == TARGET_MODULE:

                    local_name = (
                        alias.asname
                        or alias.name.split(".")[0]
                    )

                    bindings[local_name] = (
                        normalized
                    )

    return bindings


# ---------------------------------------------------------------------------
# AST USAGE ANALYSIS
# ---------------------------------------------------------------------------

class UsageVisitor(ast.NodeVisitor):

    def __init__(
        self,
        bindings: dict[str, str],
    ) -> None:

        self.bindings = bindings

        self.constructors = 0
        self.annotations = 0
        self.returns = 0
        self.parameters = 0
        self.assignments = 0
        self.attributes = 0
        self.other = 0

    def _matches_name(
        self,
        node: ast.AST,
    ) -> bool:

        return (
            isinstance(node, ast.Name)
            and node.id in self.bindings
        )

    def _matches_attribute(
        self,
        node: ast.AST,
    ) -> bool:

        if not isinstance(node, ast.Attribute):
            return False

        return (
            isinstance(node.value, ast.Name)
            and node.value.id in self.bindings
        )

    def visit_Call(
        self,
        node: ast.Call,
    ) -> None:

        if self._matches_name(node.func):
            self.constructors += 1

        elif self._matches_attribute(node.func):
            self.constructors += 1

        self.generic_visit(node)

    def visit_AnnAssign(
        self,
        node: ast.AnnAssign,
    ) -> None:

        if self._matches_name(node.annotation):
            self.annotations += 1

        self.generic_visit(node)

    def visit_arg(
        self,
        node: ast.arg,
    ) -> None:

        if node.annotation and self._matches_name(
            node.annotation
        ):
            self.parameters += 1

        self.generic_visit(node)

    def visit_Return(
        self,
        node: ast.Return,
    ) -> None:

        if node.value and self._matches_name(
            node.value
        ):
            self.returns += 1

        self.generic_visit(node)

    def visit_Assign(
        self,
        node: ast.Assign,
    ) -> None:

        for target in node.targets:

            if self._matches_name(target):
                self.assignments += 1

        self.generic_visit(node)

    def visit_Attribute(
        self,
        node: ast.Attribute,
    ) -> None:

        if self._matches_attribute(node):
            self.attributes += 1

        self.generic_visit(node)


# ---------------------------------------------------------------------------
# AUDIT
# ---------------------------------------------------------------------------

def main() -> None:

    print("=" * 78)
    print("CANONICALSOURCE USAGE AUDIT")
    print("=" * 78)

    print(
        f"Target: {TARGET_MODULE}.{TARGET_SYMBOL}"
    )

    print()

    total_consumers = 0

    totals = {
        "constructors": 0,
        "annotations": 0,
        "parameters": 0,
        "returns": 0,
        "assignments": 0,
        "attributes": 0,
        "other": 0,
    }

    for path in production_python_files():

        try:
            source = path.read_text(
                encoding="utf-8"
            )

            tree = ast.parse(
                source,
                filename=str(path),
            )

        except Exception:
            continue

        current_module = module_name_from_path(path)

        bindings = target_bindings(
            tree,
            current_module,
        )

        if not bindings:
            continue

        total_consumers += 1

        visitor = UsageVisitor(bindings)
        visitor.visit(tree)

        usage = {
            "constructors": visitor.constructors,
            "annotations": visitor.annotations,
            "parameters": visitor.parameters,
            "returns": visitor.returns,
            "assignments": visitor.assignments,
            "attributes": visitor.attributes,
            "other": visitor.other,
        }

        print("-" * 78)
        print(
            path.relative_to(ROOT)
        )

        print(
            f"  bindings    : {', '.join(bindings)}"
        )

        for key, value in usage.items():

            if value:
                print(
                    f"  {key:12}: {value}"
                )

            totals[key] += value

    print()
    print("-" * 78)
    print("SUMMARY")
    print("-" * 78)

    print(
        f"Production consumers: {total_consumers}"
    )

    for key, value in totals.items():

        print(
            f"{key:16}: {value}"
        )

    print()
    print("-" * 78)
    print("INTERPRETATION")
    print("-" * 78)

    if total_consumers:

        print(
            "CanonicalSource has verified production consumers."
        )

        if totals["constructors"]:
            print(
                "At least one production path constructs CanonicalSource."
            )

        if totals["annotations"]:
            print(
                "CanonicalSource participates in type annotations."
            )

        if totals["parameters"]:
            print(
                "CanonicalSource participates in function parameters."
            )

        if totals["returns"]:
            print(
                "CanonicalSource participates in return contracts."
            )

    else:

        print(
            "No verified production consumers detected."
        )


if __name__ == "__main__":
    main()
