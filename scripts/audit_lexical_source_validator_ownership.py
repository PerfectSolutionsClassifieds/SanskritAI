from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGETS = [
    ROOT / "domain/lexical/validators/lexical_source_validator.py",
    ROOT / "lexical/validators/lexical_source_validator.py",
]


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


def inspect(path: Path):
    print()
    print("=" * 100)
    print(f"FILE: {path.relative_to(ROOT)}")
    print("=" * 100)

    if not path.exists():
        print("FILE NOT FOUND")
        return

    tree = ast.parse(path.read_text(encoding="utf-8"))

    print()
    print("IMPORTS")

    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "LexicalSource":
                    print(
                        f"  line {node.lineno}: "
                        f"from {node.module} import "
                        f"{alias.name}"
                    )

    print()
    print("CLASSES")

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        print()
        print(
            f"  class {node.name} "
            f"(line {node.lineno})"
        )

        print("    bases:")
        for base in node.bases:
            print(
                f"      {annotation(base)}"
            )

        print()
        print("    methods:")

        for item in node.body:
            if not isinstance(
                item,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                continue

            print(
                f"      {item.name}() "
                f"[line {item.lineno}]"
            )

            if item.returns:
                print(
                    f"        returns: "
                    f"{annotation(item.returns)}"
                )

            for arg in item.args.args:
                ann = annotation(arg.annotation)

                if ann:
                    print(
                        f"        parameter "
                        f"{arg.arg}: {ann}"
                    )

            for child in ast.walk(item):
                if isinstance(child, ast.Name):
                    if child.id == "LexicalSource":
                        print(
                            f"        LexicalSource "
                            f"reference at line "
                            f"{child.lineno}"
                        )


def main():
    print("=" * 100)
    print("SANSKRITAI — LEXICALSOURCE VALIDATOR OWNERSHIP AUDIT")
    print("=" * 100)

    for target in TARGETS:
        inspect(target)

    print()
    print("=" * 100)
    print("ARCHITECTURAL QUESTIONS")
    print("=" * 100)
    print()
    print("1. Is the domain validator exclusively a Domain concern?")
    print("2. Is the lexical validator exclusively a Lexical Model concern?")
    print("3. Do their validation rules overlap?")
    print("4. Do they validate different contracts?")
    print("5. Is either validator merely a duplicate of the other?")
    print()
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 100)


if __name__ == "__main__":
    main()
