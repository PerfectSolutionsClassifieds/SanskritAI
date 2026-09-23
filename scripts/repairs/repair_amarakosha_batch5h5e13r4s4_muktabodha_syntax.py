
from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

TARGET = (
    ROOT
    / "acquisition"
    / "providers"
    / "muktabodha_provider.py"
)

EXPECTED_FUTURE_IMPORT = "from __future__ import annotations"


def parse_source(text: str) -> ast.Module:
    return ast.parse(
        text,
        filename=str(TARGET),
    )


def future_import_nodes(tree: ast.Module) -> list[ast.ImportFrom]:
    return [
        node
        for node in tree.body
        if isinstance(node, ast.ImportFrom)
        and node.module == "__future__"
    ]


def source_future_import_locations(text: str) -> list[int]:
    """
    Return actual future-import line locations.

    Comments containing the text are intentionally ignored.
    """
    tree = parse_source(text)

    return [
        node.lineno
        for node in future_import_nodes(tree)
        if any(
            alias.name == "annotations"
            for alias in node.names
        )
    ]


def validate_repaired_state(text: str) -> None:
    """
    Validate that the file contains exactly one legitimate
    future import and that it is at line 2.
    """
    locations = source_future_import_locations(text)

    if locations != [2]:
        raise RuntimeError(
            "Expected repaired Muktabodha state with exactly "
            f"one future import at line 2. Found: {locations}"
        )


def main() -> None:
    print("=" * 100)
    print(
        "BATCH 5H-5E-13R-4S-4 — "
        "MUKTABODHA FUTURE-IMPORT MINIMAL REPAIR"
    )
    print("=" * 100)

    if not TARGET.exists():
        raise FileNotFoundError(
            f"Target file does not exist: {TARGET}"
        )

    original = TARGET.read_text(
        encoding="utf-8"
    )

    print()
    print("1. PRE-REPAIR AST VALIDATION")
    print("-" * 100)

    original_tree = parse_source(original)

    original_locations = [
        node.lineno
        for node in future_import_nodes(original_tree)
        if any(
            alias.name == "annotations"
            for alias in node.names
        )
    ]

    print(
        "Actual future import locations : "
        f"{original_locations}"
    )

    # ---------------------------------------------------------
    # CASE A: Already repaired
    # ---------------------------------------------------------

    if original_locations == [2]:
        print()
        print(
            "Detected already-repaired Muktabodha provider."
        )
        print(
            "No production modification required."
        )

        print()
        print("2. ALREADY-REPAIRED STATE VALIDATION")
        print("-" * 100)

        validate_repaired_state(original)

        print(
            "Exactly one future import at line 2 : PASS"
        )

        print()
        print("3. COMPILATION VALIDATION")
        print("-" * 100)

        compile(
            original,
            str(TARGET),
            "exec",
        )

        print("Compilation : PASS")

        print()
        print("=" * 100)
        print(
            "BATCH 5H-5E-13R-4S-4 — "
            "RESULT: PASS (ALREADY REPAIRED)"
        )
        print("=" * 100)

        return

    # ---------------------------------------------------------
    # CASE B: Original audited defective state
    # ---------------------------------------------------------

    if original_locations != [2, 57]:
        raise RuntimeError(
            "Unexpected future-import state. "
            "Expected either [2, 57] for repair or [2] "
            f"for already-repaired state. Found: "
            f"{original_locations}"
        )

    print()
    print("Detected audited defective state : [2, 57]")
    print("Repair required : YES")

    print()
    print("2. APPLY EXACT MINIMAL REPAIR")
    print("-" * 100)

    lines = original.splitlines(
        keepends=True
    )

    # Confirm the exact audited line.
    if lines[56].strip() != EXPECTED_FUTURE_IMPORT:
        raise RuntimeError(
            "Line 57 is not the expected future import. "
            "Repair aborted."
        )

    # Remove exactly line 57.
    repaired_lines = (
        lines[:56] +
        lines[57:]
    )

    repaired = "".join(repaired_lines)

    if repaired == original:
        raise RuntimeError(
            "Repair produced no change."
        )

    TARGET.write_text(
        repaired,
        encoding="utf-8",
    )

    print(
        "Removed duplicate future import at line 57 : PASS"
    )

    print()
    print("3. POST-REPAIR AST VALIDATION")
    print("-" * 100)

    repaired_tree = parse_source(repaired)

    repaired_locations = [
        node.lineno
        for node in future_import_nodes(repaired_tree)
        if any(
            alias.name == "annotations"
            for alias in node.names
        )
    ]

    print(
        "Future import locations after repair : "
        f"{repaired_locations}"
    )

    if repaired_locations != [2]:
        raise RuntimeError(
            "Unexpected post-repair future-import state: "
            f"{repaired_locations}"
        )

    print("AST validation : PASS")
    print("Future import placement : PASS")

    print()
    print("4. POST-REPAIR COMPILATION")
    print("-" * 100)

    compile(
        repaired,
        str(TARGET),
        "exec",
    )

    print("Compilation : PASS")

    print()
    print("5. POST-REPAIR STRUCTURAL CHECK")
    print("-" * 100)

    validate_repaired_state(repaired)

    print(
        "Exactly one future import at line 2 : PASS"
    )
    print(
        "Duplicate future imports : 0"
    )

    print()
    print("=" * 100)
    print(
        "BATCH 5H-5E-13R-4S-4 — "
        "RESULT: PASS"
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
