
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams ParsedEntry Audit
---------------------------------

Read-only audit for the legacy
MonierWilliamsParsedEntry model.

Purpose
-------
Determine whether MonierWilliamsParsedEntry is:

1. production-used,
2. package-exported only,
3. test-only,
4. referenced by documentation,
5. completely unused.

No files are modified.
"""

from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGET = "MonierWilliamsParsedEntry"

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
}


def active_python_files() -> list[Path]:

    result: list[Path] = []

    for path in ROOT.rglob("*.py"):

        if any(
            directory in path.parts
            for directory in EXCLUDED_DIRS
        ):
            continue

        # Ignore historical numbered development copies.
        if path.stem[-1:].isdigit():
            continue

        result.append(path)

    return sorted(result)


def classify(path: Path) -> str:

    parts = path.parts

    if "tests" in parts:
        return "TEST"

    if "acquisition" in parts:
        return "ACQUISITION"

    if "domain" in parts:
        return "DOMAIN"

    if "lexical" in parts:
        return "LEXICAL"

    return "OTHER"


def main() -> None:

    print("=" * 80)
    print("MONIER-WILLIAMS PARSED ENTRY AUDIT")
    print("=" * 80)

    references = []

    for path in active_python_files():

        try:
            lines = path.read_text(
                encoding="utf-8",
                errors="ignore",
            ).splitlines()
        except OSError:
            continue

        for number, line in enumerate(
            lines,
            start=1,
        ):

            if TARGET not in line:
                continue

            references.append(
                (
                    classify(path),
                    path.relative_to(ROOT),
                    number,
                    line.strip(),
                )
            )

    if not references:
        print("NO ACTIVE REFERENCES FOUND")
        return

    for category, path, number, line in references:

        print(
            f"[{category}] "
            f"{path}:{number}: {line}"
        )

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    categories = {}

    for category, *_ in references:
        categories.setdefault(category, 0)
        categories[category] += 1

    for category, count in sorted(
        categories.items()
    ):
        print(
            f"{category:15} {count:4}"
        )


if __name__ == "__main__":
    main()
