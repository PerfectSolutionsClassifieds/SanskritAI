from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGET_MODULES = {
    "DOMAIN":
        "SanskritAI.domain.lexical.lexical_source",
    "LEXICAL_MODEL":
        "SanskritAI.lexical.models.lexical_source",
}

NUMBERED_RE = re.compile(r".*\d+\.py$")
GENERATED_RE = re.compile(r".*_G\d+\.py$")


def excluded(path: Path) -> bool:
    parts = {p.lower() for p in path.parts}

    if "tests" in parts:
        return True

    if "__pycache__" in parts:
        return True

    if NUMBERED_RE.match(path.name):
        return True

    if GENERATED_RE.match(path.name):
        return True

    return False


def dotted(node):
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        left = dotted(node.value)
        if left:
            return f"{left}.{node.attr}"
        return node.attr

    return None


def main():
    print("=" * 100)
    print("SANSKRITAI — LEXICALSOURCE PRODUCTION CONSTRUCTION AUDIT")
    print("=" * 100)

    results = {
        "DOMAIN": [],
        "LEXICAL_MODEL": [],
    }

    for path in ROOT.rglob("*.py"):

        if excluded(path):
            continue

        try:
            tree = ast.parse(
                path.read_text(encoding="utf-8")
            )
        except Exception:
            continue

        aliases = {}

        for node in ast.walk(tree):

            if isinstance(node, ast.ImportFrom):

                module = node.module or ""

                for alias in node.names:

                    if alias.name != "LexicalSource":
                        continue

                    bound = alias.asname or alias.name

                    if module == TARGET_MODULES["DOMAIN"]:
                        aliases[bound] = "DOMAIN"

                    elif module == TARGET_MODULES["LEXICAL_MODEL"]:
                        aliases[bound] = "LEXICAL_MODEL"

        for node in ast.walk(tree):

            if not isinstance(node, ast.Call):
                continue

            name = dotted(node.func)

            if name in aliases:

                results[
                    aliases[name]
                ].append(
                    (
                        str(path.relative_to(ROOT)),
                        node.lineno,
                        name,
                    )
                )

    for key in results:
        results[key] = sorted(
            set(results[key])
        )

    for key, title in [
        (
            "DOMAIN",
            "domain.lexical.lexical_source.LexicalSource",
        ),
        (
            "LEXICAL_MODEL",
            "lexical.models.lexical_source.LexicalSource",
        ),
    ]:

        print()
        print("-" * 100)
        print(title)
        print("-" * 100)

        if not results[key]:
            print("  NO DIRECT CONSTRUCTORS FOUND")
        else:
            for rel, line, name in results[key]:
                print(
                    f"  {rel}:{line} -> "
                    f"{name}(...)"
                )

        print(
            f"  TOTAL: {len(results[key])}"
        )

    print()
    print("=" * 100)
    print("IMPORTANT")
    print("=" * 100)
    print()
    print(
        "No constructor evidence does not prove a model is unused."
    )
    print(
        "Models may be created through factories, deserialization,"
    )
    print(
        "dependency injection, or external callers."
    )
    print()
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 100)


if __name__ == "__main__":
    main()
