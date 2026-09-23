
from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")
PRODUCTION_ROOTS = [
    ROOT / "acquisition",
]


def is_historical_or_generated(path: Path) -> bool:
    """
    Exclude historical/generated Python files from production repair.
    """
    if "__pycache__" in path.parts:
        return True

    stem = path.stem

    # Historical numbered files: name1.py, name2.py, ...
    if re.search(r"\d+$", stem):
        return True

    # Historical generation files: name_G1.py, name_G2.py, ...
    if re.search(r"_G\d+$", stem):
        return True

    return False


def is_production_file(path: Path) -> bool:
    """
    Return True only for production Python files.

    Tests, audit scripts, repair scripts and generated/cache
    material are intentionally excluded.
    """
    if path.suffix != ".py":
        return False

    if is_historical_or_generated(path):
        return False

    parts = set(path.parts)

    if "tests" in parts:
        return False

    if "scripts" in parts:
        return False

    return True


def production_python_files() -> list[Path]:
    """
    Discover production Python files under acquisition/.
    """
    files: list[Path] = []

    for root in PRODUCTION_ROOTS:
        if not root.exists():
            continue

        for path in root.rglob("*.py"):
            if is_production_file(path):
                files.append(path)

    return sorted(files)


def parse(path: Path) -> ast.AST:
    """
    Parse a Python file before modifying it.
    """
    return ast.parse(
        path.read_text(encoding="utf-8"),
        filename=str(path),
    )


def validate_http_downloader() -> None:
    """
    Confirm that HTTPDownloader is the actual canonical implementation.
    """
    path = (
        ROOT
        / "acquisition"
        / "downloaders"
        / "http_downloader.py"
    )

    if not path.exists():
        raise RuntimeError(
            f"Expected downloader file does not exist: {path}"
        )

    tree = parse(path)

    classes = [
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    ]

    if "HTTPDownloader" not in classes:
        raise RuntimeError(
            "Canonical class HTTPDownloader was not found."
        )

    if "HttpDownloader" in classes:
        raise RuntimeError(
            "A competing HttpDownloader class exists. "
            "Repair aborted."
        )

    print("Canonical implementation : HTTPDownloader")
    print("Canonical downloader validation : PASS")


def find_stale_references() -> list[tuple[Path, int, str]]:
    """
    Find exact production references to the stale identifier.
    """
    matches: list[tuple[Path, int, str]] = []

    for path in production_python_files():
        text = path.read_text(encoding="utf-8")

        for lineno, line in enumerate(text.splitlines(), start=1):
            if re.search(r"\bHttpDownloader\b", line):
                matches.append(
                    (
                        path,
                        lineno,
                        line.rstrip(),
                    )
                )

    return matches


def repair_file(path: Path) -> bool:
    """
    Replace only the stale identifier.

    The canonical downloader implementation itself is explicitly
    excluded from repair.
    """
    downloader_path = (
        ROOT
        / "acquisition"
        / "downloaders"
        / "http_downloader.py"
    )

    if path.resolve() == downloader_path.resolve():
        return False

    text = path.read_text(encoding="utf-8")

    # Identifier-level replacement only.
    repaired = re.sub(
        r"\bHttpDownloader\b",
        "HTTPDownloader",
        text,
    )

    if repaired == text:
        return False

    # Validate the resulting source before writing.
    ast.parse(
        repaired,
        filename=str(path),
    )

    path.write_text(
        repaired,
        encoding="utf-8",
    )

    return True


def main() -> None:
    print("=" * 100)
    print(
        "BATCH 5H-5E-13R-4S-3 — "
        "HTTP DOWNLOADER COMPATIBILITY REPAIR"
    )
    print("=" * 100)

    print()
    print("1. VALIDATE CANONICAL DOWNLOADER")
    print("-" * 100)

    validate_http_downloader()

    print()
    print("2. DISCOVER PRODUCTION FILES")
    print("-" * 100)

    files = production_python_files()

    print(
        f"Production acquisition Python files : {len(files)}"
    )

    print()
    print("3. DISCOVER STALE REFERENCES")
    print("-" * 100)

    before = find_stale_references()

    print(
        f"Stale HttpDownloader references before repair : "
        f"{len(before)}"
    )

    for path, lineno, line in before:
        print(
            f"  {path.relative_to(ROOT)}:{lineno}: {line}"
        )

    if not before:
        print("No stale references found.")
        print()
        print("=" * 100)
        print(
            "BATCH 5H-5E-13R-4S-3 — RESULT: "
            "NO REPAIR REQUIRED"
        )
        print("=" * 100)
        return

    print()
    print("4. APPLY MINIMAL CALLER REPAIR")
    print("-" * 100)

    changed: list[Path] = []

    for path in files:
        if repair_file(path):
            changed.append(path)

    print(
        f"Changed production files : {len(changed)}"
    )

    for path in changed:
        print(
            f"  {path.relative_to(ROOT)}"
        )

    print()
    print("5. POST-REPAIR SYNTAX VALIDATION")
    print("-" * 100)

    for path in changed:
        parse(path)

    print("Changed-file AST validation : PASS")

    print()
    print("6. POST-REPAIR STALE REFERENCE AUDIT")
    print("-" * 100)

    after = find_stale_references()

    print(
        f"Stale HttpDownloader references after repair : "
        f"{len(after)}"
    )

    if after:
        for path, lineno, line in after:
            print(
                f"  {path.relative_to(ROOT)}:{lineno}: {line}"
            )

        raise RuntimeError(
            "Stale HttpDownloader references remain."
        )

    print("Stale-reference elimination : PASS")

    print()
    print("7. CANONICAL HTTPDOWNLOADER PRESERVATION")
    print("-" * 100)

    downloader_path = (
        ROOT
        / "acquisition"
        / "downloaders"
        / "http_downloader.py"
    )

    downloader_tree = parse(downloader_path)

    downloader_classes = [
        node.name
        for node in downloader_tree.body
        if isinstance(node, ast.ClassDef)
    ]

    if "HTTPDownloader" not in downloader_classes:
        raise RuntimeError(
            "HTTPDownloader disappeared after repair."
        )

    if "HttpDownloader" in downloader_classes:
        raise RuntimeError(
            "Unexpected HttpDownloader class detected."
        )

    print("HTTPDownloader preserved : PASS")
    print("http_downloader.py modified : NO")

    print()
    print("=" * 100)
    print(
        "BATCH 5H-5E-13R-4S-3 — RESULT: PASS"
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
