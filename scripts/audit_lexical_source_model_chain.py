from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")

NUMBERED_RE = re.compile(r".*\d+\.py$")
GENERATED_RE = re.compile(r".*_G\d+\.py$")


TARGET_FILES = [
    ROOT / "lexical/models/dictionary_entry.py",
    ROOT / "lexical/models/lexical_record.py",
    ROOT / "lexical/models/lexical_source.py",
    ROOT / "lexical/registries/lexical_source_catalog.py",
    ROOT / "lexical/repositories/lexical_repository.py",
    ROOT / "lexical/repositories/in_memory_lexical_repository.py",
    ROOT / "lexical/validators/lexical_source_validator.py",
]


def excluded(path):
    if not path.exists():
        return True

    if "tests" in {p.lower() for p in path.parts}:
        return True

    if NUMBERED_RE.match(path.name):
        return True

    if GENERATED_RE.match(path.name):
        return True

    return False


def annotation(node):
    if node is None:
        return None

    try:
        return ast.unparse(node)
    except Exception:
        return None


def main():
    print("=" * 100)
    print("SANSKRITAI — LEXICALSOURCE MODEL OWNERSHIP CHAIN")
    print("=" * 100)

    for path in TARGET_FILES:

        if excluded(path):
            continue

        print()
        print("-" * 100)
        print(path.relative_to(ROOT))
        print("-" * 100)

        tree = ast.parse(
            path.read_text(encoding="utf-8")
        )

        for node in ast.walk(tree):

            if isinstance(node, ast.ImportFrom):

                for alias in node.names:

                    if alias.name == "LexicalSource":
                        print(
                            f"IMPORT line {node.lineno}: "
                            f"{node.module}.LexicalSource"
                        )

            elif isinstance(node, ast.AnnAssign):

                ann = annotation(node.annotation)

                if ann and "LexicalSource" in ann:
                    target = annotation(node.target)

                    print(
                        f"ANNOTATION line {node.lineno}: "
                        f"{target}: {ann}"
                    )

            elif isinstance(node, ast.arg):

                ann = annotation(node.annotation)

                if ann and "LexicalSource" in ann:
                    print(
                        f"PARAMETER line {node.lineno}: "
                        f"{node.arg}: {ann}"
                    )

            elif isinstance(node, ast.FunctionDef):

                ret = annotation(node.returns)

                if ret and "LexicalSource" in ret:
                    print(
                        f"RETURN line {node.lineno}: "
                        f"{ret}"
                    )

    print()
    print("=" * 100)
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 100)


if __name__ == "__main__":
    main()
