"""
SanskritAI
==========

Master Test Runner

Runs all v0.3.0 lexical layer tests.

Version:
    v0.3.0 Final
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
import time

# ---------------------------------------------------------
# Test Modules
# ---------------------------------------------------------

TEST_MODULES = (

    "tests.lexical.test_language",

    "tests.lexical.test_script",

    "tests.lexical.test_dictionary_sense",

    "tests.lexical.test_dictionary_entry",

    "tests.lexical.test_lexeme",

    "tests.lexical.test_relations",

    "tests.lexical.test_serialization",

    "tests.lexical.test_integrity",

)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

print("=" * 72)
print("SanskritAI v0.3.0 Final")
print("Lexical Layer Test Suite")
print("=" * 72)

print(f"Python      : {platform.python_version()}")
print(f"Executable  : {sys.executable}")
print(f"Working Dir : {os.getcwd()}")

print("=" * 72)

start_time = time.perf_counter()

passed = []
failed = []

# ---------------------------------------------------------
# Execute Tests
# ---------------------------------------------------------

for module in TEST_MODULES:

    print(f"\n>>> {module}")

    result = subprocess.run(
        [sys.executable, "-m", module]
    )

    if result.returncode == 0:

        passed.append(module)

        print("✓ PASS")

    else:

        failed.append(module)

        print("✗ FAIL")

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

elapsed = time.perf_counter() - start_time

print("\n" + "=" * 72)

print("SUMMARY")

print("-" * 72)

print(f"Total Tests : {len(TEST_MODULES)}")
print(f"Passed      : {len(passed)}")
print(f"Failed      : {len(failed)}")
print(f"Time        : {elapsed:.2f} seconds")

if failed:

    print("\nFailed Modules:")

    for module in failed:
        print(f"  • {module}")

    print("\nSTATUS : FAILED")

    sys.exit(1)

print("\nSTATUS : ALL TESTS PASSED")

print("=" * 72)

sys.exit(0)
