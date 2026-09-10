from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")
TARGET = "SanskritAI.domain.lexical.lexical_source.LexicalSource"

NUMERIC_SUFFIX_RE = None


def is_historical_python_file(path: Path) -> bool:
    name = path.name

    if not name.endswith(".py"):
        return True

    stem = name[:-3]

    # Ignore historical numbered files:
    # foo1.py, foo2.py, foo10.py, etc.
    if stem and stem[-1].isdigit():
        i = len(stem) - 1
        while i >= 0 and stem[i].isdigit():
            i -= 1
        return True

    # Ignore generated/grouped historical variants such as foo_G1.py
    if "_G" in stem:
        suffix = stem.rsplit("_G", 1)[-1]
        if suffix.isdigit():
            return True

    # Ignore tests for production-consumer audit.
    if "test" in path.parts:
        return True

    if "__pycache__" in path.parts:
        return True

    return False


def iter_python_files():
    for path in ROOT.rglob("*.py"):
        if is_historical_python_file(path):
            continue
        yield path


def module_name(path: Path) -> str:
    relative = path.relative_to(ROOT).with_suffix("")
    return ".".join(relative.parts)


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
    except Exception as exc:
        return [], [f"PARSE ERROR: {exc}"]

    imports = []
    references = []
    errors = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                imported = (
                    f"{module}.{alias.name}"
                    if module
                    else alias.name
                )

                if imported == TARGET:
                    imports.append(
                        f"line {node.lineno}: "
                        f"from {module} import {alias.name}"
                    )

        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == TARGET:
                    imports.append(
                        f"line {node.lineno}: import {alias.name}"
                    )

        elif isinstance(node, ast.Attribute):
            name = dotted_name(node)
            if name and (
                name == TARGET
                or name.endswith(".LexicalSource")
            ):
                references.append(
                    f"line {node.lineno}: {name}"
                )

        elif isinstance(node, ast.Name):
            if node.id == "LexicalSource":
                references.append(
                    f"line {node.lineno}: LexicalSource"
                )

    return imports, references + errors


def main():
    print("=" * 100)
    print("SANSKRITAI — DOMAIN LEXICALSOURCE DIRECT CONSUMER AUDIT")
    print("=" * 100)
    print()
    print(f"TARGET: {TARGET}")
    print()

    total_files = 0
    consumer_files = 0

    for path in sorted(iter_python_files()):
        total_files += 1

        imports, references = analyze(path)

        if not imports and not references:
            continue

        consumer_files += 1

        print("-" * 100)
        print(f"FILE: {path.relative_to(ROOT)}")
        print(f"MODULE: {module_name(path)}")
        print()

        if imports:
            print("IMPORTS")
            for item in imports:
                print(f"  {item}")
            print()

        if references:
            print("REFERENCES")
            for item in references:
                print(f"  {item}")
            print()

    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"Production Python files scanned: {total_files}")
    print(f"Files with LexicalSource evidence: {consumer_files}")
    print()
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 100)


if __name__ == "__main__":
    main()
