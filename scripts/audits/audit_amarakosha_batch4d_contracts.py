
from __future__ import annotations

import ast
import inspect
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")
AMARAKOSHA = ROOT / "amarakosha"


# ---------------------------------------------------------------------
# Historical / duplicate exclusion
# ---------------------------------------------------------------------

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

    if isinstance(node, ast.Subscript):
        value = dotted_name(node.value)

        if value:
            return value

    return None


def annotation_text(node):

    if node is None:
        return None

    try:
        return ast.unparse(node)
    except Exception:
        return dotted_name(node)


def default_text(node):

    if node is None:
        return None

    try:
        return ast.unparse(node)
    except Exception:
        return "<unparseable>"


def format_arguments(args):

    result = []

    positional = list(args.posonlyargs) + list(args.args)
    defaults = [None] * (
        len(positional) - len(args.defaults)
    ) + list(args.defaults)

    for arg, default in zip(positional, defaults):

        annotation = annotation_text(
            arg.annotation
        )

        value = default_text(default)

        text = arg.arg

        if annotation:
            text += f": {annotation}"

        if value is not None:
            text += f" = {value}"

        result.append(text)

    if args.vararg:

        text = "*" + args.vararg.arg

        if args.vararg.annotation:
            text += (
                ": "
                + annotation_text(
                    args.vararg.annotation
                )
            )

        result.append(text)

    for arg, default in zip(
        args.kwonlyargs,
        args.kw_defaults,
    ):

        annotation = annotation_text(
            arg.annotation
        )

        value = default_text(default)

        text = arg.arg

        if annotation:
            text += f": {annotation}"

        if value is not None:
            text += f" = {value}"

        result.append(text)

    if args.kwarg:

        text = "**" + args.kwarg.arg

        if args.kwarg.annotation:
            text += (
                ": "
                + annotation_text(
                    args.kwarg.annotation
                )
            )

        result.append(text)

    return result


def class_contract(node: ast.ClassDef):

    fields = []
    methods = []

    for child in node.body:

        if isinstance(
            child,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):

            methods.append(
                {
                    "name": child.name,
                    "line": child.lineno,
                    "signature": (
                        child.name
                        + "("
                        + ", ".join(
                            format_arguments(
                                child.args
                            )
                        )
                        + ")"
                    ),
                    "returns": annotation_text(
                        child.returns
                    ),
                }
            )

        elif isinstance(
            child,
            ast.AnnAssign,
        ):

            target = child.target

            if isinstance(
                target,
                ast.Name,
            ):

                fields.append(
                    {
                        "name": target.id,
                        "annotation": annotation_text(
                            child.annotation
                        ),
                        "default": default_text(
                            child.value
                        ),
                        "line": child.lineno,
                    }
                )

    return {
        "name": node.name,
        "line": node.lineno,
        "bases": [
            annotation_text(base)
            for base in node.bases
        ],
        "fields": fields,
        "methods": methods,
    }


def extract_classes(path: Path):

    try:
        text = path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(
            text,
            filename=str(path),
        )

    except Exception as exc:

        return {
            "error": repr(exc)
        }

    return [
        class_contract(node)
        for node in ast.walk(tree)
        if isinstance(
            node,
            ast.ClassDef,
        )
    ]


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("=" * 100)
    print("BATCH 4D — AMARAKOSHA SEMANTIC CONTRACT AUDIT")
    print("=" * 100)
    print()

    if not AMARAKOSHA.exists():

        print(
            "ERROR: amarakosha/ directory does not exist."
        )

        return

    files = sorted(
        path
        for path in AMARAKOSHA.rglob("*.py")
        if not excluded(path)
    )

    target_tokens = (
        "synset",
        "varga",
        "lexeme",
        "record",
        "metadata",
        "parser",
        "importer",
        "registry",
        "builder",
        "validator",
        "kanda",
    )

    for path in files:

        relative = path.relative_to(ROOT)

        classes = extract_classes(path)

        if isinstance(classes, dict):
            print(
                f"[PARSE ERROR] {relative}"
            )
            print(
                f"  {classes['error']}"
            )
            continue

        relevant = []

        for cls in classes:

            name = cls["name"].lower()

            if any(
                token in name
                for token in target_tokens
            ):
                relevant.append(cls)

        if not relevant:
            continue

        print("-" * 100)
        print(relative)

        for cls in relevant:

            print()
            print(
                f"CLASS: {cls['name']}"
                f"  line={cls['line']}"
            )

            print(
                "BASES:"
            )

            for base in cls["bases"]:
                print(
                    f"  {base}"
                )

            if cls["fields"]:

                print(
                    "FIELDS:"
                )

                for field in cls["fields"]:

                    print(
                        f"  {field['name']}"
                        f": {field['annotation']}"
                        f"  default={field['default']}"
                        f"  line={field['line']}"
                    )

            print(
                "METHODS:"
            )

            for method in cls["methods"]:

                print(
                    f"  {method['signature']}"
                    f" -> {method['returns']}"
                    f"  line={method['line']}"
                )

    print()
    print("=" * 100)
    print("BATCH 4D COMPLETE")
    print("=" * 100)
    print()
    print("Production code was not modified.")


if __name__ == "__main__":
    main()
