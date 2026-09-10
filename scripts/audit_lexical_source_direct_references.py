from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")

# Historical / duplicate files to ignore.
NUMBERED_FILE_RE = re.compile(r".*\d+\.py$")
GENERATED_COPY_RE = re.compile(r".*_G\d+\.py$")


def is_excluded(path: Path) -> bool:
    parts = {p.lower() for p in path.parts}

    if "tests" in parts:
        return True

    if "__pycache__" in parts:
        return True

    name = path.name

    # Ignore files such as foo1.py, foo2.py, ...
    if NUMBERED_FILE_RE.match(name):
        return True

    # Ignore generated copies such as foo_G1.py.
    if GENERATED_COPY_RE.match(name):
        return True

    return False


def production_files():
    for path in ROOT.rglob("*.py"):
        if not is_excluded(path):
            yield path


def dotted_name(node):
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        if parent:
            return f"{parent}.{node.attr}"

    return None


def source_lines(path: Path):
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return []


def main():
    targets = {
        "DOMAIN":
            "domain.lexical.lexical_source.LexicalSource",
        "LEXICAL_MODEL":
            "lexical.models.lexical_source.LexicalSource",
    }

    results = {
        "DOMAIN": [],
        "LEXICAL_MODEL": [],
    }

    print("=" * 90)
    print("SANSKRITAI — LEXICALSOURCE DIRECT REFERENCE AUDIT")
    print("=" * 90)
    print()
    print("This audit intentionally performs NO semantic inference.")
    print("It reports direct source-level evidence only.")
    print()

    for path in production_files():
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except Exception:
            continue

        rel = path.relative_to(ROOT)

        lines = source_lines(path)

        def record(target, kind, lineno):
            snippet = lines[lineno - 1].strip() if 0 < lineno <= len(lines) else ""
            results[target].append(
                (str(rel), lineno, kind, snippet)
            )

        for node in ast.walk(tree):

            # ---------------------------------------------------------
            # Direct imports
            # ---------------------------------------------------------
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""

                for alias in node.names:
                    imported = alias.name
                    bound_name = alias.asname or imported

                    if imported != "LexicalSource":
                        continue

                    if module.endswith(
                        "domain.lexical.lexical_source"
                    ):
                        record(
                            "DOMAIN",
                            f"IMPORT: {module} -> {bound_name}",
                            node.lineno,
                        )

                    elif module.endswith(
                        "lexical.models.lexical_source"
                    ):
                        record(
                            "LEXICAL_MODEL",
                            f"IMPORT: {module} -> {bound_name}",
                            node.lineno,
                        )

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name

                    if module.endswith(
                        "domain.lexical.lexical_source"
                    ):
                        record(
                            "DOMAIN",
                            f"IMPORT: {module}",
                            node.lineno,
                        )

                    elif module.endswith(
                        "lexical.models.lexical_source"
                    ):
                        record(
                            "LEXICAL_MODEL",
                            f"IMPORT: {module}",
                            node.lineno,
                        )

            # ---------------------------------------------------------
            # Constructor / bare LexicalSource references
            # ---------------------------------------------------------
            elif isinstance(node, ast.Call):
                name = dotted_name(node.func)

                if name == "LexicalSource":
                    record(
                        "DOMAIN",
                        "CONSTRUCTOR/REFERENCE: LexicalSource(...)",
                        node.lineno,
                    )

            elif isinstance(node, ast.Name):
                if node.id == "LexicalSource":
                    record(
                        "DOMAIN",
                        "NAME REFERENCE: LexicalSource",
                        node.lineno,
                    )

            # ---------------------------------------------------------
            # String annotations / forward references
            # ---------------------------------------------------------
            elif isinstance(node, ast.Constant):
                if isinstance(node.value, str):
                    value = node.value

                    if "domain.lexical.lexical_source.LexicalSource" in value:
                        record(
                            "DOMAIN",
                            "STRING ANNOTATION",
                            node.lineno,
                        )

                    if "lexical.models.lexical_source.LexicalSource" in value:
                        record(
                            "LEXICAL_MODEL",
                            "STRING ANNOTATION",
                            node.lineno,
                        )

        # -------------------------------------------------------------
        # Raw textual fallback for exact implementation paths.
        # This catches cases AST does not expose conveniently.
        # -------------------------------------------------------------
        for lineno, line in enumerate(lines, start=1):
            stripped = line.strip()

            if (
                "domain.lexical.lexical_source" in stripped
                and "LexicalSource" in stripped
            ):
                record(
                    "DOMAIN",
                    "TEXTUAL PATH REFERENCE",
                    lineno,
                )

            if (
                "lexical.models.lexical_source" in stripped
                and "LexicalSource" in stripped
            ):
                record(
                    "LEXICAL_MODEL",
                    "TEXTUAL PATH REFERENCE",
                    lineno,
                )

    # Deduplicate.
    for key in results:
        results[key] = sorted(set(results[key]))

    for key, title in [
        ("DOMAIN", "domain.lexical.lexical_source.LexicalSource"),
        ("LEXICAL_MODEL", "lexical.models.lexical_source.LexicalSource"),
    ]:
        print()
        print("-" * 90)
        print(title)
        print("-" * 90)

        if not results[key]:
            print("  (no direct references found)")
            continue

        for rel, lineno, kind, snippet in results[key]:
            print(f"  {rel}:{lineno}")
            print(f"      {kind}")
            if snippet:
                print(f"      {snippet}")

        print()
        print(f"  TOTAL DIRECT EVIDENCE: {len(results[key])}")

    print()
    print("=" * 90)
    print("SUMMARY")
    print("=" * 90)
    print(
        f"DOMAIN LexicalSource evidence       : {len(results['DOMAIN'])}"
    )
    print(
        f"LEXICAL MODEL LexicalSource evidence: "
        f"{len(results['LEXICAL_MODEL'])}"
    )

    print()
    print("IMPORTANT:")
    print("Zero evidence here means only that no direct source-level")
    print("reference was detected by this audit.")
    print("It does NOT by itself prove that a model is unused.")
    print()
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 90)


if __name__ == "__main__":
    main()
