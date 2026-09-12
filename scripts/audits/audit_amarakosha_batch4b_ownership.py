
from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")

SEARCH_ROOTS = [
    ROOT / "amarakosha",
    ROOT / "acquisition",
    ROOT / "domain",
    ROOT / "lexical",
    ROOT / "models",
    ROOT / "core",
    ROOT / "tests",
]


# ---------------------------------------------------------------------
# Exclusions
# ---------------------------------------------------------------------

def excluded(path: Path) -> bool:

    name = path.name

    if "__pycache__" in path.parts:
        return True

    if name.startswith("."):
        return True

    if re.search(r"_G\d+\.py$", name):
        return True

    if re.search(r"\d+\.py$", name):
        return True

    return False


def python_files():

    seen = set()

    for root in SEARCH_ROOTS:

        if not root.exists():
            continue

        for path in root.rglob("*.py"):

            if excluded(path):
                continue

            if path in seen:
                continue

            seen.add(path)
            yield path


# ---------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------

def dotted_name(node):

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):

        parent = dotted_name(node.value)

        if parent:
            return f"{parent}.{node.attr}"

        return node.attr

    return None


def source_text(path):

    try:
        return path.read_text(
            encoding="utf-8"
        )
    except Exception:
        return ""


# ---------------------------------------------------------------------
# Symbol categories
# ---------------------------------------------------------------------

TARGET_SYMBOLS = {
    "Synset",
    "SynsetRecord",
    "SynsetBuilder",
    "Varga",
    "VargaRecord",
    "VargaBuilder",
    "Amarakosha",
    "AmarakoshaParser",
    "AmarakoshaImporter",
    "AmarakoshaRegistry",
    "AmarakoshaRepository",
    "CanonicalDictionaryEntry",
    "CanonicalDictionarySense",
    "CanonicalLexicon",
    "CanonicalKnowledgeRepository",
    "CanonicalSource",
    "LexicalRecord",
    "Lexeme",
    "DictionaryEntry",
    "DictionarySense",
}


def symbol_from_name(name):

    if not name:
        return None

    final = name.split(".")[-1]

    if final in TARGET_SYMBOLS:
        return final

    return None


# ---------------------------------------------------------------------
# AST analysis
# ---------------------------------------------------------------------

def analyze(path):

    text = source_text(path)

    if not text:
        return None

    try:
        tree = ast.parse(
            text,
            filename=str(path),
        )
    except Exception as exc:

        return {
            "file": str(path.relative_to(ROOT)),
            "parse_error": repr(exc),
        }

    result = {
        "file": str(path.relative_to(ROOT)),
        "imports": [],
        "definitions": [],
        "constructors": [],
        "annotations": [],
        "returns": [],
        "symbol_mentions": [],
    }

    for node in ast.walk(tree):

        # -------------------------------------------------------------
        # Imports
        # -------------------------------------------------------------

        if isinstance(node, ast.Import):

            for alias in node.names:

                symbol = symbol_from_name(alias.name)

                if symbol:
                    result["imports"].append(
                        {
                            "symbol": symbol,
                            "module": alias.name,
                            "line": node.lineno,
                        }
                    )

        elif isinstance(node, ast.ImportFrom):

            module = node.module or ""

            for alias in node.names:

                full_name = f"{module}.{alias.name}"

                symbol = symbol_from_name(
                    full_name
                )

                if symbol:
                    result["imports"].append(
                        {
                            "symbol": symbol,
                            "module": module,
                            "line": node.lineno,
                        }
                    )

        # -------------------------------------------------------------
        # Definitions
        # -------------------------------------------------------------

        elif isinstance(node, ast.ClassDef):

            if node.name in TARGET_SYMBOLS:

                result["definitions"].append(
                    {
                        "symbol": node.name,
                        "line": node.lineno,
                        "bases": [
                            dotted_name(base)
                            for base in node.bases
                        ],
                    }
                )

        # -------------------------------------------------------------
        # Calls / constructors
        # -------------------------------------------------------------

        elif isinstance(node, ast.Call):

            name = dotted_name(node.func)
            symbol = symbol_from_name(name)

            if symbol:

                result["constructors"].append(
                    {
                        "symbol": symbol,
                        "call": name,
                        "line": node.lineno,
                    }
                )

        # -------------------------------------------------------------
        # Type annotations
        # -------------------------------------------------------------

        elif isinstance(node, ast.AnnAssign):

            annotation = dotted_name(
                node.annotation
            )

            symbol = symbol_from_name(
                annotation
            )

            if symbol:

                result["annotations"].append(
                    {
                        "symbol": symbol,
                        "line": node.lineno,
                    }
                )

        elif isinstance(node, ast.arg):

            if node.annotation:

                annotation = dotted_name(
                    node.annotation
                )

                symbol = symbol_from_name(
                    annotation
                )

                if symbol:

                    result["annotations"].append(
                        {
                            "symbol": symbol,
                            "line": node.lineno,
                        }
                    )

        # -------------------------------------------------------------
        # Return annotations
        # -------------------------------------------------------------

        elif isinstance(node, ast.FunctionDef):

            if node.returns:

                annotation = dotted_name(
                    node.returns
                )

                symbol = symbol_from_name(
                    annotation
                )

                if symbol:

                    result["returns"].append(
                        {
                            "symbol": symbol,
                            "line": node.lineno,
                        }
                    )

    # Deduplicate
    for key in result:
        if isinstance(result[key], list):
            result[key] = sorted(
                result[key],
                key=lambda x: (
                    x.get("symbol", ""),
                    x.get("line", 0),
                ),
            )

    return result


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("=" * 90)
    print("BATCH 4B — AMARAKOSHA CONSTRUCTION / OWNERSHIP AUDIT")
    print("=" * 90)
    print()

    all_results = []

    for path in python_files():

        result = analyze(path)

        if result is None:
            continue

        has_relevant_usage = any(
            result[key]
            for key in (
                "imports",
                "definitions",
                "constructors",
                "annotations",
                "returns",
            )
        )

        if not has_relevant_usage:
            continue

        all_results.append(result)

    # -------------------------------------------------------------
    # Definitions
    # -------------------------------------------------------------

    print("=" * 90)
    print("SYMBOL DEFINITIONS")
    print("=" * 90)

    for result in all_results:

        for item in result["definitions"]:

            print(
                f"{item['symbol']:35}"
                f" {result['file']}"
                f":{item['line']}"
            )

    print()

    # -------------------------------------------------------------
    # Constructors
    # -------------------------------------------------------------

    print("=" * 90)
    print("ACTUAL CONSTRUCTORS / CALL SITES")
    print("=" * 90)

    for result in all_results:

        for item in result["constructors"]:

            print(
                f"{item['symbol']:35}"
                f" {result['file']}"
                f":{item['line']}"
            )

    print()

    # -------------------------------------------------------------
    # Return types
    # -------------------------------------------------------------

    print("=" * 90)
    print("RETURN TYPE OWNERSHIP")
    print("=" * 90)

    for result in all_results:

        for item in result["returns"]:

            print(
                f"{item['symbol']:35}"
                f" {result['file']}"
                f":{item['line']}"
            )

    print()

    # -------------------------------------------------------------
    # Annotation ownership
    # -------------------------------------------------------------

    print("=" * 90)
    print("TYPE ANNOTATIONS")
    print("=" * 90)

    for result in all_results:

        for item in result["annotations"]:

            print(
                f"{item['symbol']:35}"
                f" {result['file']}"
                f":{item['line']}"
            )

    print()

    # -------------------------------------------------------------
    # Imports
    # -------------------------------------------------------------

    print("=" * 90)
    print("RELEVANT IMPORTS")
    print("=" * 90)

    for result in all_results:

        for item in result["imports"]:

            print(
                f"{item['symbol']:35}"
                f" {result['file']}"
                f":{item['line']}"
                f"  <- {item['module']}"
            )

    print()

    # -------------------------------------------------------------
    # Symbol summary
    # -------------------------------------------------------------

    print("=" * 90)
    print("SYMBOL USAGE SUMMARY")
    print("=" * 90)

    summary = {}

    for result in all_results:

        for key in (
            "imports",
            "definitions",
            "constructors",
            "annotations",
            "returns",
        ):

            for item in result[key]:

                symbol = item["symbol"]

                if symbol not in summary:
                    summary[symbol] = {
                        "imports": 0,
                        "definitions": 0,
                        "constructors": 0,
                        "annotations": 0,
                        "returns": 0,
                    }

                summary[symbol][key] += 1

    for symbol in sorted(summary):

        stats = summary[symbol]

        print(
            f"{symbol:35}"
            f" imports={stats['imports']:<3}"
            f" defs={stats['definitions']:<3}"
            f" constructors={stats['constructors']:<3}"
            f" annotations={stats['annotations']:<3}"
            f" returns={stats['returns']:<3}"
        )

    print()
    print("=" * 90)
    print("AUDIT COMPLETE")
    print("=" * 90)


if __name__ == "__main__":
    main()
