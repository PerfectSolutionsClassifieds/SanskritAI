from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

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


def production_files():

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

            result.append(module)

        elif isinstance(node, ast.Import):

            for alias in node.names:

                result.append(
                    normalize(alias.name)
                )

    return result


def classify(module: str) -> str:

    if module == "domain" or module.startswith(
        "domain."
    ):
        return "DOMAIN"

    if module == "lexical" or module.startswith(
        "lexical."
    ):
        return "LEXICAL"

    if module == "acquisition" or module.startswith(
        "acquisition."
    ):
        return "ACQUISITION"

    if module == "analysis" or module.startswith(
        "analysis."
    ):
        return "ANALYSIS"

    if module == "pipeline" or module.startswith(
        "pipeline."
    ):
        return "PIPELINE"

    return "OTHER"


def main():

    print("=" * 78)
    print("KNOWLEDGE LAYER DEPENDENCY AUDIT")
    print("=" * 78)

    edges = {}

    for path in production_files():

        source_layer = classify(
            module_name(path)
            .removeprefix("SanskritAI.")
        )

        for imported in imports(path):

            target_layer = classify(imported)

            if target_layer == "OTHER":
                continue

            if source_layer == target_layer:
                continue

            key = (
                source_layer,
                target_layer,
            )

            edges.setdefault(
                key,
                [],
            ).append(
                (
                    path.relative_to(ROOT),
                    imported,
                )
            )

    print()
    print("-" * 78)
    print("CROSS-LAYER DEPENDENCY MATRIX")
    print("-" * 78)

    for (source, target), records in sorted(edges.items()):

        print()
        print(
            f"{source} -> {target}: {len(records)}"
        )

        for path, imported in records:

            print(
                f"  {path} -> {imported}"
            )

    print()
    print("-" * 78)
    print("FOCUS: DOMAIN -> ACQUISITION")
    print("-" * 78)

    domain_acquisition = edges.get(
        ("DOMAIN", "ACQUISITION"),
        [],
    )

    print(
        f"Count: {len(domain_acquisition)}"
    )

    print()

    for path, imported in domain_acquisition:

        print(
            f"{path} -> {imported}"
        )

    print()
    print("-" * 78)
    print("ARCHITECTURAL INTERPRETATION")
    print("-" * 78)

    if domain_acquisition:

        print(
            "DOMAIN -> ACQUISITION is an established "
            "production dependency."
        )

        print(
            "Do not remove it mechanically."
        )

        print(
            "Next decision requires semantic ownership "
            "of acquisition.knowledge."
        )

    else:

        print(
            "No DOMAIN -> ACQUISITION dependency detected."
        )


if __name__ == "__main__":
    main()
