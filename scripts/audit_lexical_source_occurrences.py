from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")

NUMBERED_FILE_RE = re.compile(r".*\d+\.py$")
GENERATED_COPY_RE = re.compile(r".*_G\d+\.py$")


def excluded(path: Path) -> bool:
    parts = {p.lower() for p in path.parts}

    if "tests" in parts:
        return True

    if "__pycache__" in parts:
        return True

    if NUMBERED_FILE_RE.match(path.name):
        return True

    if GENERATED_COPY_RE.match(path.name):
        return True

    return False


def main():
    print("=" * 90)
    print("SANSKRITAI — LEXICALSOURCE EXACT OCCURRENCE AUDIT")
    print("=" * 90)
    print()

    matches = []

    for path in ROOT.rglob("*.py"):
        if excluded(path):
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue

        for lineno, line in enumerate(lines, start=1):
            if "LexicalSource" not in line:
                continue

            matches.append(
                (
                    str(path.relative_to(ROOT)),
                    lineno,
                    line.strip(),
                )
            )

    for rel, lineno, line in matches:
        print(f"{rel}:{lineno}")
        print(f"    {line}")

    print()
    print("=" * 90)
    print(f"TOTAL EXACT 'LexicalSource' OCCURRENCES: {len(matches)}")
    print("=" * 90)
    print()
    print("Excluded:")
    print("  * tests/")
    print("  * __pycache__/")
    print("  * *<number>.py")
    print("  * *_G<number>.py")
    print()
    print("AUDIT COMPLETE — NO FILES MODIFIED")


if __name__ == "__main__":
    main()
