from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")
TARGET_MODULE = "SanskritAI.domain.lexical.lexical_source"
TARGET_CLASS = "LexicalSource"


def iter_test_files():
    for path in ROOT.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue

        if "test" in path.parts or path.name.startswith("test_"):
            yield path


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        if parent:
            return f"{parent}.{node.attr}"

    return None


def analyze(path: Path):
    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except Exception:
        return []

    aliases = set()
    evidence = []

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):
            module = node.module or ""

            if module == TARGET_MODULE:
                for alias in node.names:
                    if alias.name == TARGET_CLASS:
                        aliases.add(
                            alias.asname or alias.name
                        )

                        evidence.append(
                            (
                                node.lineno,
                                "IMPORT",
                                f"from {module} import {alias.name}",
                            )
                        )

        elif isinstance(node, ast.Call):
            name = dotted_name(node.func)

            if name in aliases or name == TARGET_CLASS:
                evidence.append(
                    (
                        node.lineno,
                        "CONSTRUCTION",
                        name,
                    )
                )

        elif isinstance(node, ast.Attribute):
            name = dotted_name(node)

            if name and TARGET_CLASS in name:
                evidence.append(
                    (
                        node.lineno,
                        "REFERENCE",
                        name,
                    )
                )

        elif isinstance(node, ast.Name):
            if node.id in aliases or node.id == TARGET_CLASS:
                evidence.append(
                    (
                        node.lineno,
                        "NAME",
                        node.id,
                    )
                )

    return sorted(set(evidence))


def main():
    print("=" * 100)
    print("SANSKRITAI — DOMAIN LEXICALSOURCE TEST / FIXTURE AUDIT")
    print("=" * 100)
    print()
    print(f"TARGET: {TARGET_MODULE}.{TARGET_CLASS}")
    print()

    found = 0

    for path in sorted(iter_test_files()):
        evidence = analyze(path)

        if not evidence:
            continue

        found += 1

        print("-" * 100)
        print(f"TEST FILE: {path.relative_to(ROOT)}")

        for line, kind, value in evidence:
            print(f"  line {line}: {kind}: {value}")

        print()

    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"Test files with evidence: {found}")
    print()
    print(
        "Use this result to determine whether the Domain "
        "LexicalSource has a tested behavioral contract."
    )
    print()
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 100)


if __name__ == "__main__":
    main()
