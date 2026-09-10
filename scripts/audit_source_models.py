
from __future__ import annotations

from pathlib import Path
import ast


ROOT = Path("/content/SanskritAI")


TARGET_CLASSES = {
    "CorpusSource",
    "CanonicalSource",
    "LexicalSource",
    "MonierWilliamsSource",
}


EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "sanskritai.egg-info",
}


EXCLUDED_PREFIXES = (
    "tests/",
)


def iter_python_files(root: Path):
    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root).as_posix()

        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue

        if relative.startswith(EXCLUDED_PREFIXES):
            continue

        yield path


def get_class_definitions(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except Exception as exc:
        return [], f"{type(exc).__name__}: {exc}"

    results = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        if node.name not in TARGET_CLASSES:
            continue

        bases = []

        for base in node.bases:
            try:
                bases.append(ast.unparse(base))
            except Exception:
                bases.append("<unknown>")

        fields = []

        for item in node.body:
            if isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    fields.append(item.target.id)

        results.append(
            {
                "name": node.name,
                "line": node.lineno,
                "bases": bases,
                "fields": fields,
            }
        )

    return results, None


def main():
    print("=" * 80)
    print("SanskritAI — CANONICAL SOURCE MODEL AUDIT")
    print("=" * 80)

    definitions = []

    for path in iter_python_files(ROOT):
        results, error = get_class_definitions(path)

        if error:
            print(f"\nPARSE ERROR: {path}")
            print(f"  {error}")
            continue

        for result in results:
            definitions.append(
                (
                    path.relative_to(ROOT),
                    result,
                )
            )

    if not definitions:
        print("\nNo target source models found.")
        return

    for path, result in definitions:
        print("\n" + "-" * 80)
        print(path)
        print("-" * 80)

        print(f"class: {result['name']}")
        print(f"line:  {result['line']}")

        print("bases:")
        if result["bases"]:
            for base in result["bases"]:
                print(f"  - {base}")
        else:
            print("  - <none>")

        print("annotated fields:")
        if result["fields"]:
            for field in result["fields"]:
                print(f"  - {field}")
        else:
            print("  - <none>")

    print("\n" + "=" * 80)
    print("SOURCE MODEL DEFINITIONS BY CONCEPT")
    print("=" * 80)

    for target in sorted(TARGET_CLASSES):
        matches = [
            path
            for path, result in definitions
            if result["name"] == target
        ]

        print(f"\n{target}")
        if matches:
            for path in matches:
                print(f"  - {path}")
        else:
            print("  - NOT FOUND")

    print("\n" + "=" * 80)
    print(f"TOTAL TARGET SOURCE MODEL DEFINITIONS: {len(definitions)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
