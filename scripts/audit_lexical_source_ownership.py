from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

PACKAGE_NAME = "SanskritAI"

DOMAIN_MODULE = "domain.lexical.lexical_source"
KERNEL_MODULE = "lexical.models.lexical_source"

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
}


# ---------------------------------------------------------------------------
# FILE FILTERING
# ---------------------------------------------------------------------------

def is_historical(path: Path) -> bool:
    """
    Exclude historical numbered files.

    Examples:
        foo1.py
        foo2.py
        monier_williams_mapper4.py
        test_lexical_source12.py

    Also exclude:
        *_G<number>.py
    """

    stem = path.stem

    if "_G" in stem:
        suffix = stem.rsplit("_G", 1)[-1]
        if suffix.isdigit():
            return True

    if stem and stem[-1].isdigit():
        return True

    return False


def python_files() -> list[Path]:
    result: list[Path] = []

    for path in ROOT.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue

        if is_historical(path):
            continue

        result.append(path)

    return sorted(result)


def is_test(path: Path) -> bool:
    return "tests" in path.relative_to(ROOT).parts


def is_production(path: Path) -> bool:
    return not is_test(path)


# ---------------------------------------------------------------------------
# MODULE RESOLUTION
# ---------------------------------------------------------------------------

def module_name_from_path(path: Path) -> str:
    """
    Convert repository path into the logical SanskritAI module name.

    /content/SanskritAI/domain/lexical/foo.py
        ->
    SanskritAI.domain.lexical.foo
    """

    relative = path.relative_to(ROOT)

    parts = list(relative.with_suffix("").parts)

    return ".".join([PACKAGE_NAME, *parts])


def normalize_import_module(module: str) -> str:
    """
    Normalize both:

        SanskritAI.lexical.models.lexical_source
        lexical.models.lexical_source

    into:

        lexical.models.lexical_source
    """

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
    """
    Resolve Python relative imports.

    Example:

        current:
            SanskritAI.domain.lexical.foo

        from .lexical_source import LexicalSource

    becomes:

        domain.lexical.lexical_source
    """

    current_parts = current_module.split(".")

    # Remove the current module itself.
    package_parts = current_parts[:-1]

    if level > len(package_parts):
        return imported_module or ""

    base_parts = package_parts[: len(package_parts) - level + 1]

    if imported_module:
        base_parts.extend(imported_module.split("."))

    return ".".join(base_parts)


# ---------------------------------------------------------------------------
# IMPORT EXTRACTION
# ---------------------------------------------------------------------------

def imported_symbols(path: Path) -> list[tuple[str, str]]:
    """
    Return resolved:

        (module, symbol)

    pairs.
    """

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
                    current_module=current_module,
                    imported_module=node.module,
                    level=node.level,
                )

            module = normalize_import_module(module)

            for alias in node.names:
                result.append((module, alias.name))

        elif isinstance(node, ast.Import):

            for alias in node.names:
                module = normalize_import_module(alias.name)
                result.append((module, "*"))

    return result


# ---------------------------------------------------------------------------
# TARGET MATCHING
# ---------------------------------------------------------------------------

def matches_target(
    module: str,
    symbol: str,
    target_module: str,
) -> bool:

    return (
        module == target_module
        and symbol == "LexicalSource"
    )


# ---------------------------------------------------------------------------
# AUDIT
# ---------------------------------------------------------------------------

def main() -> None:

    files = python_files()

    domain_users: list[Path] = []
    kernel_users: list[Path] = []

    for path in files:

        for module, symbol in imported_symbols(path):

            if matches_target(
                module,
                symbol,
                DOMAIN_MODULE,
            ):
                domain_users.append(path)

            if matches_target(
                module,
                symbol,
                KERNEL_MODULE,
            ):
                kernel_users.append(path)

    domain_users = sorted(set(domain_users))
    kernel_users = sorted(set(kernel_users))

    domain_production = [
        path for path in domain_users
        if is_production(path)
    ]

    kernel_production = [
        path for path in kernel_users
        if is_production(path)
    ]

    domain_tests = [
        path for path in domain_users
        if is_test(path)
    ]

    kernel_tests = [
        path for path in kernel_users
        if is_test(path)
    ]

    print("=" * 78)
    print("LEXICALSOURCE OWNERSHIP AUDIT")
    print("=" * 78)

    print(f"Repository: {ROOT}")
    print(f"Python files scanned: {len(files)}")
    print()

    print("Historical numbered Python files are excluded.")
    print("Generated _G<number>.py files are excluded.")
    print()

    print("-" * 78)
    print("DOMAIN LEXICALSOURCE")
    print("-" * 78)

    print(f"Definition:")
    print(f"  {DOMAIN_MODULE}")
    print()

    print("Production consumers:")

    if domain_production:
        for path in domain_production:
            print(
                f"  {path.relative_to(ROOT)}"
            )
    else:
        print("  NONE")

    print()
    print("Test consumers:")

    if domain_tests:
        for path in domain_tests:
            print(
                f"  {path.relative_to(ROOT)}"
            )
    else:
        print("  NONE")

    print()
    print("-" * 78)
    print("KERNEL LEXICALSOURCE")
    print("-" * 78)

    print(f"Definition:")
    print(f"  {KERNEL_MODULE}")
    print()

    print("Production consumers:")

    if kernel_production:
        for path in kernel_production:
            print(
                f"  {path.relative_to(ROOT)}"
            )
    else:
        print("  NONE")

    print()
    print("Test consumers:")

    if kernel_tests:
        for path in kernel_tests:
            print(
                f"  {path.relative_to(ROOT)}"
            )
    else:
        print("  NONE")

    print()
    print("-" * 78)
    print("OWNERSHIP SUMMARY")
    print("-" * 78)

    print(
        f"Domain production users : {len(domain_production)}"
    )

    print(
        f"Domain test users       : {len(domain_tests)}"
    )

    print(
        f"Kernel production users : {len(kernel_production)}"
    )

    print(
        f"Kernel test users       : {len(kernel_tests)}"
    )

    print()
    print("-" * 78)
    print("ARCHITECTURAL DECISION")
    print("-" * 78)

    if domain_production and kernel_production:

        print("RETAIN BOTH")
        print()
        print(
            "Both LexicalSource representations have "
            "independent production ownership."
        )
        print(
            "No consolidation is justified by ownership evidence."
        )

    elif domain_production:

        print("DOMAIN OWNED")
        print()
        print(
            "Only the domain representation currently has "
            "production ownership."
        )

    elif kernel_production:

        print("KERNEL OWNED")
        print()
        print(
            "Only the kernel representation currently has "
            "production ownership."
        )

    else:

        print("NO PRODUCTION OWNERSHIP DETECTED")

        print()
        print(
            "WARNING: this result should be treated as a possible "
            "import-resolution failure before making architecture decisions."
        )


if __name__ == "__main__":
    main()
