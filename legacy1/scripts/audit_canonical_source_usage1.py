from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGET_MODULE = (
    "acquisition.knowledge.models.canonical_source"
)

TARGET_SYMBOL = "CanonicalSource"


def is_historical(path: Path) -> bool:

    stem = path.stem

    if "_G" in stem:
        tail = stem.rsplit("_G", 1)[-1]

        if tail.isdigit():
            return True

    if stem and stem[-1].isdigit():
        return True

    return False


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


def find_consumers():

    consumers = []

    for path in ROOT.rglob("*.py"):

        if "tests" in path.parts:
            continue

        if is_historical(path):
            continue

        try:
            tree = ast.parse(
                path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            continue

        imported = False

        for node in ast.walk(tree):

            if isinstance(node, ast.ImportFrom):

                module = normalize(
                    node.module or ""
                )

                if (
                    module == TARGET_MODULE
                    and any(
                        alias.name == TARGET_SYMBOL
                        for alias in node.names
                    )
                ):
                    imported = True

            elif isinstance(node, ast.Import):

                for alias in node.names:

                    if normalize(alias.name) == TARGET_MODULE:
                        imported = True

        if imported:
            consumers.append(
                (path, tree)
            )

    return consumers


def classify_usage(
    tree: ast.AST,
) -> dict[str, int]:

    result = {
        "constructor": 0,
        "annotation": 0,
        "attribute": 0,
        "other": 0,
    }

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if (
                isinstance(node.func, ast.Name)
                and node.func.id == TARGET_SYMBOL
            ):
                result["constructor"] += 1
                continue

        if isinstance(node, ast.arg):

            if (
                isinstance(node.annotation, ast.Name)
                and node.annotation.id == TARGET_SYMBOL
            ):
                result["annotation"] += 1
                continue

        if isinstance(node, ast.AnnAssign):

            if (
                isinstance(node.annotation, ast.Name)
                and node.annotation.id == TARGET_SYMBOL
            ):
                result["annotation"] += 1
                continue

        if isinstance(node, ast.Attribute):

            if node.attr == TARGET_SYMBOL:
                result["attribute"] += 1
                continue

    return result


def main():

    consumers = find_consumers()

    print("=" * 78)
    print("CANONICALSOURCE USAGE AUDIT")
    print("=" * 78)

    print(
        f"Target: {TARGET_MODULE}.{TARGET_SYMBOL}"
    )

    print()

    if not consumers:

        print("No production consumers detected.")

        return

    total = {
        "constructor": 0,
        "annotation": 0,
        "attribute": 0,
        "other": 0,
    }

    for path, tree in consumers:

        usage = classify_usage(tree)

        print("-" * 78)

        print(
            path.relative_to(ROOT)
        )

        print(
            f"  constructors : {usage['constructor']}"
        )

        print(
            f"  annotations  : {usage['annotation']}"
        )

        print(
            f"  attributes   : {usage['attribute']}"
        )

        for key in total:
            total[key] += usage[key]

    print()
    print("-" * 78)
    print("TOTAL USAGE SIGNALS")
    print("-" * 78)

    for key, value in total.items():

        print(
            f"{key:14}: {value}"
        )

    print()
    print("-" * 78)
    print("INTERPRETATION")
    print("-" * 78)

    if total["constructor"]:

        print(
            "CanonicalSource is actively constructed."
        )

    elif total["annotation"]:

        print(
            "CanonicalSource appears primarily as a type contract."
        )

    else:

        print(
            "CanonicalSource is imported but no simple direct "
            "constructor/type-annotation usage was detected."
        )


if __name__ == "__main__":
    main()
