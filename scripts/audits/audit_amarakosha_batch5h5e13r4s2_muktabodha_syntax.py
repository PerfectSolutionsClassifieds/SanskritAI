
from __future__ import annotations

"""
BATCH 5H-5E-13R-4S-2
====================

MUKTABODHA PROVIDER SYNTAX AUDIT

READ-ONLY.

Determines exactly why muktabodha_provider.py fails to import.

No production files are modified.
"""

from pathlib import Path
import ast
import re

PROJECT_ROOT = Path("/content/SanskritAI")

TARGET = (
    PROJECT_ROOT
    / "acquisition"
    / "providers"
    / "muktabodha_provider.py"
)


def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def main() -> None:

    section(
        "BATCH 5H-5E-13R-4S-2 — "
        "MUKTABODHA SYNTAX AUDIT"
    )

    if not TARGET.exists():
        raise RuntimeError(
            f"Target does not exist: {TARGET}"
        )

    text = TARGET.read_text(
        encoding="utf-8"
    )

    lines = text.splitlines()

    section(
        "1. FILE METADATA"
    )

    print(
        f"Path : {TARGET}"
    )

    print(
        f"Lines : {len(lines)}"
    )

    section(
        "2. FUTURE IMPORT LOCATIONS"
    )

    future_imports = []

    for number, line in enumerate(
        lines,
        start=1,
    ):

        if line.strip().startswith(
            "from __future__ import"
        ):

            future_imports.append(
                (
                    number,
                    line.strip(),
                )
            )

    for number, line in future_imports:

        print(
            f"{number}: {line}"
        )

    print()
    print(
        f"Future import count : "
        f"{len(future_imports)}"
    )

    section(
        "3. AST PARSE"
    )

    try:

        tree = ast.parse(
            text,
            filename=str(TARGET),
        )

        print(
            "AST parse : PASS"
        )

        future_nodes = [
            node
            for node in tree.body
            if isinstance(
                node,
                ast.ImportFrom,
            )
            and node.module == "__future__"
        ]

        print(
            f"AST future-import nodes : "
            f"{len(future_nodes)}"
        )

        for node in future_nodes:

            print(
                f"  line {node.lineno}: "
                f"{ast.unparse(node)}"
            )

    except SyntaxError as exc:

        print(
            "AST parse : FAIL"
        )

        print(
            f"  msg      : {exc.msg}"
        )

        print(
            f"  line     : {exc.lineno}"
        )

        print(
            f"  offset   : {exc.offset}"
        )

        print(
            f"  text     : {exc.text!r}"
        )

    section(
        "4. MODULE HEADER"
    )

    for number, line in enumerate(
        lines[:80],
        start=1,
    ):

        print(
            f"{number:03d}: {line}"
        )

    section(
        "5. FINAL RESULT"
    )

    print(
        "BATCH 5H-5E-13R-4S-2 — RESULT: "
        "AUDIT COMPLETE"
    )


if __name__ == "__main__":
    main()
