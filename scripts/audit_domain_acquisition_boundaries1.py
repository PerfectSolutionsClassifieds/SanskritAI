from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
}

TARGET_PREFIX = "acquisition"


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
    result = []

    for path in ROOT.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue

        if "tests" in path.parts:
            continue

        if is_historical(path):
            continue

        result.append(path)

    return sorted(result)


def module_imports(path: Path) -> list[tuple[str, str]]:
    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except Exception:
        return []

    result = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                result.append((module, alias.name))

        elif isinstance(node, ast.Import):
            result.append((alias.name, "*") for alias in node.names)

    return result


def main() -> None:
    print("=" * 78)
    print("DOMAIN -> ACQUISITION BOUNDARY AUDIT")
    print("=" * 78)
    print(f"Repository: {ROOT}")
    print()
    print("Purpose:")
    print(
        "Inspect production dependencies from domain/* into acquisition/*."
    )
    print()
    print(
        "This audit does NOT propose a refactor."
    )
    print(
        "It only identifies whether the dependency is intentional,"
    )
    print(
        "adapter-mediated, or potentially inverted."
    )
    print()

    findings = []

    for path in production_python_files():
        relative = path.relative_to(ROOT)

        if "domain" not in relative.parts:
            continue

        for module, name in module_imports(path):
            if module == "acquisition" or module.startswith(
                TARGET_PREFIX + "."
            ):
                findings.append(
                    (relative, module, name)
                )

    print("-" * 78)
    print("CROSS-LAYER IMPORTS")
    print("-" * 78)

    if not findings:
        print("No DOMAIN -> ACQUISITION imports detected.")
        return

    for path, module, name in findings:
        print()
        print(f"FILE   : {path}")
        print(f"IMPORT : {module}")
        print(f"SYMBOL : {name}")

    print()
    print("-" * 78)
    print("ARCHITECTURAL REVIEW SIGNAL")
    print("-" * 78)

    print(
        f"DOMAIN -> ACQUISITION imports detected: {len(findings)}"
    )
    print()
    print(
        "These dependencies require semantic ownership review."
    )
    print(
        "Do NOT introduce a new abstraction until each dependency"
    )
    print(
        "has been classified as intentional or architecturally inverted."
    )


if __name__ == "__main__":
    main()
