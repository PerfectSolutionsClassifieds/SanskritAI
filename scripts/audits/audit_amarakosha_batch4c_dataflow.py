
from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")
AMARAKOSHA = ROOT / "amarakosha"


def excluded(path: Path) -> bool:

    name = path.name

    if "__pycache__" in path.parts:
        return True

    if re.search(r"_G\d+\.py$", name):
        return True

    if re.search(r"\d+\.py$", name):
        return True

    return False


def dotted_name(node):

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):

        parent = dotted_name(node.value)

        if parent:
            return f"{parent}.{node.attr}"

        return node.attr

    return None


def parse(path):

    try:
        return ast.parse(
            path.read_text(
                encoding="utf-8"
            ),
            filename=str(path),
        )
    except Exception:
        return None


def main():

    print("=" * 90)
    print("BATCH 4C — AMARAKOSHA DATA-FLOW CONTRACT AUDIT")
    print("=" * 90)
    print()

    if not AMARAKOSHA.exists():
        print("ERROR: amarakosha/ not found")
        return

    files = sorted(
        p
        for p in AMARAKOSHA.rglob("*.py")
        if not excluded(p)
    )

    interesting = (
        "Builder",
        "Record",
        "Parser",
        "Importer",
        "Registry",
        "Repository",
        "Validator",
        "Synset",
        "Varga",
    )

    for path in files:

        tree = parse(path)

        if tree is None:
            continue

        relative = path.relative_to(ROOT)

        print("-" * 90)
        print(relative)

        # -------------------------------------------------------------
        # Classes
        # -------------------------------------------------------------

        for node in ast.walk(tree):

            if not isinstance(
                node,
                ast.ClassDef,
            ):
                continue

            if not any(
                token.lower() in node.name.lower()
                for token in interesting
            ):
                continue

            bases = [
                dotted_name(base)
                for base in node.bases
            ]

            print(
                f"  CLASS      {node.name}"
            )

            if bases:
                print(
                    f"    BASES    {bases}"
                )

            # ---------------------------------------------------------
            # Methods
            # ---------------------------------------------------------

            for method in node.body:

                if not isinstance(
                    method,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                    ),
                ):
                    continue

                if method.name.startswith("_") and method.name not in {
                    "__init__",
                    "__post_init__",
                }:
                    continue

                return_type = (
                    dotted_name(method.returns)
                    if method.returns
                    else None
                )

                print(
                    f"    METHOD   {method.name}"
                    f"  -> {return_type}"
                    f"  line={method.lineno}"
                )

                # -----------------------------------------------------
                # Calls inside method
                # -----------------------------------------------------

                for call in ast.walk(method):

                    if not isinstance(
                        call,
                        ast.Call,
                    ):
                        continue

                    name = dotted_name(call.func)

                    if not name:
                        continue

                    final = name.split(".")[-1]

                    if (
                        final in {
                            "Synset",
                            "Varga",
                            "SynsetRecord",
                            "VargaRecord",
                            "Lexeme",
                            "LexicalRecord",
                            "CanonicalDictionaryEntry",
                            "CanonicalDictionarySense",
                            "CanonicalLexicon",
                            "CanonicalSource",
                            "CanonicalKnowledgeRepository",
                        }
                        or
                        "build" in final.lower()
                        or
                        "parse" in final.lower()
                        or
                        "import" in final.lower()
                        or
                        "register" in final.lower()
                    ):
                        print(
                            f"      CALL {name}"
                            f"  line={call.lineno}"
                        )

    print()
    print("=" * 90)
    print("BATCH 4C COMPLETE")
    print("=" * 90)
    print()
    print("Do not modify production code from this report.")
    print("Use the output to establish the Amarakośa ownership matrix.")


if __name__ == "__main__":
    main()
