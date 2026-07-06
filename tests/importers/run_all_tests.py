"""
SanskritAI
==========

Importer Test Suite

Runs all importer layer tests.

Version:
    v0.4.0 Final
"""

from __future__ import annotations

import platform
import subprocess
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------
# Project Root
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------
# Test Modules
# ---------------------------------------------------------------------

TEST_MODULES = sorted(

    (

        "tests.importers.test_line_classifier",

        "tests.importers.test_unicode_normalizer",

        "tests.importers.test_structure_numbering",

        "tests.importers.test_parser_errors",

        "tests.importers.test_parser_context",

        "tests.importers.test_parser_validator",

        "tests.importers.test_classification_result",

        "tests.importers.test_amarakosha_builder",

        "tests.importers.test_import_result_builder",

        "tests.importers.test_parser",

        "tests.integration.test_import_pipeline",

    )

)

# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------


def main() -> int:

    print("=" * 72)

    print("SanskritAI v0.4.0")

    print("Importer Test Suite")

    print("=" * 72)

    print(f"Python       : {platform.python_version()}")

    print(f"Executable   : {sys.executable}")

    print(f"Project Root : {PROJECT_ROOT}")

    print("=" * 72)

    start = time.perf_counter()

    passed = []
    failed = []

    for module in TEST_MODULES:

        print(f"\n>>> {module}")

        result = subprocess.run(

            [sys.executable, "-m", module],

            cwd=PROJECT_ROOT,

            capture_output=True,

            text=True,

        )

        if result.returncode == 0:

            passed.append(module)

            print("✓ PASS")

        else:

            failed.append(module)

            print("✗ FAIL")

            print("-" * 72)

            print(result.stdout)

            print(result.stderr)

            print("-" * 72)

    elapsed = time.perf_counter() - start

    print("\n" + "=" * 72)

    print("SUMMARY")

    print("-" * 72)

    print(f"Total   : {len(TEST_MODULES)}")

    print(f"Passed  : {len(passed)}")

    print(f"Failed  : {len(failed)}")

    print(f"Elapsed : {elapsed:.2f} seconds")

    if failed:

        print("\nFailed Modules")

        for module in failed:

            print(f"  • {module}")

        print("\nSTATUS : FAILED")

        return 1

    print("\nSTATUS : ALL TESTS PASSED")

    print("=" * 72)

    return 0


if __name__ == "__main__":

    raise SystemExit(main())
