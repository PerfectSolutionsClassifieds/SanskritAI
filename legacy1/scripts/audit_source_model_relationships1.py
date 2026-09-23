
from __future__ import annotations

from pathlib import Path
import re


ROOT = Path("/content/SanskritAI")


MODEL_NAMES = (
    "CorpusSource",
    "CanonicalSource",
    "LexicalSource",
    "MonierWilliamsSource",
)


TARGET_FILES = [
    ROOT / "acquisition/models/acquisition_manifest.py",
    ROOT / "acquisition/models/acquisition_result.py",
    ROOT / "acquisition/sources/monier_williams_manifest.py",
    ROOT / "acquisition/sources/monier_williams.py",
    ROOT / "acquisition/lexical/monier_williams/monier_williams_source.py",
    ROOT / "acquisition/lexical/monier_williams/monier_williams_acquisition_service.py",
    ROOT / "acquisition/lexical/monier_williams/monier_williams_source_pipeline.py",
    ROOT / "domain/lexical/adapters/monier_williams_mapper.py",
    ROOT / "domain/lexical/lexical_source.py",
    ROOT / "lexical/models/lexical_source.py",
    ROOT / "acquisition/knowledge/models/canonical_source.py",
]


def main():
    print("=" * 80)
    print("SanskritAI — SOURCE MODEL RELATIONSHIP AUDIT")
    print("=" * 80)

    for path in TARGET_FILES:
        print("\n" + "-" * 80)
        print(path.relative_to(ROOT))
        print("-" * 80)

        if not path.exists():
            print("FILE NOT FOUND")
            continue

        lines = path.read_text(encoding="utf-8").splitlines()

        found = False

        for number, line in enumerate(lines, start=1):
            if any(
                re.search(
                    rf"\b{re.escape(name)}\b",
                    line,
                )
                for name in MODEL_NAMES
            ):
                print(f"{number:5}: {line.rstrip()}")
                found = True

        if not found:
            print("No target source-model references.")

    print("\n" + "=" * 80)
    print("END OF RELATIONSHIP AUDIT")
    print("=" * 80)


if __name__ == "__main__":
    main()

    
