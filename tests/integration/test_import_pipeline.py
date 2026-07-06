"""
SanskritAI
==========

Integration Test

Verifies the complete Amarakośa import pipeline.

Version:
    v0.4.0 Final
"""

from __future__ import annotations

from pathlib import Path

from models.imports import ImportStatus

from services.importers import AmarakoshaImporter


# ---------------------------------------------------------------------
# Locate sample corpus
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SAMPLE_FILE = (

    PROJECT_ROOT
    / "data"
    / "amarakosha"
    / "sample.txt"

)

# ---------------------------------------------------------------------
# Main Test
# ---------------------------------------------------------------------


def main() -> None:

    assert SAMPLE_FILE.exists(), (

        f"Sample corpus not found:\n{SAMPLE_FILE}"

    )

    importer = AmarakoshaImporter()

    result = importer.import_file(

        SAMPLE_FILE,

    )

    assert result.status == ImportStatus.SUCCESS

    assert result.book is not None

    assert len(result.book.kandas) > 0

    assert result.statistics.kandas > 0

    assert result.statistics.vargas > 0

    assert result.statistics.verses > 0

    print()

    print("Imported Book")

    print("------------------------------")

    print(f"Kāṇḍas : {result.statistics.kandas}")

    print(f"Vargas : {result.statistics.vargas}")

    print(f"Verses : {result.statistics.verses}")

    print()

    print("PASS")


if __name__ == "__main__":

    main()
