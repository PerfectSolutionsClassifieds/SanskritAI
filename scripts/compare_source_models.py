
from __future__ import annotations

from pathlib import Path
import ast


ROOT = Path("/content/SanskritAI")


TARGETS = {
    "CorpusSource": [
        ROOT / "acquisition/models/corpus_source.py",
    ],
    "CanonicalSource": [
        ROOT / "acquisition/knowledge/models/canonical_source.py",
    ],
    "LexicalSource": [
        ROOT / "domain/lexical/lexical_source.py",
        ROOT / "lexical/models/lexical_source.py",
    ],
    "MonierWilliamsSource": [
        ROOT / "acquisition/sources/monier_williams.py",
        ROOT / "acquisition/lexical/monier_williams/monier_williams_source.py",
    ],
}


def class_info(path: Path, target: str):
    if not path.exists():
        return {
            "path": str(path.relative_to(ROOT)),
            "exists": False,
        }

    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        if node.name != target:
            continue

        bases = []
        for base in node.bases:
            bases.append(ast.unparse(base))

        fields = []

        for item in node.body:
            if isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    fields.append(item.target.id)

        methods = []

        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(item.name)

        decorators = []

        for decorator in node.decorator_list:
            decorators.append(ast.unparse(decorator))

        return {
            "path": str(path.relative_to(ROOT)),
            "exists": True,
            "class": node.name,
            "line": node.lineno,
            "bases": bases,
            "fields": fields,
            "methods": methods,
            "decorators": decorators,
        }

    return {
        "path": str(path.relative_to(ROOT)),
        "exists": True,
        "class": None,
    }


def main():
    print("=" * 80)
    print("SanskritAI — SOURCE MODEL STRUCTURAL COMPARISON")
    print("=" * 80)

    for model, paths in TARGETS.items():
        print("\n" + "=" * 80)
        print(model)
        print("=" * 80)

        for path in paths:
            info = class_info(path, model)

            print("\nFILE:")
            print(f"  {info['path']}")

            if not info["exists"]:
                print("  STATUS: FILE NOT FOUND")
                continue

            if info.get("class") is None:
                print("  STATUS: TARGET CLASS NOT FOUND")
                continue

            print(f"  class: {info['class']}")
            print(f"  line:  {info['line']}")

            print("\n  decorators:")
            for value in info["decorators"]:
                print(f"    - {value}")

            print("\n  bases:")
            for value in info["bases"] or ["<none>"]:
                print(f"    - {value}")

            print("\n  fields:")
            for value in info["fields"] or ["<none>"]:
                print(f"    - {value}")

            print("\n  methods:")
            for value in info["methods"] or ["<none>"]:
                print(f"    - {value}")

    print("\n" + "=" * 80)
    print("END OF STRUCTURAL COMPARISON")
    print("=" * 80)


if __name__ == "__main__":
    main()

    
