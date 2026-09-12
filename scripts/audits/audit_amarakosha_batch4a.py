
from __future__ import annotations

import ast
import json
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")
AMARAKOSHA_ROOT = ROOT / "amarakosha"
TEST_ROOT = ROOT / "tests"

OUTPUT_DIR = ROOT / "_audit"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_PATH = OUTPUT_DIR / "amarakosha_batch4a_structure.json"


# ---------------------------------------------------------------------
# Historical / duplicate exclusion policy
# ---------------------------------------------------------------------

def is_excluded_python_file(path: Path) -> bool:
    """
    Ignore historical numbered files such as:
        foo1.py
        foo2.py
        monier_williams_mapper4.py

    Also ignore:
        *_G123.py
        tests
        __pycache__
    """
    name = path.name

    if name.startswith("."):
        return True

    if name == "__pycache__":
        return True

    if re.search(r"_G\d+\.py$", name):
        return True

    if re.search(r"\d+\.py$", name):
        return True

    return False


def active_python_files(root: Path) -> list[Path]:
    if not root.exists():
        return []

    files = []

    for path in root.rglob("*.py"):
        if is_excluded_python_file(path):
            continue

        if "__pycache__" in path.parts:
            continue

        files.append(path)

    return sorted(files)


# ---------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------

def safe_parse(path: Path):
    try:
        return ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except Exception as exc:
        return {
            "error": repr(exc),
        }


def dotted_name(node):
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)

        if parent:
            return f"{parent}.{node.attr}"

        return node.attr

    return None


def class_bases(node: ast.ClassDef) -> list[str]:
    result = []

    for base in node.bases:
        name = dotted_name(base)

        if name:
            result.append(name)

    return result


def imported_names(tree) -> list[str]:
    imports = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    alias.name
                )

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                imports.append(
                    f"{module}.{alias.name}"
                )

    return sorted(set(imports))


def defined_classes(tree) -> list[dict]:
    classes = []

    for node in ast.walk(tree):

        if not isinstance(node, ast.ClassDef):
            continue

        classes.append(
            {
                "name": node.name,
                "line": node.lineno,
                "bases": class_bases(node),
                "methods": sorted(
                    child.name
                    for child in node.body
                    if isinstance(
                        child,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef,
                        ),
                    )
                ),
            }
        )

    return classes


def defined_functions(tree) -> list[dict]:
    functions = []

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            functions.append(
                {
                    "name": node.name,
                    "line": node.lineno,
                }
            )

    return functions


def constructor_calls(tree) -> list[dict]:
    calls = []

    for node in ast.walk(tree):

        if not isinstance(node, ast.Call):
            continue

        name = dotted_name(node.func)

        if not name:
            continue

        if (
            "Amarak" in name
            or "Synset" in name
            or "Varga" in name
            or "Canonical" in name
            or "DictionaryEntry" in name
            or "DictionarySense" in name
        ):
            calls.append(
                {
                    "name": name,
                    "line": node.lineno,
                }
            )

    return calls


# ---------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------

def audit():

    print("=" * 80)
    print("BATCH 4A — AMARAKOSHA EXISTING IMPLEMENTATION AUDIT")
    print("=" * 80)
    print()

    print(f"Repository : {ROOT}")
    print(f"Amarakosha : {AMARAKOSHA_ROOT}")
    print()

    if not AMARAKOSHA_ROOT.exists():
        print("ERROR: amarakosha/ directory does not exist.")
        return

    files = active_python_files(AMARAKOSHA_ROOT)

    print(f"Active Amarakośa Python files: {len(files)}")
    print()

    report = {
        "repository": str(ROOT),
        "amarakosha_root": str(AMARAKOSHA_ROOT),
        "files": [],
        "summary": {
            "python_files": len(files),
            "classes": 0,
            "functions": 0,
            "constructor_calls": 0,
        },
    }

    for path in files:

        relative = path.relative_to(ROOT)

        tree = safe_parse(path)

        if isinstance(tree, dict) and "error" in tree:

            item = {
                "file": str(relative),
                "parse_error": tree["error"],
            }

            report["files"].append(item)

            print(f"[PARSE ERROR] {relative}")
            print(f"    {tree['error']}")
            continue

        classes = defined_classes(tree)
        functions = defined_functions(tree)
        imports = imported_names(tree)
        constructors = constructor_calls(tree)

        item = {
            "file": str(relative),
            "classes": classes,
            "functions": functions,
            "imports": imports,
            "constructor_calls": constructors,
        }

        report["files"].append(item)

        report["summary"]["classes"] += len(classes)
        report["summary"]["functions"] += len(functions)
        report["summary"]["constructor_calls"] += len(constructors)

        print("-" * 80)
        print(relative)

        if classes:
            print("  CLASSES:")
            for cls in classes:
                print(
                    f"    {cls['name']}"
                    f"  bases={cls['bases']}"
                )

        if functions:
            print("  FUNCTIONS:")
            for fn in functions:
                print(
                    f"    {fn['name']}"
                    f"  line={fn['line']}"
                )

        if constructors:
            print("  RELEVANT CONSTRUCTORS:")
            for call in constructors:
                print(
                    f"    {call['name']}"
                    f"  line={call['line']}"
                )

        relevant_imports = [
            item
            for item in imports
            if (
                "canonical" in item.lower()
                or "lexical" in item.lower()
                or "amarak" in item.lower()
                or "dictionary" in item.lower()
                or "acquisition" in item.lower()
                or "domain" in item.lower()
            )
        ]

        if relevant_imports:
            print("  RELEVANT IMPORTS:")
            for item in relevant_imports:
                print(f"    {item}")

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(
        f"Python files       : "
        f"{report['summary']['python_files']}"
    )

    print(
        f"Classes            : "
        f"{report['summary']['classes']}"
    )

    print(
        f"Functions          : "
        f"{report['summary']['functions']}"
    )

    print(
        f"Relevant calls     : "
        f"{report['summary']['constructor_calls']}"
    )

    REPORT_PATH.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print(f"[REPORT] {REPORT_PATH}")
    print()


if __name__ == "__main__":
    audit()
