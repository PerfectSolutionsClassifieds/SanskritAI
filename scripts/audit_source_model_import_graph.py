from __future__ import annotations

import ast
from pathlib import Path
from collections import defaultdict


ROOT = Path("/content/SanskritAI")

SOURCE_MODULES = {
    "CorpusSource":
        "SanskritAI.acquisition.models.corpus_source",

    "CanonicalSource":
        "SanskritAI.acquisition.knowledge.models.canonical_source",

    "DomainLexicalSource":
        "SanskritAI.domain.lexical.lexical_source",

    "KernelLexicalSource":
        "SanskritAI.lexical.models.lexical_source",

    "MWMetadataSource":
        "SanskritAI.acquisition.sources.monier_williams",

    "MWRawSource":
        "SanskritAI.acquisition.lexical.monier_williams.monier_williams_source",
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


def main():
    graph = defaultdict(set)

    for path in sorted(ROOT.rglob("*.py")):
        if excluded(path):
            continue

        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        current = path.relative_to(ROOT).as_posix()

        for node in ast.walk(tree):

            if isinstance(node, ast.ImportFrom):
                module = node.module or ""

                for logical, target_module in SOURCE_MODULES.items():
                    if module == target_module:
                        graph[logical].add(current)

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    for logical, target_module in SOURCE_MODULES.items():
                        if alias.name == target_module:
                            graph[logical].add(current)

    print("=" * 80)
    print("SanskritAI — SOURCE MODEL IMPORT GRAPH")
    print("=" * 80)

    for logical, module in SOURCE_MODULES.items():
        print()
        print(f"{logical}")
        print(f"  module: {module}")

        consumers = sorted(graph.get(logical, set()))

        print(f"  production consumers: {len(consumers)}")

        if consumers:
            for consumer in consumers:
                print(f"    -> {consumer}")
        else:
            print("    -> <none>")

    print()
    print("=" * 80)
    print("END OF SOURCE MODEL IMPORT GRAPH")
    print("=" * 80)


if __name__ == "__main__":
    main()

