from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
}

HISTORICAL_SUFFIXES = tuple(str(i) for i in range(1, 100))


def is_historical(path: Path) -> bool:
    name = path.name

    if not name.endswith(".py"):
        return True

    stem = path.stem

    if "_G" in stem:
        tail = stem.rsplit("_G", 1)[-1]
        if tail.isdigit():
            return True

    for suffix in HISTORICAL_SUFFIXES:
        if stem.endswith(suffix):
            return True

    return False


def python_files() -> list[Path]:
    files = []

    for path in ROOT.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue

        if is_historical(path):
            continue

        files.append(path)

    return sorted(files)


def imported_names(path: Path) -> list[tuple[str, str]]:
    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except Exception:
        return []

    result: list[tuple[str, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                result.append((module, alias.name))

        elif isinstance(node, ast.Import):
            for alias in node.names:
                result.append((alias.name, "*"))

    return result


def classify(path: Path) -> str:
    relative = path.relative_to(ROOT)

    if "tests" in relative.parts:
        return "TEST"

    return "PRODUCTION"


def main() -> None:
    domain_module = "domain.lexical.lexical_source"
    kernel_module = "lexical.models.lexical_source"

    domain_users: list[Path] = []
    kernel_users: list[Path] = []

    for path in python_files():
        for module, name in imported_names(path):
            if module == domain_module and name == "LexicalSource":
                domain_users.append(path)

            if module == kernel_module and name == "LexicalSource":
                kernel_users.append(path)

    print("=" * 78)
    print("LEXICALSOURCE OWNERSHIP AUDIT")
    print("=" * 78)
    print(f"Repository: {ROOT}")
    print()
    print("Historical numbered Python files are excluded.")
    print("Generated _G<number>.py files are excluded.")
    print()

    print("-" * 78)
    print("DOMAIN LEXICALSOURCE CONSUMERS")
    print("-" * 78)

    for path in sorted(set(domain_users)):
        print(f"  [{classify(path):10}] {path.relative_to(ROOT)}")

    print()
    print("-" * 78)
    print("KERNEL LEXICALSOURCE CONSUMERS")
    print("-" * 78)

    for path in sorted(set(kernel_users)):
        print(f"  [{classify(path):10}] {path.relative_to(ROOT)}")

    print()
    print("-" * 78)
    print("OWNERSHIP SUMMARY")
    print("-" * 78)

    print(
        f"Domain LexicalSource users : {len(set(domain_users))}"
    )

    print(
        f"Kernel LexicalSource users : {len(set(kernel_users))}"
    )

    print()
    print("ARCHITECTURAL DECISION")
    print("-" * 78)

    if domain_users and kernel_users:
        print("RETAIN BOTH")
        print()
        print(
            "Both representations have independent production consumers."
        )
        print(
            "No consolidation is justified by current ownership evidence."
        )
    elif domain_users:
        print("DOMAIN-OWNED REPRESENTATION")
    elif kernel_users:
        print("KERNEL-OWNED REPRESENTATION")
    else:
        print("NO PRODUCTION OWNERSHIP DETECTED")


if __name__ == "__main__":
    main()
