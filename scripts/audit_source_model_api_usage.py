from __future__ import annotations

import ast
from pathlib import Path
from collections import defaultdict


ROOT = Path("/content/SanskritAI")

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
    "sanskritai.egg-info",
    "tests",
}


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_PARTS for part in path.parts)


def attribute_name(node: ast.AST):
    if isinstance(node, ast.Attribute):
        return node.attr

    return None


def root_name(node: ast.AST):
    while isinstance(node, ast.Attribute):
        node = node.value

    if isinstance(node, ast.Name):
        return node.id

    return None


def main():
    usages = defaultdict(list)

    for path in sorted(ROOT.rglob("*.py")):
        if is_excluded(path):
            continue

        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        relative = path.relative_to(ROOT).as_posix()

        for node in ast.walk(tree):
            if not isinstance(node, ast.Attribute):
                continue

            root = root_name(node.value)

            if root not in TARGETS:
                continue

            attr = attribute_name(node)

            if attr is None:
                continue

            usages[root].append(
                (
                    relative,
                    node.lineno,
                    attr,
                    ast.unparse(node),
                )
            )

    print("=" * 80)
    print("SanskritAI — SOURCE MODEL API USAGE AUDIT")
    print("=" * 80)

    for target in sorted(TARGETS):
        print()
        print("-" * 80)
        print(target)
        print("-" * 80)

        items = usages.get(target, [])

        if not items:
            print("  <no direct attribute usage detected>")
            continue

        grouped = defaultdict(list)

        for filename, line, attr, expression in items:
            grouped[attr].append(
                (filename, line, expression)
            )

        for attr in sorted(grouped):
            print()
            print(f"  .{attr}")

            for filename, line, expression in sorted(
                grouped[attr],
                key=lambda x: (x[0], x[1]),
            ):
                print(
                    f"    {filename}:{line} -> {expression}"
                )

    print()
    print("=" * 80)
    print("END OF API USAGE AUDIT")
    print("=" * 80)


if __name__ == "__main__":
    main()

