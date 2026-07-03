from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def build_dictionary(csv_path: str | Path, output_path: str | Path) -> Path:
    entries = {}
    with Path(csv_path).open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            word = row.get("word", "").strip()
            if not word:
                continue
            entries[word] = {
                "word": word,
                "lemma": row.get("lemma", word).strip(),
                "meaning": row.get("meaning", "").strip(),
                "pos": row.get("pos", "").strip(),
                "features": {},
            }

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as file:
        json.dump(entries, file, ensure_ascii=False, indent=2)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Build dictionary JSON from CSV.")
    parser.add_argument("csv_path")
    parser.add_argument("output_path", nargs="?", default="data/dictionaries/basic.json")
    args = parser.parse_args()
    print(f"Dictionary written to {build_dictionary(args.csv_path, args.output_path)}")


if __name__ == "__main__":
    main()
