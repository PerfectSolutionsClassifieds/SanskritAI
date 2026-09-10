from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGET_MODULE = (
    "acquisition.knowledge.models.canonical_source"
)

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
}


def is_historical(path: Path) -> bool:

    stem = path.stem

    if "_G" in stem:
        suffix = stem.rsplit("_G", 1)[-1]

        if suffix.isdigit():
            return True

    if stem and stem[-1].isdigit():
        return True

    return False


def python_files():

    result = []

    for path in ROOT.rglob("*.py"):

        if any(
            part in EXCLUDED_DIRS
            for part in path.parts
        ):
            continue

        if is_historical(path):
            continue

        result.append(path)

    return sorted(result)


def module_name(path: Path) -> str:

    relative = path.relative_to(ROOT)

    return ".".join(
        ["SanskritAI", *relative.with_suffix("").parts]
    )


def normalize(module: str) -> str:

    prefix = "SanskritAI."

    if module.startswith(prefix):
        return module[len(prefix):]

    return module


def imports(path: Path):

    try:
        tree = ast.parse(
            path.read_text(
                encoding="utf-8"
            )
        )
    except Exception:
        return []

    current = module_name(path)
    current_parts = current.split(".")

    result = []

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):

            module = node.module or ""

            if node.level:

                package_parts = current_parts[:-1]

                base = package_parts[
                    :len(package_parts) - node.level + 1
                ]

                if node.module:
                    base.extend(
                        node.module.split(".")
                    )

                module = ".".join(base)

            module = normalize(module)

            for alias in node.names:

                result.append(
                    (
                        module,
                        alias.name,
                    )
                )

        elif isinstance(node, ast.Import):

            for alias in node.names:

                result.append(
                    (
                        normalize(alias.name),
                        "*",
                    )
                )

    return result


def main():

    production = []
    tests = []

    for path in python_files():

        found = False

        for module, symbol in imports(path):

            if module == TARGET_MODULE:

                found = True

                record = (
                    path,
                    module,
                    symbol,
                )

                if "tests" in path.parts:
                    tests.append(record)
                else:
                    production.append(record)

        if found:
            pass

    print("=" * 78)
    print("CANONICALSOURCE OWNERSHIP AUDIT")
    print("=" * 78)

    print(
        f"Target: {TARGET_MODULE}"
    )

    print()

    print("-" * 78)
    print("PRODUCTION CONSUMERS")
    print("-" * 78)

    if production:

        for path, module, symbol in production:

            print(
                f"{path.relative_to(ROOT)}"
            )

            print(
                f"  symbol: {symbol}"
            )

    else:
        print("NONE")

    print()

    print("-" * 78)
    print("TEST CONSUMERS")
    print("-" * 78)

    if tests:

        for path, module, symbol in tests:

            print(
                f"{path.relative_to(ROOT)}"
            )

            print(
                f"  symbol: {symbol}"
            )

    else:
        print("NONE")

    print()

    print("-" * 78)
    print("SUMMARY")
    print("-" * 78)

    print(
        f"Production consumers: {len(production)}"
    )

    print(
        f"Test consumers      : {len(tests)}"
    )

    print()

    if production:

        print(
            "CanonicalSource has active production ownership."
        )

        print(
            "Next step: inspect each consumer's semantic use."
        )

    else:

        print(
            "No production ownership detected."
        )


if __name__ == "__main__":
    main()
