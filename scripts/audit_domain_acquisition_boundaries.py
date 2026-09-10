from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

PACKAGE_NAME = "SanskritAI"

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
        suffix = stem.rsplit("_G", 1)[-1]

        if suffix.isdigit():
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

    parts = list(
        relative.with_suffix("").parts
    )

    return ".".join(
        [PACKAGE_NAME, *parts]
    )


def normalize_module(module: str) -> str:

    prefix = PACKAGE_NAME + "."

    if module == PACKAGE_NAME:
        return ""

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

    if level > len(package_parts):
        return imported_module or ""

    base_parts = package_parts[
        : len(package_parts) - level + 1
    ]

    if imported_module:
        base_parts.extend(
            imported_module.split(".")
        )

    return ".".join(base_parts)


# ---------------------------------------------------------------------------
# IMPORT EXTRACTION
# ---------------------------------------------------------------------------

def imports_for_file(
    path: Path,
) -> list[tuple[str, str]]:

    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except Exception:
        return []

    current_module = module_name_from_path(path)

    result: list[tuple[str, str]] = []

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

            for alias in node.names:

                result.append(
                    (module, alias.name)
                )

        elif isinstance(node, ast.Import):

            for alias in node.names:

                module = normalize_module(
                    alias.name
                )

                result.append(
                    (module, "*")
                )

    return result


# ---------------------------------------------------------------------------
# AUDIT
# ---------------------------------------------------------------------------

def main() -> None:

    files = production_python_files()

    findings = []

    for path in files:

        relative = path.relative_to(ROOT)

        if "domain" not in relative.parts:
            continue

        for module, symbol in imports_for_file(path):

            if (
                module == "acquisition"
                or module.startswith("acquisition.")
            ):

                findings.append(
                    (
                        path,
                        module,
                        symbol,
                    )
                )

    print("=" * 78)
    print("DOMAIN -> ACQUISITION BOUNDARY AUDIT")
    print("=" * 78)

    print(f"Repository: {ROOT}")
    print(
        f"Production Python files scanned: {len(files)}"
    )
    print()

    print("Historical numbered Python files are excluded.")
    print("Generated _G<number>.py files are excluded.")
    print("Tests are excluded.")
    print()

    print("-" * 78)
    print("DOMAIN -> ACQUISITION IMPORTS")
    print("-" * 78)

    if not findings:

        print(
            "No DOMAIN -> ACQUISITION imports detected."
        )

        print()
        print(
            "This is a valid result only after package-aware "
            "import resolution has been verified."
        )

        return

    for path, module, symbol in findings:

        print()

        print(
            f"FILE   : {path.relative_to(ROOT)}"
        )

        print(
            f"IMPORT : {module}"
        )

        print(
            f"SYMBOL : {symbol}"
        )

    print()
    print("-" * 78)
    print("SUMMARY")
    print("-" * 78)

    print(
        f"DOMAIN -> ACQUISITION imports: {len(findings)}"
    )

    print()
    print("-" * 78)
    print("ARCHITECTURAL REVIEW")
    print("-" * 78)

    print(
        "These dependencies must be reviewed individually."
    )

    print(
        "Do not automatically invert or remove them."
    )

    print(
        "First classify each dependency by semantic ownership."
    )


if __name__ == "__main__":
    main()
