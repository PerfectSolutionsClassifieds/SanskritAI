from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")

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
    print("=" * 90)
    print("SANSKRITAI — LEXICALSOURCE PACKAGE RE-EXPORT AUDIT")
    print("=" * 90)
    print()

    found = []

    for path in ROOT.rglob("*.py"):
        if excluded(path):
            continue

        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        rel = path.relative_to(ROOT)

        for node in ast.walk(tree):

            if isinstance(node, ast.ImportFrom):
                module = node.module or ""

                for alias in node.names:
                    if alias.name != "LexicalSource":
                        continue

                    if (
                        "lexical_source" in module.lower()
                        or module.endswith(".lexical")
                        or module.endswith(".models")
                    ):
                        found.append(
                            (
                                str(rel),
                                node.lineno,
                                f"from {module} import "
                                f"LexicalSource"
                                + (
                                    f" as {alias.asname}"
                                    if alias.asname
                                    else ""
                                ),
                            )
                        )

            elif isinstance(node, ast.Assign):
                value = dotted(node.value)

                if value and value.endswith("LexicalSource"):
                    for target in node.targets:
                        target_name = dotted(target)

                        if target_name:
                            found.append(
                                (
                                    str(rel),
                                    node.lineno,
                                    f"{target_name} = {value}",
                                )
                            )

    found = sorted(set(found))

    if not found:
        print("  (no possible re-export/import evidence found)")
    else:
        for rel, line, statement in found:
            print(f"  {rel}:{line}")
            print(f"      {statement}")

    print()
    print("-" * 90)
    print(f"TOTAL RE-EXPORT / IMPORT EVIDENCE: {len(found)}")
    print("-" * 90)
    print()
    print("This audit is evidence-only.")
    print("No production files were modified.")
    print("=" * 90)


if __name__ == "__main__":
    main()
