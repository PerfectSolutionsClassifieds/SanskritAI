from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")
TARGET_IMPORT = "SanskritAI.domain.lexical.lexical_source"
TARGET_CLASS = "LexicalSource"


def is_historical_python_file(path: Path) -> bool:
    name = path.name

    if not name.endswith(".py"):
        return True

    stem = name[:-3]

    if stem and stem[-1].isdigit():
        return True

    if "_G" in stem:
        suffix = stem.rsplit("_G", 1)[-1]
        if suffix.isdigit():
            return True

    if "__pycache__" in path.parts:
        return True

    return False


def iter_python_files():
    for path in ROOT.rglob("*.py"):
        if is_historical_python_file(path):
            continue
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
    except Exception as exc:
        return []

    imported_aliases = set()
    evidence = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""

            if module == TARGET_IMPORT:
                for alias in node.names:
                    if alias.name == TARGET_CLASS:
                        imported_aliases.add(
                            alias.asname or alias.name
                        )

        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == TARGET_IMPORT:
                    imported_aliases.add(
                        alias.asname or alias.name
                    )

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):
            func_name = dotted_name(node.func)

            if func_name in imported_aliases:
                evidence.append(
                    (
                        node.lineno,
                        "DIRECT CONSTRUCTOR",
                        func_name,
                    )
                )

            elif func_name == TARGET_CLASS:
                evidence.append(
                    (
                        node.lineno,
                        "CONSTRUCTOR",
                        func_name,
                    )
                )

        elif isinstance(node, ast.Attribute):
            name = dotted_name(node)

            if name and TARGET_CLASS in name:
                evidence.append(
                    (
                        node.lineno,
                        "ATTRIBUTE REFERENCE",
                        name,
                    )
                )

    return sorted(set(evidence))


def main():
    print("=" * 100)
    print("SANSKRITAI — DOMAIN LEXICALSOURCE CONSTRUCTION / FACTORY AUDIT")
    print("=" * 100)
    print()
    print(f"TARGET MODULE: {TARGET_IMPORT}")
    print(f"TARGET CLASS : {TARGET_CLASS}")
    print()

    found = 0

    for path in sorted(iter_python_files()):
        evidence = analyze(path)

        if not evidence:
            continue

        found += 1

        print("-" * 100)
        print(f"FILE: {path.relative_to(ROOT)}")

        for line, kind, name in evidence:
            print(f"  line {line}: {kind}: {name}")

        print()

    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)

    if found == 0:
        print("NO DIRECT CONSTRUCTION EVIDENCE FOUND")
        print()
        print(
            "This does NOT prove the model is unused."
        )
        print(
            "Possible indirect paths include factories, "
            "deserialization, dependency injection, "
            "reflection, or external callers."
        )
    else:
        print(f"Files with construction evidence: {found}")

    print()
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 100)


if __name__ == "__main__":
    main()
