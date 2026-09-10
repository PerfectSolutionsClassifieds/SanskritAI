from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGET = "LexicalSource"

NUMBERED_FILE_RE = re.compile(r".*\d+\.py$")
GENERATED_COPY_RE = re.compile(r".*_G\d+\.py$")


def excluded(path: Path) -> bool:
    parts = {p.lower() for p in path.parts}

    if "tests" in parts:
        return True

    if "__pycache__" in parts:
        return True

    if NUMBERED_FILE_RE.match(path.name):
        return True

    if GENERATED_COPY_RE.match(path.name):
        return True

    return False


def dotted(node):
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        left = dotted(node.value)
        return f"{left}.{node.attr}" if left else node.attr

    return None


def main():
    print("=" * 100)
    print("SANSKRITAI — LEXICALSOURCE DEPENDENCY CHAIN AUDIT")
    print("=" * 100)
    print()

    results = {}

    for path in ROOT.rglob("*.py"):

        if excluded(path):
            continue

        try:
            tree = ast.parse(
                path.read_text(encoding="utf-8")
            )
        except Exception:
            continue

        imports = []
        references = []
        constructors = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ImportFrom):

                for alias in node.names:

                    if alias.name == TARGET:

                        imports.append(
                            (
                                node.lineno,
                                node.module or "",
                            )
                        )

            elif isinstance(node, ast.Name):

                if node.id == TARGET:

                    references.append(node.lineno)

            elif isinstance(node, ast.Call):

                if dotted(node.func) == TARGET:

                    constructors.append(node.lineno)

        if not (
            imports
            or references
            or constructors
        ):
            continue

        rel = str(path.relative_to(ROOT))

        results[rel] = {
            "imports": sorted(set(imports)),
            "references": sorted(set(references)),
            "constructors": sorted(set(constructors)),
        }

    print("PRODUCTION CONSUMERS")
    print()

    for rel in sorted(results):

        item = results[rel]

        print("-" * 100)
        print(rel)

        if item["imports"]:
            print("  imports:")
            for line, module in item["imports"]:
                print(
                    f"    line {line}: "
                    f"from {module} import LexicalSource"
                )

        if item["constructors"]:
            print("  constructors:")
            for line in item["constructors"]:
                print(
                    f"    line {line}: "
                    f"LexicalSource(...)"
                )

        if item["references"]:
            print("  references:")
            for line in item["references"]:
                print(
                    f"    line {line}: "
                    f"LexicalSource"
                )

    print()
    print("=" * 100)
    print("CONSUMER SUMMARY")
    print("=" * 100)

    print(
        f"Production modules containing "
        f"LexicalSource evidence: {len(results)}"
    )

    print()

    print("Important:")
    print(
        "This audit reports the dependency chain around the "
        "symbol name."
    )
    print(
        "It does not decide which implementation owns a reference."
    )

    print()
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 100)


if __name__ == "__main__":
    main()
