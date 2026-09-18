
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

    original = TARGET.read_text(encoding="utf-8")

    print()
    print("1. PRE-REPAIR VALIDATION")
    print("-" * 100)

    lines = original.splitlines(keepends=True)

    locations = [
        index + 1
        for index, line in enumerate(lines)
        if line.strip() == EXPECTED_FUTURE_IMPORT
    ]

    print("Future import locations :", locations)

    if locations != [2, 57]:
        raise RuntimeError(
            "Expected exactly two future imports at "
            "lines 2 and 57. "
            f"Found: {locations}"
        )

    tree = parse_source(original)

    nodes = future_import_nodes(tree)

    if len(nodes) != 2:
        raise RuntimeError(
            f"Expected 2 AST future imports; found {len(nodes)}."
        )

    if nodes[0].lineno != 2:
        raise RuntimeError(
            "First future import is not at line 2."
        )

    if nodes[1].lineno != 57:
        raise RuntimeError(
            "Second future import is not at line 57."
        )

    print("Pre-repair AST validation : PASS")

    print()
    print("2. APPLY EXACT MINIMAL REPAIR")
    print("-" * 100)

    # Remove exactly the audited duplicate line.
    repaired_lines = [
        line
        for index, line in enumerate(lines, start=1)
        if index != 57
    ]

    repaired = "".join(repaired_lines)

    if repaired == original:
        raise RuntimeError(
            "Repair produced no change."
        )

    # Confirm only the expected future-import line was removed.
    original_without_target = (
        original.splitlines(keepends=True)[:56]
        + original.splitlines(keepends=True)[57:]
    )

    expected_repaired = "".join(original_without_target)

    if repaired != expected_repaired:
        raise RuntimeError(
            "Repair differs from the expected one-line removal."
        )

    TARGET.write_text(
        repaired,
        encoding="utf-8",
    )

    print("Removed line 57 only : PASS")

    print()
    print("3. POST-REPAIR AST VALIDATION")
    print("-" * 100)

    post_tree = parse_source(repaired)

    post_nodes = future_import_nodes(post_tree)

    print(
        "Future import count : "
        f"{len(post_nodes)}"
    )

    if len(post_nodes) != 1:
        raise RuntimeError(
            "Expected exactly one future import after repair."
        )

    if post_nodes[0].lineno != 2:
        raise RuntimeError(
            "Remaining future import is not at line 2."
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

    remaining_locations = [
        index + 1
        for index, line in enumerate(
            repaired.splitlines(),
            start=1,
        )
        if line.strip() == EXPECTED_FUTURE_IMPORT
    ]

    if remaining_locations != [2]:
        raise RuntimeError(
            "Unexpected future-import locations after repair: "
            f"{remaining_locations}"
        )

    print(
        "Remaining future import : line 2"
    )
    print("Duplicate future import : 0")

    print()
    print("=" * 100)
    print(
        "BATCH 5H-5E-13R-4S-4 — RESULT: PASS"
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
