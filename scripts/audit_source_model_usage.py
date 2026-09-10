
from __future__ import annotations

from pathlib import Path
import re


ROOT = Path("/content/SanskritAI")


TARGET_NAMES = (
    "CorpusSource",
    "CanonicalSource",
    "LexicalSource",
    "MonierWilliamsSource",
)


EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "sanskritai.egg-info",
}


EXCLUDED_PREFIXES = (
    "tests/",
)


def iter_python_files(root: Path):
    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root).as_posix()

        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue

        if relative.startswith(EXCLUDED_PREFIXES):
            continue

        yield path


def classify_line(line: str):
    stripped = line.strip()

    if stripped.startswith("from "):
        return "IMPORT"

    if stripped.startswith("import "):
        return "IMPORT"

    if re.search(r"\bclass\s+(CorpusSource|CanonicalSource|LexicalSource|MonierWilliamsSource)\b", stripped):
        return "DEFINITION"

    if re.search(
        r"\b(CorpusSource|CanonicalSource|LexicalSource|MonierWilliamsSource)\s*\(",
        stripped,
    ):
        return "CONSTRUCTION"

    if "." in stripped:
        return "ATTRIBUTE_OR_METHOD"

    return "REFERENCE"


def main():
    print("=" * 80)
    print("SanskritAI — SOURCE MODEL CONSUMER AUDIT")
    print("=" * 80)

    total = 0

    for path in iter_python_files(ROOT):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        matches = []

        for number, line in enumerate(text.splitlines(), start=1):
            if not any(
                re.search(
                    rf"\b{re.escape(name)}\b",
                    line,
                )
                for name in TARGET_NAMES
            ):
                continue

            kind = classify_line(line)

            matches.append(
                (
                    number,
                    kind,
                    line.strip(),
                )
            )

        if not matches:
            continue

        print("\n" + "-" * 80)
        print(path.relative_to(ROOT))
        print("-" * 80)

        for number, kind, line in matches:
            print(f"{number:5} [{kind:20}] {line}")

        total += len(matches)

    print("\n" + "=" * 80)
    print(f"TOTAL SOURCE MODEL REFERENCES: {total}")
    print("=" * 80)


if __name__ == "__main__":
    main()
    
