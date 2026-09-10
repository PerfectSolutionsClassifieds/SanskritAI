from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGETS = {
    "DOMAIN": ROOT / "domain/lexical/lexical_source.py",
    "LEXICAL_MODEL": ROOT / "lexical/models/lexical_source.py",
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


def annotation_text(node):
    if node is None:
        return None

    try:
        return ast.unparse(node)
    except Exception:
        return None


def inspect_file(label: str, path: Path):
    print()
    print("=" * 90)
    print(f"{label}: {path.relative_to(ROOT)}")
    print("=" * 90)

    if not path.exists():
        print("FILE NOT FOUND")
        return

    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except Exception as exc:
        print(f"PARSE ERROR: {exc}")
        return

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        if node.name != "LexicalSource":
            continue

        print()
        print("CLASS")
        print(f"  name       : {node.name}")
        print(f"  line       : {node.lineno}")

        print()
        print("BASE CLASSES")
        for base in node.bases:
            print(f"  {annotation_text(base)}")

        print()
        print("CLASS DECORATORS")
        if node.decorator_list:
            for decorator in node.decorator_list:
                print(f"  {annotation_text(decorator)}")
        else:
            print("  (none)")

        fields = []
        properties = []
        methods = []

        for item in node.body:

            if isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    fields.append(
                        (
                            item.target.id,
                            annotation_text(item.annotation),
                        )
                    )

            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        fields.append(
                            (
                                target.id,
                                None,
                            )
                        )

            elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = []

                for arg in item.args.args:
                    args.append(
                        f"{arg.arg}: "
                        f"{annotation_text(arg.annotation) or 'Any'}"
                    )

                returns = annotation_text(item.returns) or "None"

                decorators = [
                    annotation_text(d)
                    for d in item.decorator_list
                ]

                entry = {
                    "name": item.name,
                    "line": item.lineno,
                    "args": args,
                    "returns": returns,
                    "decorators": decorators,
                }

                if "property" in decorators:
                    properties.append(entry)
                else:
                    methods.append(entry)

        print()
        print("FIELDS / ATTRIBUTES")
        if fields:
            for name, annotation in fields:
                print(
                    f"  {name}"
                    + (f": {annotation}" if annotation else "")
                )
        else:
            print("  (none)")

        print()
        print("PROPERTIES")
        if properties:
            for item in properties:
                print(
                    f"  {item['name']}() "
                    f"[line {item['line']}]"
                )
                print(
                    f"      -> {item['returns']}"
                )
        else:
            print("  (none)")

        print()
        print("METHODS")
        if methods:
            for item in methods:
                args = ", ".join(item["args"])

                print(
                    f"  {item['name']}({args}) "
                    f"[line {item['line']}]"
                )
                print(
                    f"      -> {item['returns']}"
                )

                if item["decorators"]:
                    print(
                        f"      decorators: "
                        f"{', '.join(item['decorators'])}"
                    )
        else:
            print("  (none)")

        print()
        print("DOCSTRING")
        doc = ast.get_docstring(node)
        if doc:
            for line in doc.splitlines():
                print(f"  {line}")
        else:
            print("  (none)")


def main():
    print("=" * 90)
    print("SANSKRITAI — LEXICALSOURCE IMPLEMENTATION AUDIT")
    print("=" * 90)
    print()
    print("Historical/duplicate files are excluded.")
    print("No production files are modified.")

    for label, path in TARGETS.items():
        inspect_file(label, path)

    print()
    print("=" * 90)
    print("AUDIT COMPLETE")
    print("=" * 90)


if __name__ == "__main__":
    main()
