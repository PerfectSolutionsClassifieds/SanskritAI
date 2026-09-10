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

        if left:
            return f"{left}.{node.attr}"

        return node.attr

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
    print("SANSKRITAI — LEXICALSOURCE CONSUMER DETAIL AUDIT")
    print("=" * 100)

    for path in ROOT.rglob("*.py"):

        if excluded(path):
            continue

        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except Exception:
            continue

        imports = {}

        for node in ast.walk(tree):

            # ---------------------------------------------------------
            # Imports
            # ---------------------------------------------------------
            if isinstance(node, ast.ImportFrom):

                module = node.module or ""

                for alias in node.names:

                    if alias.name != "LexicalSource":
                        continue

                    bound = alias.asname or alias.name

                    if module == TARGET_MODULES["DOMAIN"]:
                        imports[bound] = "DOMAIN"

                    elif module == TARGET_MODULES["LEXICAL_MODEL"]:
                        imports[bound] = "LEXICAL_MODEL"

            elif isinstance(node, ast.Import):

                for alias in node.names:

                    if alias.name == TARGET_MODULES["DOMAIN"]:
                        imports[
                            alias.asname or alias.name.split(".")[-1]
                        ] = "DOMAIN"

                    elif alias.name == TARGET_MODULES["LEXICAL_MODEL"]:
                        imports[
                            alias.asname or alias.name.split(".")[-1]
                        ] = "LEXICAL_MODEL"

        if not imports:
            continue

        rel = path.relative_to(ROOT)

        print()
        print("-" * 100)
        print(rel)
        print("-" * 100)

        print()
        print("IMPORTS")

        for bound, target in imports.items():
            print(f"  {bound} -> {target}")

        print()
        print("REFERENCES")

        references = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Name):

                if node.id in imports:
                    references.append(
                        (
                            node.lineno,
                            "NAME",
                            node.id,
                        )
                    )

            elif isinstance(node, ast.Call):

                name = dotted(node.func)

                if name in imports:
                    references.append(
                        (
                            node.lineno,
                            "CONSTRUCTOR/CALL",
                            name,
                        )
                    )

            elif isinstance(node, ast.arg):

                ann = annotation(node.annotation)

                if ann and ann in imports:
                    references.append(
                        (
                            node.lineno,
                            "PARAMETER ANNOTATION",
                            ann,
                        )
                    )

            elif isinstance(node, (ast.AnnAssign, ast.Assign)):

                ann = None

                if isinstance(node, ast.AnnAssign):
                    ann = annotation(node.annotation)

                if ann and ann in imports:
                    references.append(
                        (
                            node.lineno,
                            "VARIABLE ANNOTATION",
                            ann,
                        )
                    )

            elif isinstance(node, ast.FunctionDef):

                ret = annotation(node.returns)

                if ret and ret in imports:
                    references.append(
                        (
                            node.lineno,
                            "RETURN ANNOTATION",
                            ret,
                        )
                    )

        for lineno, kind, value in sorted(
            set(references)
        ):
            print(
                f"  line {lineno:<5} "
                f"{kind:<24} {value}"
            )

        if (
            "DOMAIN" in imports.values()
            and "LEXICAL_MODEL" in imports.values()
        ):
            print()
            print(
                "  *** BOTH LexicalSource implementations "
                "are imported by this module. ***"
            )

    print()
    print("=" * 100)
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 100)


if __name__ == "__main__":
    main()
