"""
SanskritAI
==========

Integration Test

Verifies parser error recovery using a malformed
Amarakośa sample corpus.

The parser should:

    • Continue after recoverable errors
    • Record all encountered errors
    • Produce internally consistent statistics
    • Leave the parser in a valid final state

Version:
    v0.4.0 Final
"""

from __future__ import annotations

from pathlib import Path

from models.imports import ImportStatus

from services.importers import AmarakoshaImporter


# ---------------------------------------------------------
# Locate malformed sample corpus
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SAMPLE_FILE = (
    PROJECT_ROOT
    / "data"
    / "amarakosha"
    / "malformed.txt"
)


# ---------------------------------------------------------
# Main Test
# ---------------------------------------------------------

def main() -> None:

    assert SAMPLE_FILE.exists(), (
        f"Malformed sample not found:\n{SAMPLE_FILE}"
    )

    importer = AmarakoshaImporter()

    result = importer.import_file(SAMPLE_FILE)

    # -----------------------------------------------------
    # Import should complete without crashing.
    # -----------------------------------------------------

    assert result is not None

    # -----------------------------------------------------
    # A partially imported book should still exist.
    # -----------------------------------------------------

    assert result.book is not None

    # -----------------------------------------------------
    # Statistics object should always exist.
    # -----------------------------------------------------

    assert result.statistics is not None

    # -----------------------------------------------------
    # At least one parser error should be reported.
    # -----------------------------------------------------

    assert len(result.errors) > 0

    # -----------------------------------------------------
    # Basic statistical consistency.
    # -----------------------------------------------------

    assert result.statistics.kandas >= 0
    assert result.statistics.vargas >= 0
    assert result.statistics.verses >= 0

    assert result.statistics.total_lines > 0

    # -----------------------------------------------------
    # Import status
    #
    # Accept SUCCESS_WITH_WARNINGS if supported.
    # Otherwise SUCCESS is acceptable provided
    # parser errors were recorded.
    # -----------------------------------------------------

    valid_statuses = {
        ImportStatus.SUCCESS,
    }

    if hasattr(ImportStatus, "SUCCESS_WITH_WARNINGS"):
        valid_statuses.add(
            ImportStatus.SUCCESS_WITH_WARNINGS
        )

    assert result.status in valid_statuses

    # -----------------------------------------------------
    # Report
    # -----------------------------------------------------

    print()

    print("=" * 60)
    print("IMPORT ERROR RECOVERY TEST")
    print("=" * 60)

    print(f"Status      : {result.status.name}")

    print(
        f"Kāṇḍas      : {result.statistics.kandas}"
    )

    print(
        f"Vargas      : {result.statistics.vargas}"
    )

    print(
        f"Verses      : {result.statistics.verses}"
    )

    print(
        f"Errors      : {len(result.errors)}"
    )

    print()

    print("Recorded Parser Errors")

    print("-" * 60)

    for error in result.errors:

        print(error)

    print("-" * 60)

    print("PASS")


if __name__ == "__main__":

    main()
