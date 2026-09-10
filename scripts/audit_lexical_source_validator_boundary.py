from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGET = (
    ROOT
    / "lexical"
    / "validators"
    / "lexical_source_validator.py"
)


def dotted(node):
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        left = dotted(node.value)
        return f"{left}.{node.attr}" if left else node.attr

    return None


def annotation(node):
    if node is None:
        return None

    try:
        return ast.unparse(node)
    except Exception:
        return None


def main():
    print("=" * 100)
    print("SANSKRITAI — LEXICALSOURCE VALIDATOR BOUNDARY AUDIT")
    print("=" * 100)

    print()
    print(f"TARGET: {TARGET.relative_to(ROOT)}")

    if not TARGET.exists():
        print("FILE NOT FOUND")
        return

    text = TARGET.read_text(encoding="utf-8")
    tree = ast.parse(text)

    print()
    print("-" * 100)
    print("IMPORTS OF LEXICALSOURCE")
    print("-" * 100)

    aliases = {}

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):

            module = node.module or ""

            for alias in node.names:

                if alias.name != "LexicalSource":
                    continue

                bound = alias.asname or alias.name

                aliases[bound] = module

                print(
                    f"line {node.lineno}: "
                    f"{bound} <- {module}"
                )

    print()
    print("-" * 100)
    print("LEXICALSOURCE REFERENCES")
    print("-" * 100)

    for node in ast.walk(tree):

        if isinstance(node, ast.Name):

            if node.id in aliases:
                print(
                    f"line {node.lineno}: "
                    f"NAME {node.id}"
                )

        elif isinstance(node, ast.Call):

            name = dotted(node.func)

            if name in aliases:
                print(
                    f"line {node.lineno}: "
                    f"CALL {name}(...)"
                )

        elif isinstance(node, ast.arg):

            ann = annotation(node.annotation)

            if ann in aliases:
                print(
                    f"line {node.lineno}: "
                    f"PARAMETER {ann}"
                )

        elif isinstance(node, ast.AnnAssign):

            ann = annotation(node.annotation)

            if ann in aliases:
                print(
                    f"line {node.lineno}: "
                    f"ATTRIBUTE/VARIABLE {ann}"
                )

        elif isinstance(node, ast.FunctionDef):

            ret = annotation(node.returns)

            if ret in aliases:
                print(
                    f"line {node.lineno}: "
                    f"RETURN {ret}"
                )

    print()
    print("-" * 100)
    print("CLASS DEFINITIONS")
    print("-" * 100)

    for node in tree.body:

        if isinstance(node, ast.ClassDef):

            print(
                f"line {node.lineno}: "
                f"class {node.name}"
            )

            print("  bases:")

            for base in node.bases:
                print(
                    f"    {annotation(base)}"
                )

    print()
    print("=" * 100)
    print("BOUNDARY QUESTIONS")
    print("=" * 100)
    print()
    print("1. Why does this validator import both implementations?")
    print("2. Is one import used only for compatibility?")
    print("3. Is one implementation used for validation while the")
    print("   other is used for lexical-model typing?")
    print("4. Is this validator actually crossing the Domain/Kernel boundary?")
    print("5. Could the two implementations be consolidated safely?")
    print()
    print("AUDIT ONLY — NO FILES MODIFIED")
    print("=" * 100)


if __name__ == "__main__":
    main()
