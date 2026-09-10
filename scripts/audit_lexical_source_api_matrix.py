from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGETS = {
    "DOMAIN":
        ROOT / "domain/lexical/lexical_source.py",
    "LEXICAL_MODEL":
        ROOT / "lexical/models/lexical_source.py",
}


def annotation(node):
    if node is None:
        return None

    try:
        return ast.unparse(node)
    except Exception:
        return None


def inspect(path: Path):
    result = {
        "fields": {},
        "methods": {},
        "properties": {},
        "bases": [],
        "decorators": [],
    }

    tree = ast.parse(path.read_text(encoding="utf-8"))

    cls = None

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            if node.name == "LexicalSource":
                cls = node
                break

    if cls is None:
        return result

    result["bases"] = [
        annotation(base)
        for base in cls.bases
    ]

    result["decorators"] = [
        annotation(dec)
        for dec in cls.decorator_list
    ]

    for item in cls.body:

        if isinstance(item, ast.AnnAssign):
            if isinstance(item.target, ast.Name):
                result["fields"][item.target.id] = (
                    annotation(item.annotation)
                )

        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    result["fields"][target.id] = "unannotated"

        elif isinstance(
            item,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            decorators = [
                annotation(d)
                for d in item.decorator_list
            ]

            returns = annotation(item.returns)

            args = []

            for arg in item.args.args:
                args.append(
                    (
                        arg.arg,
                        annotation(arg.annotation),
                    )
                )

            if "property" in decorators:
                result["properties"][item.name] = (
                    returns
                )
            else:
                result["methods"][item.name] = {
                    "returns": returns,
                    "args": args,
                }

    return result


def main():
    data = {}

    for label, path in TARGETS.items():
        data[label] = inspect(path)

    print("=" * 100)
    print("SANSKRITAI — LEXICALSOURCE API COMPARISON MATRIX")
    print("=" * 100)

    for label in ("DOMAIN", "LEXICAL_MODEL"):

        print()
        print("-" * 100)
        print(label)
        print("-" * 100)

        print()
        print("BASES")
        for base in data[label]["bases"]:
            print(f"  {base}")

        print()
        print("DECORATORS")
        for dec in data[label]["decorators"]:
            print(f"  {dec}")

        print()
        print("FIELDS")
        for name, typ in data[label]["fields"].items():
            print(f"  {name}: {typ}")

        print()
        print("PROPERTIES")
        for name, typ in data[label]["properties"].items():
            print(f"  {name} -> {typ}")

        print()
        print("METHODS")
        for name, info in data[label]["methods"].items():
            args = ", ".join(
                f"{n}: {t or 'Any'}"
                for n, t in info["args"]
            )

            print(
                f"  {name}({args})"
                f" -> {info['returns'] or 'None'}"
            )

    print()
    print("=" * 100)
    print("FIELD OVERLAP")
    print("=" * 100)

    domain_fields = set(
        data["DOMAIN"]["fields"]
    )

    model_fields = set(
        data["LEXICAL_MODEL"]["fields"]
    )

    print(
        "COMMON FIELDS:"
    )

    for name in sorted(
        domain_fields & model_fields
    ):
        print(f"  {name}")

    print()
    print("DOMAIN ONLY:")

    for name in sorted(
        domain_fields - model_fields
    ):
        print(f"  {name}")

    print()
    print("LEXICAL MODEL ONLY:")

    for name in sorted(
        model_fields - domain_fields
    ):
        print(f"  {name}")

    domain_props = set(
        data["DOMAIN"]["properties"]
    )

    model_props = set(
        data["LEXICAL_MODEL"]["properties"]
    )

    print()
    print("=" * 100)
    print("PROPERTY OVERLAP")
    print("=" * 100)

    print("COMMON:")
    for name in sorted(
        domain_props & model_props
    ):
        print(f"  {name}")

    print()
    print("DOMAIN ONLY:")
    for name in sorted(
        domain_props - model_props
    ):
        print(f"  {name}")

    print()
    print("LEXICAL MODEL ONLY:")
    for name in sorted(
        model_props - domain_props
    ):
        print(f"  {name}")

    print()
    print("=" * 100)
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 100)


if __name__ == "__main__":
    main()
