
"""
SanskritAI — Active Source Model Relationship Audit

Purpose
-------
Show relationships between active production source models
and the production modules that reference them.

Target source concepts:
    CorpusSource
    CanonicalSource
    LexicalSource
    MonierWilliamsSource

Excluded:
    - tests
    - scripts
    - cache directories
    - historical numbered copies (*1.py, *2.py, ...)

This is a READ-ONLY audit.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path


PROJECT_ROOT = Path("/content/SanskritAI")

TARGET_NAMES = {
    "CorpusSource",
    "CanonicalSource",
    "LexicalSource",
    "MonierWilliamsSource",
}

EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "tests",
    "scripts",
}

NUMBERED_COPY_PATTERN = re.compile(r".*\d+$")


TARGET_MODULES = {
    "acquisition.models.acquisition_manifest.py": [
        "CorpusSource",
    ],
    "acquisition.models.acquisition_result.py": [
        "CorpusSource",
    ],
    "acquisition.sources.monier_williams_manifest.py": [
        "MonierWilliamsSource",
    ],
    "acquisition.sources.monier_williams.py": [
        "MonierWilliamsSource",
    ],
    (
        "acquisition.lexical.monier_williams."
        "monier_williams_source.py"
    ): [
        "MonierWilliamsSource",
    ],
    (
        "acquisition.lexical.monier_williams."
        "monier_williams_acquisition_service.py"
    ): [
        "MonierWilliamsSource",
    ],
    (
        "acquisition.lexical.monier_williams."
        "monier_williams_source_pipeline.py"
    ): [],
    "domain.lexical.adapters.monier_williams_mapper.py": [
        "CanonicalSource",
    ],
    "domain.lexical.lexical_source.py": [
        "LexicalSource",
    ],
    "lexical.models.lexical_source.py": [
        "LexicalSource",
    ],
    (
        "acquisition.knowledge.models."
        "canonical_source.py"
    ): [
        "CanonicalSource",
    ],
}


def relative_name(path: Path) -> str:

    return str(
        path.relative_to(
            PROJECT_ROOT
        )
    )


def excluded(path: Path) -> bool:

    if any(
        part in EXCLUDED_PARTS
        for part in path.parts
    ):
        return True

    if NUMBERED_COPY_PATTERN.match(path.stem):
        return True

    return False


def source_reference_lines(
    path: Path,
) -> list[tuple[int, str]]:

    results: list[tuple[int, str]] = []

    try:
        source = path.read_text(
            encoding="utf-8"
        )
        tree = ast.parse(source)

    except (
        OSError,
        UnicodeDecodeError,
        SyntaxError,
    ):
        return results

    for node in ast.walk(tree):

        if isinstance(
            node,
            ast.ImportFrom,
        ):

            for alias in node.names:

                if alias.name in TARGET_NAMES:

                    results.append(
                        (
                            node.lineno,
                            (
                                f"IMPORT_FROM "
                                f"{alias.name}"
                            ),
                        )
                    )

        elif isinstance(
            node,
            ast.Name,
        ):

            if node.id in TARGET_NAMES:

                results.append(
                    (
                        node.lineno,
                        (
                            f"REFERENCE "
                            f"{node.id}"
                        ),
                    )
                )

    return results


def scan() -> dict[
    str,
    list[tuple[str, int, str]],
]:

    relationships: dict[
        str,
        list[tuple[str, int, str]],
    ] = {
        name: []
        for name in sorted(TARGET_NAMES)
    }

    for path in PROJECT_ROOT.rglob("*.py"):

        if excluded(path):
            continue

        relative = relative_name(path)

        references = source_reference_lines(
            path
        )

        for line, description in references:

            for target in TARGET_NAMES:

                if target in description:

                    relationships[
                        target
                    ].append(
                        (
                            relative,
                            line,
                            description,
                        )
                    )

    return relationships


def print_report(
    relationships: dict[
        str,
        list[tuple[str, int, str]],
    ],
) -> None:

    print("=" * 80)
    print(
        "SANSKRITAI — ACTIVE SOURCE MODEL "
        "RELATIONSHIP AUDIT"
    )
    print("=" * 80)
    print()

    for model in sorted(
        relationships
    ):

        print("-" * 80)
        print(model)
        print("-" * 80)

        entries = relationships[
            model
        ]

        if not entries:

            print(
                "  <no active production "
                "relationships detected>"
            )
            print()
            continue

        grouped: dict[
            str,
            list[tuple[int, str]],
        ] = {}

        for (
            file,
            line,
            description,
        ) in entries:

            grouped.setdefault(
                file,
                [],
            ).append(
                (
                    line,
                    description,
                )
            )

        for file in sorted(grouped):

            print()
            print(f"  {file}")

            for (
                line,
                description,
            ) in sorted(
                grouped[file]
            ):

                print(
                    f"    line {line:4d}: "
                    f"{description}"
                )

        print()

    print("=" * 80)
    print(
        "NUMBERED HISTORICAL COPIES: EXCLUDED"
    )
    print("=" * 80)
    print()

    print(
        "Excluded pattern: *<number>.py"
    )

    print()

    print("=" * 80)
    print(
        "AUDIT COMPLETE — NO FILES MODIFIED"
    )
    print("=" * 80)


def main() -> None:

    relationships = scan()

    print_report(
        relationships
    )


if __name__ == "__main__":
    main()
