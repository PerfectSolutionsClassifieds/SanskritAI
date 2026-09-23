from __future__ import annotations

import ast
import re
from pathlib import Path
from collections import defaultdict


ROOT = Path("/content/SanskritAI")


# ---------------------------------------------------------------------------
# Historical / duplicate file filtering
# ---------------------------------------------------------------------------

def is_historical_duplicate(path: Path) -> bool:
    """
    Exclude historical numbered copies such as:

        mapper1.py
        mapper2.py
        source4.py

    Also exclude common generation copies such as:

        canonical_lexicon_G4.py
        source_G2.py
    """
    stem = path.stem

    if re.search(r"\d+$", stem):
        return True

    if re.search(r"_G\d+$", stem, flags=re.IGNORECASE):
        return True

    return False


def is_production_python(path: Path) -> bool:
    if path.suffix != ".py":
        return False

    if "__pycache__" in path.parts:
        return False

    if "tests" in path.parts:
        return False

    if is_historical_duplicate(path):
        return False

    return True


# ---------------------------------------------------------------------------
# Source model classification
# ---------------------------------------------------------------------------

MODEL_OWNERSHIP = {
    ("acquisition.knowledge.models.canonical_source", "CanonicalSource"):
        "CANONICAL PROVENANCE / SOURCE METADATA",

    ("acquisition.models.corpus_source", "CorpusSource"):
        "GENERIC ACQUISITION SOURCE IDENTITY",

    ("domain.lexical.lexical_source", "LexicalSource"):
        "DOMAIN LEXICAL SOURCE IDENTITY",

    ("lexical.models.lexical_source", "LexicalSource"):
        "LEXICAL MODEL SOURCE METADATA",

    ("acquisition.lexical.monier_williams.monier_williams_source",
     "MonierWilliamsSource"):
        "MONIER-WILLIAMS RAW CONTENT CONTRACT",

    ("acquisition.sources.monier_williams",
     "MonierWilliamsSource"):
        "MONIER-WILLIAMS SOURCE METADATA",
}


def module_name(path: Path) -> str:
    relative = path.relative_to(ROOT).with_suffix("")
    return ".".join(relative.parts)


def class_info(node: ast.ClassDef):
    fields = []
    methods = []
    properties = []

    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods.append(item.name)

            for decorator in item.decorator_list:
                if (
                    isinstance(decorator, ast.Name)
                    and decorator.id == "property"
                ):
                    properties.append(item.name)

        elif isinstance(item, ast.AnnAssign):
            if isinstance(item.target, ast.Name):
                fields.append(item.target.id)

        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    fields.append(target.id)

    bases = []
    for base in node.bases:
        try:
            bases.append(ast.unparse(base))
        except Exception:
            bases.append("<unknown>")

    decorators = []
    for decorator in node.decorator_list:
        try:
            decorators.append(ast.unparse(decorator))
        except Exception:
            decorators.append("<unknown>")

    return fields, methods, properties, bases, decorators


# ---------------------------------------------------------------------------
# Scan
# ---------------------------------------------------------------------------

definitions = []

for path in sorted(ROOT.rglob("*.py")):
    if not is_production_python(path):
        continue

    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except Exception:
        continue

    module = module_name(path)

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        key = (module, node.name)

        if key not in MODEL_OWNERSHIP:
            continue

        fields, methods, properties, bases, decorators = class_info(node)

        definitions.append({
            "module": module,
            "name": node.name,
            "path": path,
            "line": node.lineno,
            "ownership": MODEL_OWNERSHIP[key],
            "fields": fields,
            "methods": methods,
            "properties": properties,
            "bases": bases,
            "decorators": decorators,
        })


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

print("=" * 80)
print("SANSKRITAI — PRODUCTION SOURCE MODEL OWNERSHIP AUDIT")
print("=" * 80)

print()
print(f"Production definitions found: {len(definitions)}")

for index, item in enumerate(definitions, start=1):
    print()
    print("-" * 80)
    print(f"[{index}] {item['name']}")
    print(f"Module      : {item['module']}")
    print(f"File        : {item['path']}")
    print(f"Line        : {item['line']}")
    print(f"Ownership   : {item['ownership']}")
    print(
        "Bases       : "
        + (", ".join(item["bases"]) if item["bases"] else "(none)")
    )
    print(
        "Fields      : "
        + (", ".join(item["fields"]) if item["fields"] else "(none)")
    )
    print(
        "Methods     : "
        + (", ".join(item["methods"]) if item["methods"] else "(none)")
    )
    print(
        "Properties  : "
        + (
            ", ".join(item["properties"])
            if item["properties"]
            else "(none)"
        )
    )


# ---------------------------------------------------------------------------
# Concept summary
# ---------------------------------------------------------------------------

grouped = defaultdict(list)

for item in definitions:
    grouped[item["name"]].append(item)


print()
print("=" * 80)
print("CONCEPT SUMMARY")
print("=" * 80)

for name in sorted(grouped):
    items = grouped[name]

    print()
    print(f"{name}: {len(items)} production definition(s)")

    for item in items:
        print(
            f"  - {item['module']} "
            f"-> {item['ownership']}"
        )


print()
print("=" * 80)
print("HISTORICAL / DUPLICATE FILE FILTER")
print("=" * 80)
print()
print("Excluded:")
print("  *<number>.py")
print("  *_G<number>.py")
print("  tests/")
print("  __pycache__/")

print()
print("=" * 80)
print("AUDIT COMPLETE — NO FILES MODIFIED")
print("=" * 80)
