from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGET_PREFIX = "acquisition.knowledge"

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
}


def is_historical(path: Path) -> bool:
    stem = path.stem

    if "_G" in stem:
        tail = stem.rsplit("_G", 1)[-1]

        if tail.isdigit():
            return True

    if stem and stem[-1].isdigit():
        return True

    return False


def production_files() -> list[Path]:

    result = []

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


def module_name(path: Path) -> str:

    relative = path.relative_to(ROOT)

    return ".".join(
        [
            "SanskritAI",
            *relative.with_suffix("").parts,
        ]
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


def layer(path: Path) -> str:

    relative = path.relative_to(ROOT)

    parts = relative.parts

    if "domain" in parts:
        return "DOMAIN"

    if "lexical" in parts:
        return "LEXICAL"

    if "acquisition" in parts:
        return "ACQUISITION"

    return "OTHER"


def main():

    print("=" * 78)
    print("CANONICAL KNOWLEDGE OWNERSHIP AUDIT")
    print("=" * 78)

    print(
        f"Target subsystem: {TARGET_PREFIX}"
    )

    print()

    consumers = {}

    for path in production_files():

        for module, symbol in imports(path):

            if (
                module == TARGET_PREFIX
                or module.startswith(
                    TARGET_PREFIX + "."
                )
            ):

                relative = str(
                    path.relative_to(ROOT)
                )

                consumers.setdefault(
                    relative,
                    [],
                ).append(
                    (
                        module,
                        symbol,
                    )
                )

    print("-" * 78)
    print("EXTERNAL PRODUCTION CONSUMERS")
    print("-" * 78)

    external = {}

    for path, records in consumers.items():

        if path.startswith(
            "acquisition/knowledge/"
        ):
            continue

        external[path] = records

    if external:

        for path in sorted(external):

            print()
            print(
                f"{layer(ROOT / path):12} {path}"
            )

            for module, symbol in external[path]:

                print(
                    f"    -> {module}.{symbol}"
                )

    else:

        print("NONE")

    print()
    print("-" * 78)
    print("CONSUMERS BY LAYER")
    print("-" * 78)

    counts = {}

    for path in external:

        current_layer = layer(
            ROOT / path
        )

        counts[current_layer] = (
            counts.get(current_layer, 0) + 1
        )

    for key in sorted(counts):

        print(
            f"{key:12}: {counts[key]}"
        )

    print()
    print("-" * 78)
    print("ARCHITECTURAL SIGNAL")
    print("-" * 78)

    domain_count = counts.get(
        "DOMAIN",
        0,
    )

    lexical_count = counts.get(
        "LEXICAL",
        0,
    )

    acquisition_count = counts.get(
        "ACQUISITION",
        0,
    )

    print(
        f"DOMAIN consumers      : {domain_count}"
    )

    print(
        f"LEXICAL consumers     : {lexical_count}"
    )

    print(
        f"ACQUISITION consumers  : {acquisition_count}"
    )

    print()

    if domain_count:

        print(
            "IMPORTANT:"
        )

        print(
            "The canonical knowledge subsystem has direct "
            "DOMAIN consumers."
        )

        print(
            "Before moving or duplicating models, determine "
            "whether acquisition.knowledge is actually an "
            "infrastructure layer or the canonical knowledge "
            "domain itself."
        )

        print(
            "No production refactor should be performed yet."
        )


if __name__ == "__main__":
    main()

