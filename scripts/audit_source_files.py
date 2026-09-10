
from pathlib import Path


ROOT = Path("/content/SanskritAI")


KEYWORDS = (
    "source",
    "canonical",
    "lexical",
)


def main():
    print("=" * 80)
    print("SanskritAI — SOURCE-RELATED FILE AUDIT")
    print("=" * 80)

    matches = []

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue

        if any(part in {".git", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue

        name = path.name.lower()

        if any(keyword in name for keyword in KEYWORDS):
            matches.append(path)

    for path in matches:
        print(path.relative_to(ROOT))

    print("\n" + "=" * 80)
    print(f"TOTAL SOURCE-RELATED FILES: {len(matches)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
    
