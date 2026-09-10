from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("/content/SanskritAI")

DOMAIN_MODULE = "SanskritAI.domain.lexical.lexical_source"
LEXICAL_MODULE = "SanskritAI.lexical.models.lexical_source"


LAYER_NAMES = {
    "domain",
    "application",
    "services",
    "service",
    "adapters",
    "repositories",
    "repository",
    "registries",
    "registry",
    "lexical",
}


def is_historical_python_file(path: Path) -> bool:
    name = path.name

    if not name.endswith(".py"):
        return True

    stem = name[:-3]

    if stem and stem[-1].isdigit():
        return True

    if "_G" in stem:
        suffix = stem.rsplit("_G", 1)[-1]
        if suffix.isdigit():
            return True

    if "__pycache__" in path.parts:
        return True

    if "test" in path.parts:
        return True

    return False


def iter_python_files():
    for path in ROOT.rglob("*.py"):
        if is_historical_python_file(path):
            continue
        yield path


def layer_for(path: Path) -> str:
    parts = path.relative_to(ROOT).parts

    for part in parts:
        if part in LAYER_NAMES:
            return part

    return "other"


def analyze(path: Path):
    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except Exception as exc:
        return [(
            0,
            "PARSE ERROR",
            str(exc),
        )]

    evidence = []

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):
            module = node.module or ""

            if module in {
                DOMAIN_MODULE,
                LEXICAL_MODULE,
            }:
                for alias in node.names:
                    evidence.append(
                        (
                            node.lineno,
                            "IMPORT",
                            f"from {module} import {alias.name}",
                        )
                    )

        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in {
                    DOMAIN_MODULE,
                    LEXICAL_MODULE,
                }:
                    evidence.append(
                        (
                            node.lineno,
                            "IMPORT",
                            f"import {alias.name}",
                        )
                    )

    return evidence


def main():
    print("=" * 100)
    print("SANSKRITAI — DOMAIN → APPLICATION → LEXICAL SOURCE BOUNDARY AUDIT")
    print("=" * 100)
    print()
    print("DOMAIN TARGET:")
    print(f"  {DOMAIN_MODULE}")
    print()
    print("LEXICAL TARGET:")
    print(f"  {LEXICAL_MODULE}")
    print()

    by_layer = {}
    total = 0

    for path in sorted(iter_python_files()):
        evidence = analyze(path)

        if not evidence:
            continue

        layer = layer_for(path)

        by_layer.setdefault(layer, [])

        for item in evidence:
            by_layer[layer].append(
                (
                    path.relative_to(ROOT),
                    *item,
                )
            )

        total += len(evidence)

    for layer in sorted(by_layer):
        print("-" * 100)
        print(f"LAYER: {layer.upper()}")
        print("-" * 100)

        for path, line, kind, value in by_layer[layer]:
            print(
                f"{path} | line {line} | {kind} | {value}"
            )

        print()

    print("=" * 100)
    print("BOUNDARY SUMMARY")
    print("=" * 100)

    if not by_layer:
        print("NO CROSS-LAYER IMPORT EVIDENCE FOUND")
    else:
        for layer in sorted(by_layer):
            print(
                f"{layer:20s}: "
                f"{len(by_layer[layer])} reference(s)"
            )

    print()
    print(f"TOTAL BOUNDARY REFERENCES: {total}")
    print()
    print("AUDIT COMPLETE — NO FILES MODIFIED")
    print("=" * 100)


if __name__ == "__main__":
    main()
