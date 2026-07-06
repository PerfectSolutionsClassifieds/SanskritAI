"""
SanskritAI
==========

Module:
    tests.lexical.run_all_tests

Description
-----------
Master test runner for the Lexical Layer.

This script executes every lexical unit test as an independent
Python module and reports a concise summary.

Version:
    v0.3.0 Final
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
import time
from pathlib import Path

# =========================================================
# Project Root
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.chdir(PROJECT_ROOT)

# =========================================================
# Test Modules
# =========================================================

TEST_MODULES = tuple(sorted((

    "tests.lexical.test_dictionary_entry",

    "tests.lexical.test_dictionary_sense",

    "tests.lexical.test_integrity",

    "tests.lexical.test_language",

    "tests.lexical.test_lexeme",

    "tests.lexical.test_relations",

    "tests.lexical.test_script",

    "tests.lexical.test_serialization",

)))

# =========================================================
# Main
# =========================================================

def main() -> int:

    print("=" * 72)
    print("SanskritAI v0.3.0 Final")
    print("Lexical Layer Test Suite")
    print("=" * 72)

    print(f"Python       : {platform.python_version()}")
    print(f"Executable   : {sys.executable}")
    print(f"Working Dir  : {os.getcwd()}")
    print(f"Project Root : {PROJECT_ROOT}")

    print("=" * 72)

    start_time = time.perf_counter()

    passed: list[str] = []
    failed: list[str] = []

    # -----------------------------------------------------
    # Execute Tests
    # -----------------------------------------------------

    for module in TEST_MODULES:

        print(f"\n>>> {module}")

        result = subprocess.run(
            [sys.executable, "-m", module],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:

            passed.append(module)

            print("✓ PASS")

        else:

            failed.append(module)

            print("✗ FAIL")

            if result.stdout.strip():

                print("\n----- STDOUT -----")

                print(result.stdout)

            if result.stderr.strip():

                print("\n----- STDERR -----")

                print(result.stderr)

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    elapsed = time.perf_counter() - start_time

    print("\n" + "=" * 72)

    print("SUMMARY")

    print("-" * 72)

    print(f"Total Tests : {len(TEST_MODULES)}")
    print(f"Passed      : {len(passed)}")
    print(f"Failed      : {len(failed)}")
    print(f"Elapsed     : {elapsed:.2f} seconds")

    if failed:

        print("\nFailed Modules")

        print("-" * 72)

        for module in failed:

            print(f"• {module}")

        print("\nSTATUS : FAILED")

        print("=" * 72)

        return 1

    print("\nSTATUS : ALL TESTS PASSED")

    print("=" * 72)

    return 0


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":

    sys.exit(main())
