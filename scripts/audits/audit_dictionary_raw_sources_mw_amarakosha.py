
from __future__ import annotations

from pathlib import Path
import hashlib


ROOT = Path("/content/SanskritAI").resolve()

SOURCES = {
    "monier_williams": {
        "artifacts": [
            ROOT / "mw.txt",
            ROOT / "mw-meta2.txt",
        ],
        "format": "UTF-8 pseudo-XML/XML dictionary",
        "source_type": "LEXICON",
        "role": "canonical lexical source artifact + format specification",
    },
    "amarakosha": {
        "artifacts": [
            ROOT / "amarakosha.txt",
            ROOT / "data/raw/amarakosha/pdf/amarfin1.pdf",
            ROOT / "data/raw/amarakosha/pdf/amarfin2.pdf",
            ROOT / "data/raw/amarakosha/pdf/amarfin3.pdf",
        ],
        "format": "UTF-8 SCL-derived text + external PDF representations",
        "source_type": "LEXICON",
        "role": "canonical lexical source artifact + external reference representations",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


print("=" * 72)
print("Dictionary raw-source inventory")
print("Monier-Williams + Amarakośa")
print("=" * 72)

for source_id, spec in SOURCES.items():

    print()
    print("-" * 72)
    print(source_id)
    print("-" * 72)

    print(f"source_type : {spec['source_type']}")
    print(f"format      : {spec['format']}")
    print(f"role        : {spec['role']}")

    for artifact in spec["artifacts"]:

        exists = artifact.exists()
        is_file = artifact.is_file() if exists else False

        print()
        print(f"artifact : {artifact}")
        print(f"exists   : {exists}")
        print(f"is_file  : {is_file}")

        if not is_file:
            continue

        print(f"size     : {artifact.stat().st_size}")
        print(f"sha256   : {sha256(artifact)}")

        if artifact.suffix.lower() == ".txt":
            try:
                text = artifact.read_text(encoding="utf-8")

                print("UTF-8    : PASS")
                print(f"lines    : {len(text.splitlines())}")
                print(f"chars    : {len(text)}")

            except UnicodeDecodeError as exc:
                print(f"UTF-8    : FAIL — {exc}")

print()
print("=" * 72)
print("RESULT: PASS — raw dictionary source inventory completed.")
print("No production files modified.")
print("=" * 72)
