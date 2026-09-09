
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Boundary Audit
------------------------------

Read-only architectural audit.

Purpose
-------
Identify active references to:

* MonierWilliamsSourceRecord
* MonierWilliamsRecord
* from_source_record
* from_source_records
* MonierWilliamsParsedEntry

Historical numbered Python files are excluded.

This script does not modify any files.
"""

from pathlib import Path
import re


ROOT = Path("/content/SanskritAI")

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
}

HISTORICAL_PATTERN = re.compile(
    r".*[0-9]+\.py$"
)

PATTERNS = (
    "MonierWilliamsSourceRecord",
    "MonierWilliamsRecord",
    "from_source_record",
    "from_source_records",
    "MonierWilliamsParsedEntry",
)


def active_python_files() -> list[Path]:
    files: list[Path] = []

    for path in ROOT.rglob("*.py"):
        if any(
            excluded in path.parts
            for excluded in EXCLUDED_DIRS
        ):
            continue

        if HISTORICAL_PATTERN.fullmatch(
            path.name
        ):
            continue

        files.append(path)

    return sorted(files)


def audit_pattern(
    pattern: str,
) -> None:

    print()
    print("=" * 80)
    print(f"PATTERN: {pattern}")
    print("=" * 80)

    found = False

    for path in active_python_files():

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except OSError:
            continue

        for line_number, line in enumerate(
            text.splitlines(),
            start=1,
        ):

            if pattern in line:

                found = True

                relative = path.relative_to(ROOT)

                print(
                    f"{relative}:{line_number}:"
                    f" {line.strip()}"
                )

    if not found:
        print("NO ACTIVE REFERENCES FOUND")


def main() -> None:

    print("=" * 80)
    print("SANSKRITAI MONIER-WILLIAMS ARCHITECTURAL AUDIT")
    print("=" * 80)

    print(f"ROOT: {ROOT}")

    files = active_python_files()

    print(
        f"ACTIVE PYTHON FILES: {len(files)}"
    )

    for pattern in PATTERNS:
        audit_pattern(pattern)


if __name__ == "__main__":
    main()
