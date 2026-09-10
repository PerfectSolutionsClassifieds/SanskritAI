from __future__ import annotations

import ast
from pathlib import Path
from collections import defaultdict


ROOT = Path("/content/SanskritAI")

TARGET_MODULES = {
    "CorpusSource": "SanskritAI.acquisition.models.corpus_source",
    "CanonicalSource": "SanskritAI.acquisition.knowledge.models.canonical_source",
    "DomainLexicalSource": "SanskritAI.domain.lexical.lexical_source",
    "KernelLexicalSource": "SanskritAI.lexical.models.lexical_source",
    "MWMetadataSource": "SanskritAI.acquisition.sources.monier_williams",
    "MWRawSource": "SanskritAI.acquisition.lexical.monier_williams.monier_williams_source",
}

EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "sanskritai.egg-info",
    "tests",
}


def excluded(path: Path) -> bool:
    return any(part in EXCLUDED_PARTS for part in path.parts)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def inspect(path: Path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return []

    findings = []

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                for logical_name, target_module in TARGET_MODULES.items():
                    if module == target_module:
                        findings.append(
                            (
                                logical_name,
                                "IMPORT_FROM",
                                node.lineno,
                                alias.name,
                            )
                        )

        elif isinstance(node, ast.Import):
            for alias in node.names:
                for logical_name, target_module in TARGET_MODULES.items():
                    if alias.name == target_module:
                        findings.append(
                            (
                                logical_name,
                                "IMPORT",
                                node.lineno,
                                alias.name,
                            )
                        )

    return findings


def main():
    dependencies = defaultdict(list)

    for path in sorted(ROOT.rglob("*.py")):
        if excluded(path):
            continue

        if not path.is_file():
            continue

        for finding in inspect(path):
            logical_name, kind, line, detail = finding

            dependencies[logical_name].append(
                {
                    "file": relative(path),
                    "kind": kind,
                    "line": line,
                    "detail": detail,
                }
            )

    print("=" * 80)
    print("SanskritAI — SOURCE MODEL DEPENDENCY AUDIT")
    print("=" * 80)

    for logical_name in TARGET_MODULES:
        print()
        print("-" * 80)
        print(logical_name)
        print("-" * 80)

        items = dependencies.get(logical_name, [])

        if not items:
            print("  <no production imports>")
            continue

        grouped = defaultdict(list)

        for item in items:
            grouped[item["file"]].append(item)

        for filename in sorted(grouped):
            print()
            print(f"  {filename}")

            for item in grouped[filename]:
                print(
                    f"    line {item['line']:>4} "
                    f"{item['kind']:<12} "
                    f"{item['detail']}"
                )

    print()
    print("=" * 80)
    print("END OF DEPENDENCY AUDIT")
    print("=" * 80)


if __name__ == "__main__":
    main()

