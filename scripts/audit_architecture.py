
"""
SanskritAI — Reusable Architectural Audit

Purpose
-------
Provide one reusable architecture-audit script that can be used across
SanskritAI source/model/validator/repository questions without creating a
new inspection script for every architectural investigation.

Design principles
-----------------
1. Ownership first
2. Semantics second
3. Consumers before implementation details
4. Production code separated from tests
5. Historical numbered files are ignored
6. No source-code modifications
7. No architectural assumptions are imposed
8. Output should support an explicit architectural decision

Examples
--------
From the repository root:

    python scripts/audit_architecture.py

    python scripts/audit_architecture.py --target lexical-source

    python scripts/audit_architecture.py --target corpus-source

    python scripts/audit_architecture.py --target canonical-source

    python scripts/audit_architecture.py --target monier-williams-source

    python scripts/audit_architecture.py --target all-sources

Optional:

    python scripts/audit_architecture.py \
        --target lexical-source \
        --show-code

    python scripts/audit_architecture.py \
        --target lexical-source \
        --max-files 300

The script is intentionally conservative. It reports evidence and signals;
it does not automatically modify production architecture.
"""

from __future__ import annotations

import argparse
import ast
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


# ============================================================================
# Configuration
# ============================================================================

REPO_ROOT = Path(__file__).resolve().parents[1]

IGNORED_DIRECTORIES = {
    ".git",
    ".github",
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
}

# User-directed rule:
# Ignore historical / duplicate numbered Python files such as:
#
#   mapper1.py
#   mapper2.py
#   test_source3.py
#
# Also ignore common generated audit variants such as:
#
#   audit_source_G1.py
#
NUMBERED_FILE_RE = re.compile(r"\d+\.py$", re.IGNORECASE)
GENERATED_AUDIT_RE = re.compile(r"_G\d+\.py$", re.IGNORECASE)


TARGETS = {
    "lexical-source": {
        "label": "LexicalSource",
        "symbols": ["LexicalSource"],
        "paths": [
            "domain/lexical",
            "lexical",
        ],
        "semantic_fields": [
            "source_id",
            "identifier",
            "name",
            "source_type",
            "version",
            "language",
            "script",
            "description",
            "url",
            "website",
            "publisher",
            "editor",
            "publication_year",
        ],
        "keywords": [
            "lexical",
            "source",
            "dictionary",
            "record",
            "repository",
            "catalog",
            "validator",
        ],
    },
    "corpus-source": {
        "label": "CorpusSource",
        "symbols": ["CorpusSource"],
        "paths": [
            "acquisition",
            "corpus",
        ],
        "semantic_fields": [
            "source_id",
            "name",
            "source_type",
            "source_format",
            "license",
            "version",
            "edition",
            "publisher",
            "author",
            "description",
            "language",
            "status",
            "download_urls",
            "checksum",
            "local_path",
            "cache_directory",
        ],
        "keywords": [
            "corpus",
            "source",
            "acquisition",
            "manifest",
            "provider",
            "acquirer",
            "repository",
        ],
    },
    "canonical-source": {
        "label": "CanonicalSource",
        "symbols": ["CanonicalSource"],
        "paths": [
            "acquisition",
            "domain",
            "corpus",
            "knowledge",
        ],
        "semantic_fields": [
            "source_id",
            "name",
            "short_name",
            "source_type",
            "language",
            "script",
            "author",
            "editor",
            "publisher",
            "edition",
            "publication_year",
            "version",
            "website",
            "download_url",
            "api_endpoint",
            "license",
            "description",
            "notes",
            "metadata",
        ],
        "keywords": [
            "canonical",
            "source",
            "provenance",
            "knowledge",
            "repository",
        ],
    },
    "monier-williams-source": {
        "label": "MonierWilliamsSource",
        "symbols": ["MonierWilliamsSource"],
        "paths": [
            "acquisition",
            "domain",
        ],
        "semantic_fields": [
            "source_id",
            "name",
            "source",
            "identifier",
            "source_name",
            "source_type",
            "source_format",
            "encoding",
            "language",
            "year",
            "author",
            "title",
            "publisher",
        ],
        "keywords": [
            "monier",
            "williams",
            "source",
            "dictionary",
            "lexical",
            "parser",
            "acquisition",
        ],
    },
    "all-sources": {
        "label": "All Source Models",
        "symbols": [
            "LexicalSource",
            "CorpusSource",
            "CanonicalSource",
            "MonierWilliamsSource",
        ],
        "paths": [
            "acquisition",
            "corpus",
            "domain",
            "lexical",
        ],
        "semantic_fields": [],
        "keywords": [
            "source",
            "lexical",
            "corpus",
            "canonical",
            "acquisition",
            "repository",
            "validator",
        ],
    },
}


# ============================================================================
# Data structures
# ============================================================================

@dataclass
class SymbolDefinition:
    symbol: str
    file: Path
    relative_path: str
    line: int
    bases: list[str] = field(default_factory=list)
    decorator_names: list[str] = field(default_factory=list)
    fields: list[str] = field(default_factory=list)
    properties: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)


@dataclass
class ImportEvidence:
    file: Path
    relative_path: str
    line: int
    imported_symbol: str
    module: str
    alias: str | None = None


@dataclass
class SymbolUsage:
    file: Path
    relative_path: str
    line: int
    symbol: str
    context: str


@dataclass
class FileAnalysis:
    file: Path
    relative_path: str
    is_test: bool
    imports: list[ImportEvidence] = field(default_factory=list)
    definitions: list[SymbolDefinition] = field(default_factory=list)
    usages: list[SymbolUsage] = field(default_factory=list)


# ============================================================================
# File filtering
# ============================================================================

def is_ignored_file(path: Path) -> bool:
    """
    Ignore historical numbered files and generated audit variants.

    Examples ignored:
        foo1.py
        foo2.py
        test_foo3.py
        audit_source_G1.py
    """
    name = path.name

    if NUMBERED_FILE_RE.search(name):
        return True

    if GENERATED_AUDIT_RE.search(name):
        return True

    return False


def is_ignored_directory(path: Path) -> bool:
    return any(part in IGNORED_DIRECTORIES for part in path.parts)


def is_test_file(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}

    if "tests" in parts:
        return True

    return path.name.startswith("test_")


def iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if is_ignored_directory(path):
            continue

        if is_ignored_file(path):
            continue

        yield path


# ============================================================================
# AST helpers
# ============================================================================

def get_node_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        return node.attr

    if isinstance(node, ast.Constant):
        return str(node.value)

    return ""


def get_dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent = get_dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr

    return ""


def get_decorator_name(node: ast.AST) -> str:
    if isinstance(node, ast.Call):
        return get_dotted_name(node.func)

    return get_dotted_name(node)


def annotation_name(annotation: ast.AST | None) -> str:
    if annotation is None:
        return ""

    return get_dotted_name(annotation)


def extract_class_fields(node: ast.ClassDef) -> list[str]:
    """
    Collect likely dataclass/model fields without attempting to execute code.
    """
    fields: list[str] = []

    for item in node.body:
        if isinstance(item, ast.AnnAssign):
            if isinstance(item.target, ast.Name):
                fields.append(item.target.id)

        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    fields.append(target.id)

    return sorted(set(fields))


def extract_class_properties(node: ast.ClassDef) -> list[str]:
    properties: list[str] = []

    for item in node.body:
        if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        for decorator in item.decorator_list:
            name = get_decorator_name(decorator)

            if name.endswith("property"):
                properties.append(item.name)

    return sorted(set(properties))


def extract_class_methods(node: ast.ClassDef) -> list[str]:
    methods: list[str] = []

    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods.append(item.name)

    return sorted(set(methods))


def extract_base_names(node: ast.ClassDef) -> list[str]:
    return [
        get_dotted_name(base)
        for base in node.bases
        if get_dotted_name(base)
    ]


# ============================================================================
# AST file analysis
# ============================================================================

def analyze_file(path: Path, symbols: list[str]) -> FileAnalysis:
    relative = path.relative_to(REPO_ROOT).as_posix()
    analysis = FileAnalysis(
        file=path,
        relative_path=relative,
        is_test=is_test_file(path),
    )

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")

    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        return analysis

    symbol_set = set(symbols)

    for node in ast.walk(tree):

        # ---------------------------------------------------------------
        # Definitions
        # ---------------------------------------------------------------
        if isinstance(node, ast.ClassDef):
            if node.name in symbol_set:
                analysis.definitions.append(
                    SymbolDefinition(
                        symbol=node.name,
                        file=path,
                        relative_path=relative,
                        line=node.lineno,
                        bases=extract_base_names(node),
                        decorator_names=[
                            get_decorator_name(d)
                            for d in node.decorator_list
                        ],
                        fields=extract_class_fields(node),
                        properties=extract_class_properties(node),
                        methods=extract_class_methods(node),
                    )
                )

        # ---------------------------------------------------------------
        # Imports
        # ---------------------------------------------------------------
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                imported = alias.name
                local_name = alias.asname or imported

                if imported in symbol_set:
                    analysis.imports.append(
                        ImportEvidence(
                            file=path,
                            relative_path=relative,
                            line=node.lineno,
                            imported_symbol=imported,
                            module=module,
                            alias=alias.asname,
                        )
                    )

        elif isinstance(node, ast.Import):
            for alias in node.names:
                root_name = alias.name.split(".")[0]

                if root_name in symbol_set:
                    analysis.imports.append(
                        ImportEvidence(
                            file=path,
                            relative_path=relative,
                            line=node.lineno,
                            imported_symbol=root_name,
                            module=alias.name,
                            alias=alias.asname,
                        )
                    )

        # ---------------------------------------------------------------
        # Symbol usages
        # ---------------------------------------------------------------
        elif isinstance(node, ast.Name):
            if node.id in symbol_set:
                context = "name"

                if isinstance(node.ctx, ast.Call):
                    context = "constructor/call"

                analysis.usages.append(
                    SymbolUsage(
                        file=path,
                        relative_path=relative,
                        line=node.lineno,
                        symbol=node.id,
                        context=context,
                    )
                )

        elif isinstance(node, ast.Attribute):
            if node.attr in symbol_set:
                analysis.usages.append(
                    SymbolUsage(
                        file=path,
                        relative_path=relative,
                        line=node.lineno,
                        symbol=node.attr,
                        context="attribute",
                    )
                )

    return analysis


# ============================================================================
# Import-origin resolution
# ============================================================================

def resolve_import_origin(
    import_evidence: ImportEvidence,
    definitions: list[SymbolDefinition],
) -> str:
    """
    Resolve a symbol import against discovered definitions.

    This is intentionally heuristic. It does not execute imports.
    """

    module = import_evidence.module

    candidates = [
        definition
        for definition in definitions
        if definition.symbol == import_evidence.imported_symbol
    ]

    if not candidates:
        return "UNRESOLVED"

    module_tail = module.replace(".", "/")

    exact = [
        definition
        for definition in candidates
        if definition.relative_path.endswith(module_tail + ".py")
    ]

    if len(exact) == 1:
        return exact[0].relative_path

    if len(candidates) == 1:
        return candidates[0].relative_path

    return "AMBIGUOUS"


# ============================================================================
# Semantic comparison
# ============================================================================

def normalize_field(field: str) -> str:
    aliases = {
        "identifier": "identity",
        "source_id": "identity",
        "source": "identity",
        "source_name": "name",
        "url": "website",
        "download_url": "website",
        "api_endpoint": "website",
        "year": "publication_year",
    }

    return aliases.get(field, field)


def semantic_field_groups(
    definitions: list[SymbolDefinition],
) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)

    for definition in definitions:
        for field in definition.fields:
            result[definition.relative_path].add(normalize_field(field))

    return result


def compare_definitions(
    definitions: list[SymbolDefinition],
) -> list[tuple[str, str, set[str]]]:
    results = []

    for index, left in enumerate(definitions):
        for right in definitions[index + 1 :]:
            left_fields = {
                normalize_field(field)
                for field in left.fields
            }

            right_fields = {
                normalize_field(field)
                for field in right.fields
            }

            common = left_fields & right_fields

            if common:
                results.append(
                    (
                        left.relative_path,
                        right.relative_path,
                        common,
                    )
                )

    return results


# ============================================================================
# Reporting helpers
# ============================================================================

def section(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def subsection(title: str) -> None:
    print()
    print("-" * 78)
    print(title)
    print("-" * 78)


def print_definition(definition: SymbolDefinition) -> None:
    print(f"\n{definition.symbol}")
    print(f"  file        : {definition.relative_path}")
    print(f"  line        : {definition.line}")

    print(
        "  bases       : "
        + (", ".join(definition.bases) or "(none)")
    )

    print(
        "  decorators  : "
        + (", ".join(definition.decorator_names) or "(none)")
    )

    print(
        "  fields      : "
        + (", ".join(definition.fields) or "(none)")
    )

    print(
        "  properties  : "
        + (", ".join(definition.properties) or "(none)")
    )

    print(
        "  methods     : "
        + (", ".join(definition.methods) or "(none)")
    )


def print_imports(
    imports: list[ImportEvidence],
    definitions: list[SymbolDefinition],
) -> None:
    for evidence in imports:
        origin = resolve_import_origin(evidence, definitions)

        scope = (
            "TEST"
            if evidence.file and is_test_file(evidence.file)
            else "PROD"
        )

        alias = f" as {evidence.alias}" if evidence.alias else ""

        print(
            f"[{scope}] "
            f"{evidence.relative_path}:{evidence.line} "
            f"imports {evidence.imported_symbol}{alias} "
            f"from {evidence.module} "
            f"-> {origin}"
        )


def print_consumers(
    analyses: list[FileAnalysis],
    definitions: list[SymbolDefinition],
    symbols: list[str],
) -> None:
    definition_files = {
        definition.relative_path
        for definition in definitions
    }

    for analysis in analyses:
        if analysis.relative_path in definition_files:
            continue

        if not analysis.usages:
            continue

        relevant = [
            usage
            for usage in analysis.usages
            if usage.symbol in symbols
        ]

        if not relevant:
            continue

        scope = "TEST" if analysis.is_test else "PROD"

        lines = sorted({usage.line for usage in relevant})

        print(
            f"[{scope}] "
            f"{analysis.relative_path} "
            f"lines={lines}"
        )


def classify_definition_path(path: str) -> str:
    normalized = path.replace("\\", "/").lower()

    if "/validators/" in normalized:
        return "VALIDATOR"

    if "/repositories/" in normalized:
        return "REPOSITORY"

    if "/registries/" in normalized or "/catalog" in normalized:
        return "REGISTRY/CATALOG"

    if "/builders/" in normalized:
        return "BUILDER"

    if "/services/" in normalized:
        return "SERVICE"

    if "/providers/" in normalized:
        return "PROVIDER"

    if "/acquirers/" in normalized:
        return "ACQUIRER"

    if "/models/" in normalized:
        return "MODEL"

    if "/sources/" in normalized:
        return "SOURCE"

    if "/adapters/" in normalized:
        return "ADAPTER"

    if "/pipelines/" in normalized:
        return "PIPELINE"

    return "OTHER"


def print_ownership_summary(
    definitions: list[SymbolDefinition],
    imports: list[ImportEvidence],
) -> None:
    subsection("OWNERSHIP SIGNALS")

    production_imports = [
        item
        for item in imports
        if not is_test_file(item.file)
    ]

    test_imports = [
        item
        for item in imports
        if is_test_file(item.file)
    ]

    print(f"Definitions discovered : {len(definitions)}")
    print(f"Production imports     : {len(production_imports)}")
    print(f"Test imports           : {len(test_imports)}")

    ownership = defaultdict(list)

    for definition in definitions:
        ownership[classify_definition_path(definition.relative_path)].append(
            definition.relative_path
        )

    for category in sorted(ownership):
        print(f"\n{category}:")
        for path in sorted(set(ownership[category])):
            print(f"  - {path}")


def print_semantic_overlap(
    definitions: list[SymbolDefinition],
) -> None:
    subsection("SEMANTIC FIELD OVERLAP")

    comparisons = compare_definitions(definitions)

    if not comparisons:
        print("No common semantic fields detected.")
        return

    for left, right, common in comparisons:
        print(f"\n{left}")
        print(f"vs")
        print(f"{right}")
        print(
            "  common semantic fields: "
            + ", ".join(sorted(common))
        )


def print_architectural_decision(
    definitions: list[SymbolDefinition],
    production_imports: list[ImportEvidence],
) -> None:
    subsection("ARCHITECTURAL SIGNAL")

    if not definitions:
        print("NO-DEFINITION")
        print("No target definition was discovered.")
        return

    if len(definitions) == 1:
        if production_imports:
            print("LIKELY SINGLE ACTIVE MODEL")
            print(
                "One definition has production consumers. "
                "No duplicate target definition was found."
            )
        else:
            print("POSSIBLE ORPHAN")
            print(
                "One definition exists, but no production import "
                "was detected by this static audit."
            )
        return

    # Multiple definitions.
    categories = {
        classify_definition_path(definition.relative_path)
        for definition in definitions
    }

    if len(categories) > 1:
        print("LIKELY DISTINCT REPRESENTATIONS")
        print(
            "Multiple definitions exist in different architectural "
            "locations. Compare ownership and semantics before consolidation."
        )
    else:
        print("DUPLICATE-CANDIDATE")
        print(
            "Multiple definitions exist within similar architectural "
            "locations. Consumer and contract analysis is required."
        )


# ============================================================================
# Target-specific discovery
# ============================================================================

def relevant_path(path: Path, target_config: dict) -> bool:
    relative = path.relative_to(REPO_ROOT).as_posix()

    configured_paths = target_config.get("paths", [])

    if not configured_paths:
        return True

    return any(
        relative == prefix
        or relative.startswith(prefix.rstrip("/") + "/")
        for prefix in configured_paths
    )


def analyze_target(target_name: str, show_code: bool = False) -> None:
    if target_name not in TARGETS:
        valid = ", ".join(sorted(TARGETS))
        raise SystemExit(
            f"Unknown target '{target_name}'. Valid targets: {valid}"
        )

    config = TARGETS[target_name]

    symbols = config["symbols"]

    section("SANSKRITAI ARCHITECTURAL AUDIT")

    print(f"Repository : {REPO_ROOT}")
    print(f"Target     : {target_name}")
    print(f"Symbols    : {', '.join(symbols)}")

    print()
    print("Historical numbered Python files are excluded.")
    print("Generated _G<number>.py audit files are excluded.")
    print("Tests and production code are reported separately.")

    # ---------------------------------------------------------------------
    # Discover files
    # ---------------------------------------------------------------------

    python_files = [
        path
        for path in iter_python_files(REPO_ROOT)
        if relevant_path(path, config)
    ]

    subsection("1. FILE INVENTORY")

    print(f"Python files scanned: {len(python_files)}")

    analyses: list[FileAnalysis] = []

    for path in python_files:
        analysis = analyze_file(path, symbols)
        analyses.append(analysis)

    # ---------------------------------------------------------------------
    # Definitions
    # ---------------------------------------------------------------------

    definitions = [
        definition
        for analysis in analyses
        for definition in analysis.definitions
    ]

    subsection("2. TARGET DEFINITIONS")

    if not definitions:
        print("No target definitions found.")
    else:
        for definition in definitions:
            print_definition(definition)

    # ---------------------------------------------------------------------
    # Imports
    # ---------------------------------------------------------------------

    imports = [
        evidence
        for analysis in analyses
        for evidence in analysis.imports
    ]

    subsection("3. IMPORT / CONSUMER ORIGINS")

    if not imports:
        print("No explicit target imports found.")
    else:
        print_imports(imports, definitions)

    # ---------------------------------------------------------------------
    # Ownership
    # ---------------------------------------------------------------------

    print_ownership_summary(definitions, imports)

    # ---------------------------------------------------------------------
    # Consumers
    # ---------------------------------------------------------------------

    subsection("4. DIRECT SYMBOL CONSUMERS")

    print_consumers(
        analyses=analyses,
        definitions=definitions,
        symbols=symbols,
    )

    # ---------------------------------------------------------------------
    # Production/test split
    # ---------------------------------------------------------------------

    subsection("5. PRODUCTION vs TEST USAGE")

    definition_paths = {
        definition.relative_path
        for definition in definitions
    }

    production_usage = defaultdict(list)
    test_usage = defaultdict(list)

    for analysis in analyses:
        if analysis.relative_path in definition_paths:
            continue

        for usage in analysis.usages:
            if analysis.is_test:
                test_usage[analysis.relative_path].append(usage)
            else:
                production_usage[analysis.relative_path].append(usage)

    print(f"Production consumer files: {len(production_usage)}")
    print(f"Test consumer files      : {len(test_usage)}")

    if production_usage:
        print("\nProduction:")
        for path in sorted(production_usage):
            print(f"  - {path}")

    if test_usage:
        print("\nTests:")
        for path in sorted(test_usage):
            print(f"  - {path}")

    # ---------------------------------------------------------------------
    # Semantic fields
    # ---------------------------------------------------------------------

    print_semantic_overlap(definitions)

    # ---------------------------------------------------------------------
    # Architecture classification
    # ---------------------------------------------------------------------

    production_imports = [
        item
        for item in imports
        if not is_test_file(item.file)
    ]

    print_architectural_decision(
        definitions=definitions,
        production_imports=production_imports,
    )

    # ---------------------------------------------------------------------
    # Semantic ownership matrix
    # ---------------------------------------------------------------------

    subsection("6. FIELD OWNERSHIP MATRIX")

    semantic_fields = config.get("semantic_fields", [])

    if not semantic_fields:
        print(
            "No predefined semantic-field matrix for this target. "
            "Use discovered fields above."
        )
    else:
        for definition in definitions:
            print()
            print(definition.relative_path)

            normalized_fields = {
                normalize_field(field)
                for field in definition.fields
            }

            for field in semantic_fields:
                status = "YES" if normalize_field(field) in normalized_fields else "-"
                print(f"  {field:22} {status}")

    # ---------------------------------------------------------------------
    # Optional source snippets
    # ---------------------------------------------------------------------

    if show_code:
        subsection("7. TARGET SOURCE SNIPPETS")

        for definition in definitions:
            try:
                lines = definition.file.read_text(
                    encoding="utf-8",
                    errors="replace",
                ).splitlines()

                start = max(0, definition.line - 1)
                end = min(len(lines), start + 80)

                print()
                print(f"# {definition.relative_path}")
                print("#" + "-" * 76)

                for index in range(start, end):
                    print(
                        f"{index + 1:5}: "
                        f"{lines[index]}"
                    )

            except OSError as exc:
                print(
                    f"Unable to read {definition.relative_path}: {exc}"
                )

    # ---------------------------------------------------------------------
    # Final concise summary
    # ---------------------------------------------------------------------

    section("AUDIT SUMMARY")

    print(f"Target definitions : {len(definitions)}")
    print(f"Explicit imports   : {len(imports)}")
    print(f"Production users   : {len(production_usage)}")
    print(f"Test users         : {len(test_usage)}")

    if len(definitions) == 0:
        print("\nDecision: NO-DEFINITION")
    elif len(definitions) == 1 and production_usage:
        print("\nDecision: ACTIVE SINGLE MODEL")
    elif len(definitions) > 1:
        print("\nDecision: DUPLICATE-CANDIDATE / DISTINCT-REPRESENTATION REVIEW")
    else:
        print("\nDecision: POSSIBLE ORPHAN / NEEDS REVIEW")

    print()
    print(
        "Guiding principle: "
        "Inspect architecture by ownership first, "
        "semantics second, implementation last."
    )


# ============================================================================
# CLI
# ============================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reusable SanskritAI architectural audit."
    )

    parser.add_argument(
        "--target",
        default="lexical-source",
        choices=sorted(TARGETS),
        help="Architecture target to audit.",
    )

    parser.add_argument(
        "--show-code",
        action="store_true",
        help="Show source snippets around discovered definitions.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    analyze_target(
        target_name=args.target,
        show_code=args.show_code,
    )


if __name__ == "__main__":
    main()
