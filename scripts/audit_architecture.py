
"""
SanskritAI — Reusable Architectural Audit Engine
=================================================

Architecture-first inspection tool.

Primary principle
-----------------
    Ownership -> Boundary -> Semantics -> Contract -> Implementation

This script is intentionally READ-ONLY.

It does not:
    - modify production code
    - import project modules
    - execute application code
    - instantiate domain models
    - make architectural changes

It statically analyzes Python source using AST.

Historical files
----------------
Files ending with numeric suffixes are ignored:

    example1.py
    example2.py
    test_example3.py

Generated audit variants are also ignored:

    *_G1.py
    *_G2.py

Targets
-------
    lexical-source
    corpus-source
    canonical-source
    monier-williams-source
    all-sources

Examples
--------
    !cd /content/SanskritAI && \
        python scripts/audit_architecture.py \
        --target lexical-source

    !cd /content/SanskritAI && \
        python scripts/audit_architecture.py \
        --target all-sources

    !cd /content/SanskritAI && \
        python scripts/audit_architecture.py \
        --target lexical-source \
        --show-code

    !cd /content/SanskritAI && \
        python scripts/audit_architecture.py \
        --target lexical-source \
        --view summary

    !cd /content/SanskritAI && \
        python scripts/audit_architecture.py \
        --target lexical-source \
        --view boundaries

Views
-----
    full
    summary
    definitions
    ownership
    semantics
    boundaries
    contracts

Default:
    full
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
# Repository configuration
# ============================================================================

REPO_ROOT = Path(__file__).resolve().parents[1]

PACKAGE_ROOT = "SanskritAI"

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

NUMBERED_FILE_RE = re.compile(
    r"\d+\.py$",
    re.IGNORECASE,
)

GENERATED_AUDIT_RE = re.compile(
    r"_G\d+\.py$",
    re.IGNORECASE,
)


TARGETS = {
    "lexical-source": {
        "label": "LexicalSource",
        "symbols": ["LexicalSource"],
        "paths": [
            "domain/lexical",
            "lexical",
        ],
        "semantic_aliases": {
            "source_id": "identity",
            "identifier": "identity",
            "source": "identity",
            "source_name": "name",
            "url": "external_reference",
            "website": "external_reference",
            "download_url": "external_reference",
            "api_endpoint": "external_reference",
            "year": "publication_year",
        },
    },

    "corpus-source": {
        "label": "CorpusSource",
        "symbols": ["CorpusSource"],
        "paths": [
            "acquisition",
            "corpus",
        ],
        "semantic_aliases": {
            "source_id": "identity",
            "identifier": "identity",
            "source_name": "name",
            "year": "publication_year",
            "url": "external_reference",
            "website": "external_reference",
        },
    },

    "canonical-source": {
        "label": "CanonicalSource",
        "symbols": ["CanonicalSource"],
        "paths": [
            "acquisition",
            "domain",
            "corpus",
        ],
        "semantic_aliases": {
            "source_id": "identity",
            "identifier": "identity",
            "source_name": "name",
            "url": "external_reference",
            "website": "external_reference",
            "download_url": "external_reference",
            "api_endpoint": "external_reference",
            "year": "publication_year",
        },
    },

    "monier-williams-source": {
        "label": "MonierWilliamsSource",
        "symbols": [
            "MonierWilliamsSource",
        ],
        "paths": [
            "acquisition",
            "domain",
        ],
        "semantic_aliases": {
            "source_id": "identity",
            "identifier": "identity",
            "source": "identity",
            "source_name": "name",
            "year": "publication_year",
        },
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
        "semantic_aliases": {
            "source_id": "identity",
            "identifier": "identity",
            "source": "identity",
            "source_name": "name",
            "url": "external_reference",
            "website": "external_reference",
            "download_url": "external_reference",
            "api_endpoint": "external_reference",
            "year": "publication_year",
        },
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
    module_name: str
    line: int
    bases: list[str] = field(default_factory=list)
    decorators: list[str] = field(default_factory=list)
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
    resolved_origin: str = "UNRESOLVED"


@dataclass
class UsageEvidence:
    file: Path
    relative_path: str
    line: int
    symbol: str
    context: str


@dataclass
class FileAnalysis:
    file: Path
    relative_path: str
    module_name: str
    is_test: bool

    definitions: list[SymbolDefinition] = field(
        default_factory=list
    )

    imports: list[ImportEvidence] = field(
        default_factory=list
    )

    usages: list[UsageEvidence] = field(
        default_factory=list
    )


# ============================================================================
# File filtering
# ============================================================================

def is_ignored_file(path: Path) -> bool:
    name = path.name

    if NUMBERED_FILE_RE.search(name):
        return True

    if GENERATED_AUDIT_RE.search(name):
        return True

    return False


def is_ignored_directory(path: Path) -> bool:
    return any(
        part in IGNORED_DIRECTORIES
        for part in path.parts
    )


def is_test_file(path: Path) -> bool:
    parts = {
        part.lower()
        for part in path.parts
    }

    return (
        "tests" in parts
        or path.name.startswith("test_")
    )


def iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):

        if is_ignored_directory(path):
            continue

        if is_ignored_file(path):
            continue

        yield path


# ============================================================================
# Module naming
# ============================================================================

def module_name_from_path(path: Path) -> str:
    relative = path.relative_to(REPO_ROOT)

    parts = list(relative.parts)

    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1][:-3]

    return ".".join(
        [PACKAGE_ROOT] + parts
    )


def module_to_relative_path(module: str) -> str:
    """
    Convert:

        SanskritAI.lexical.models.lexical_source

    into:

        lexical/models/lexical_source.py
    """

    prefix = PACKAGE_ROOT + "."

    if module.startswith(prefix):
        module = module[len(prefix):]

    return module.replace(".", "/") + ".py"


# ============================================================================
# AST helpers
# ============================================================================

def dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)

        if parent:
            return f"{parent}.{node.attr}"

        return node.attr

    return ""


def decorator_name(node: ast.AST) -> str:
    if isinstance(node, ast.Call):
        return dotted_name(node.func)

    return dotted_name(node)


def extract_fields(
    node: ast.ClassDef,
) -> list[str]:

    fields: set[str] = set()

    for item in node.body:

        if isinstance(item, ast.AnnAssign):
            if isinstance(item.target, ast.Name):
                fields.add(item.target.id)

        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    fields.add(target.id)

    return sorted(fields)


def extract_properties(
    node: ast.ClassDef,
) -> list[str]:

    properties = []

    for item in node.body:

        if not isinstance(
            item,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            continue

        for decorator in item.decorator_list:

            name = decorator_name(decorator)

            if name.endswith("property"):
                properties.append(item.name)

    return sorted(set(properties))


def extract_methods(
    node: ast.ClassDef,
) -> list[str]:

    return sorted(
        {
            item.name
            for item in node.body
            if isinstance(
                item,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
        }
    )


def extract_bases(
    node: ast.ClassDef,
) -> list[str]:

    return sorted(
        {
            dotted_name(base)
            for base in node.bases
            if dotted_name(base)
        }
    )


# ============================================================================
# File analysis
# ============================================================================

def analyze_file(
    path: Path,
    symbols: list[str],
) -> FileAnalysis:

    relative = path.relative_to(REPO_ROOT).as_posix()

    module_name = module_name_from_path(path)

    result = FileAnalysis(
        file=path,
        relative_path=relative,
        module_name=module_name,
        is_test=is_test_file(path),
    )

    try:
        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        tree = ast.parse(
            text,
            filename=str(path),
        )

    except (
        OSError,
        SyntaxError,
    ):
        return result

    symbol_set = set(symbols)

    for node in ast.walk(tree):

        # ---------------------------------------------------------------
        # Class definitions
        # ---------------------------------------------------------------

        if isinstance(node, ast.ClassDef):

            if node.name in symbol_set:

                result.definitions.append(
                    SymbolDefinition(
                        symbol=node.name,
                        file=path,
                        relative_path=relative,
                        module_name=module_name,
                        line=node.lineno,
                        bases=extract_bases(node),
                        decorators=[
                            decorator_name(d)
                            for d in node.decorator_list
                        ],
                        fields=extract_fields(node),
                        properties=extract_properties(node),
                        methods=extract_methods(node),
                    )
                )

        # ---------------------------------------------------------------
        # from x import Symbol
        # ---------------------------------------------------------------

        elif isinstance(
            node,
            ast.ImportFrom,
        ):

            module = node.module or ""

            for alias in node.names:

                imported_symbol = alias.name

                if imported_symbol not in symbol_set:
                    continue

                result.imports.append(
                    ImportEvidence(
                        file=path,
                        relative_path=relative,
                        line=node.lineno,
                        imported_symbol=imported_symbol,
                        module=module,
                        alias=alias.asname,
                    )
                )

        # ---------------------------------------------------------------
        # import x
        # ---------------------------------------------------------------

        elif isinstance(
            node,
            ast.Import,
        ):

            for alias in node.names:

                imported_root = alias.name.split(".")[0]

                if imported_root not in symbol_set:
                    continue

                result.imports.append(
                    ImportEvidence(
                        file=path,
                        relative_path=relative,
                        line=node.lineno,
                        imported_symbol=imported_root,
                        module=alias.name,
                        alias=alias.asname,
                    )
                )

        # ---------------------------------------------------------------
        # Symbol usage
        # ---------------------------------------------------------------

        elif isinstance(node, ast.Name):

            if node.id not in symbol_set:
                continue

            context = "reference"

            if isinstance(node.ctx, ast.Store):
                context = "assignment"

            result.usages.append(
                UsageEvidence(
                    file=path,
                    relative_path=relative,
                    line=node.lineno,
                    symbol=node.id,
                    context=context,
                )
            )

        elif isinstance(node, ast.Attribute):

            if node.attr not in symbol_set:
                continue

            result.usages.append(
                UsageEvidence(
                    file=path,
                    relative_path=relative,
                    line=node.lineno,
                    symbol=node.attr,
                    context="attribute",
                )
            )

    return result


# ============================================================================
# Definition index
# ============================================================================

def build_definition_index(
    analyses: list[FileAnalysis],
) -> dict[str, list[SymbolDefinition]]:

    index: dict[
        str,
        list[SymbolDefinition],
    ] = defaultdict(list)

    for analysis in analyses:

        for definition in analysis.definitions:

            index[definition.symbol].append(
                definition
            )

    return index


# ============================================================================
# Import resolution
# ============================================================================

def resolve_import(
    evidence: ImportEvidence,
    definition_index: dict[str, list[SymbolDefinition]],
) -> str:

    candidates = definition_index.get(
        evidence.imported_symbol,
        [],
    )

    if not candidates:
        return "UNRESOLVED"

    # ---------------------------------------------------------------
    # Exact module path match.
    # ---------------------------------------------------------------

    expected_path = module_to_relative_path(
        (
            f"{PACKAGE_ROOT}."
            f"{evidence.module}"
        )
    )

    exact = [
        definition
        for definition in candidates
        if definition.relative_path == expected_path
    ]

    if len(exact) == 1:
        return exact[0].relative_path

    # ---------------------------------------------------------------
    # If only one candidate exists, resolve directly.
    # ---------------------------------------------------------------

    if len(candidates) == 1:
        return candidates[0].relative_path

    # ---------------------------------------------------------------
    # Explicit source module path may match by suffix.
    # ---------------------------------------------------------------

    suffix = module_to_relative_path(
        evidence.module
    )

    suffix_matches = [
        definition
        for definition in candidates
        if definition.relative_path.endswith(suffix)
    ]

    if len(suffix_matches) == 1:
        return suffix_matches[0].relative_path

    return "AMBIGUOUS"


def resolve_all_imports(
    analyses: list[FileAnalysis],
) -> None:

    index = build_definition_index(
        analyses
    )

    for analysis in analyses:

        for evidence in analysis.imports:

            evidence.resolved_origin = resolve_import(
                evidence,
                index,
            )


# ============================================================================
# Semantic normalization
# ============================================================================

def semantic_field(
    field: str,
    aliases: dict[str, str],
) -> str:

    return aliases.get(
        field,
        field,
    )


def semantic_fields(
    definition: SymbolDefinition,
    aliases: dict[str, str],
) -> set[str]:

    return {
        semantic_field(
            field,
            aliases,
        )
        for field in definition.fields
    }


# ============================================================================
# Architecture classification
# ============================================================================

def layer_for_path(
    relative_path: str,
) -> str:

    normalized = relative_path.replace(
        "\\",
        "/",
    ).lower()

    if normalized.startswith("domain/"):
        return "DOMAIN"

    if normalized.startswith("lexical/"):
        return "LEXICAL"

    if normalized.startswith("acquisition/"):
        return "ACQUISITION"

    if normalized.startswith("corpus/"):
        return "CORPUS"

    if normalized.startswith("core/"):
        return "CORE"

    if normalized.startswith("models/"):
        return "MODELS"

    if normalized.startswith("services/"):
        return "SERVICES"

    if normalized.startswith("pipeline/"):
        return "PIPELINE"

    return "OTHER"


def component_for_path(
    relative_path: str,
) -> str:

    normalized = relative_path.replace(
        "\\",
        "/",
    ).lower()

    mappings = [
        ("/validators/", "VALIDATOR"),
        ("/repositories/", "REPOSITORY"),
        ("/registries/", "REGISTRY"),
        ("/indexes/", "INDEX"),
        ("/catalog", "CATALOG"),
        ("/builders/", "BUILDER"),
        ("/services/", "SERVICE"),
        ("/providers/", "PROVIDER"),
        ("/acquirers/", "ACQUIRER"),
        ("/adapters/", "ADAPTER"),
        ("/pipelines/", "PIPELINE"),
        ("/models/", "MODEL"),
        ("/sources/", "SOURCE"),
    ]

    for marker, label in mappings:

        if marker in normalized:
            return label

    return "OTHER"


# ============================================================================
# Reporting
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


def print_definitions(
    definitions: list[SymbolDefinition],
) -> None:

    subsection("TARGET DEFINITIONS")

    if not definitions:

        print("No target definitions discovered.")
        return

    for definition in definitions:

        print()
        print(definition.symbol)

        print(
            f"  file        : "
            f"{definition.relative_path}"
        )

        print(
            f"  module      : "
            f"{definition.module_name}"
        )

        print(
            f"  line        : "
            f"{definition.line}"
        )

        print(
            f"  layer       : "
            f"{layer_for_path(definition.relative_path)}"
        )

        print(
            f"  component   : "
            f"{component_for_path(definition.relative_path)}"
        )

        print(
            "  bases       : "
            + (
                ", ".join(definition.bases)
                or "(none)"
            )
        )

        print(
            "  decorators  : "
            + (
                ", ".join(definition.decorators)
                or "(none)"
            )
        )

        print(
            "  fields      : "
            + (
                ", ".join(definition.fields)
                or "(none)"
            )
        )

        print(
            "  properties  : "
            + (
                ", ".join(definition.properties)
                or "(none)"
            )
        )

        print(
            "  methods     : "
            + (
                ", ".join(definition.methods)
                or "(none)"
            )
        )


def print_imports(
    analyses: list[FileAnalysis],
) -> None:

    subsection(
        "IMPORT OWNERSHIP / RESOLUTION"
    )

    imports = [
        evidence
        for analysis in analyses
        for evidence in analysis.imports
    ]

    if not imports:

        print("No explicit imports discovered.")
        return

    for evidence in imports:

        scope = (
            "TEST"
            if is_test_file(evidence.file)
            else "PROD"
        )

        alias = (
            f" as {evidence.alias}"
            if evidence.alias
            else ""
        )

        print(
            f"[{scope}] "
            f"{evidence.relative_path}:"
            f"{evidence.line} "
            f"imports "
            f"{evidence.imported_symbol}"
            f"{alias} "
            f"from "
            f"{PACKAGE_ROOT}."
            f"{evidence.module} "
            f"-> "
            f"{evidence.resolved_origin}"
        )


def print_consumers(
    analyses: list[FileAnalysis],
    definitions: list[SymbolDefinition],
    symbols: list[str],
) -> None:

    subsection(
        "PRODUCTION CONSUMERS"
    )

    definition_files = {
        definition.relative_path
        for definition in definitions
    }

    consumers = {}

    for analysis in analyses:

        if analysis.is_test:
            continue

        if analysis.relative_path in definition_files:
            continue

        usages = [
            usage
            for usage in analysis.usages
            if usage.symbol in symbols
        ]

        if usages:
            consumers[
                analysis.relative_path
            ] = usages

    if not consumers:

        print(
            "No production consumers detected."
        )
        return

    for path in sorted(consumers):

        usages = consumers[path]

        lines = sorted(
            {
                usage.line
                for usage in usages
            }
        )

        print(
            f"[{layer_for_path(path)}] "
            f"{component_for_path(path)} "
            f"{path} "
            f"lines={lines}"
        )


def print_test_consumers(
    analyses: list[FileAnalysis],
    definitions: list[SymbolDefinition],
    symbols: list[str],
) -> None:

    subsection(
        "TEST CONSUMERS"
    )

    definition_files = {
        definition.relative_path
        for definition in definitions
    }

    consumers = {}

    for analysis in analyses:

        if not analysis.is_test:
            continue

        if analysis.relative_path in definition_files:
            continue

        usages = [
            usage
            for usage in analysis.usages
            if usage.symbol in symbols
        ]

        if usages:
            consumers[
                analysis.relative_path
            ] = usages

    if not consumers:

        print("No test consumers detected.")
        return

    for path in sorted(consumers):

        lines = sorted(
            {
                usage.line
                for usage in consumers[path]
            }
        )

        print(
            f"{path} lines={lines}"
        )


def print_exact_semantics(
    definitions: list[SymbolDefinition],
) -> None:

    subsection(
        "EXACT FIELD COMPARISON"
    )

    for index, left in enumerate(definitions):

        for right in definitions[index + 1:]:

            common = (
                set(left.fields)
                & set(right.fields)
            )

            only_left = (
                set(left.fields)
                - set(right.fields)
            )

            only_right = (
                set(right.fields)
                - set(left.fields)
            )

            print()
            print(left.relative_path)
            print("vs")
            print(right.relative_path)

            print(
                "  exact common fields: "
                + (
                    ", ".join(
                        sorted(common)
                    )
                    or "(none)"
                )
            )

            print(
                "  left-only fields: "
                + (
                    ", ".join(
                        sorted(only_left)
                    )
                    or "(none)"
                )
            )

            print(
                "  right-only fields: "
                + (
                    ", ".join(
                        sorted(only_right)
                    )
                    or "(none)"
                )
            )


def print_semantic_equivalence(
    definitions: list[SymbolDefinition],
    aliases: dict[str, str],
) -> None:

    subsection(
        "SEMANTIC FIELD COMPARISON"
    )

    for index, left in enumerate(definitions):

        for right in definitions[index + 1:]:

            left_semantic = semantic_fields(
                left,
                aliases,
            )

            right_semantic = semantic_fields(
                right,
                aliases,
            )

            common = (
                left_semantic
                & right_semantic
            )

            print()
            print(left.relative_path)
            print("vs")
            print(right.relative_path)

            print(
                "  semantic overlap: "
                + (
                    ", ".join(
                        sorted(common)
                    )
                    or "(none)"
                )
            )


def print_boundary_analysis(
    analyses: list[FileAnalysis],
    definitions: list[SymbolDefinition],
) -> None:

    subsection(
        "ARCHITECTURAL BOUNDARY ANALYSIS"
    )

    definition_map = {
        definition.relative_path:
            definition
        for definition in definitions
    }

    print("Target definitions by layer:")

    for definition in definitions:

        print(
            f"  "
            f"{layer_for_path(definition.relative_path):12} "
            f"{component_for_path(definition.relative_path):14} "
            f"{definition.relative_path}"
        )

    print()
    print("Production imports by boundary:")

    boundaries = defaultdict(list)

    for analysis in analyses:

        if analysis.is_test:
            continue

        consumer_layer = layer_for_path(
            analysis.relative_path
        )

        for evidence in analysis.imports:

            origin = evidence.resolved_origin

            if origin in definition_map:

                origin_layer = layer_for_path(
                    origin
                )

                if consumer_layer != origin_layer:

                    key = (
                        consumer_layer,
                        origin_layer,
                    )

                    boundaries[key].append(
                        (
                            analysis.relative_path,
                            origin,
                            evidence.line,
                        )
                    )

    if not boundaries:

        print(
            "  No cross-layer imports of the "
            "target definitions detected."
        )

    else:

        for (
            consumer_layer,
            origin_layer,
        ) in sorted(boundaries):

            print()
            print(
                f"  {consumer_layer} -> "
                f"{origin_layer}"
            )

            for (
                consumer,
                origin,
                line,
            ) in boundaries[
                (
                    consumer_layer,
                    origin_layer,
                )
            ]:

                print(
                    f"    {consumer}:{line}"
                    f" -> {origin}"
                )


def print_contract_signals(
    definitions: list[SymbolDefinition],
) -> None:

    subsection(
        "CONTRACT DIFFERENCE SIGNALS"
    )

    for index, left in enumerate(definitions):

        for right in definitions[index + 1:]:

            print()
            print(
                f"{left.relative_path}"
            )
            print(
                f"vs"
            )
            print(
                f"{right.relative_path}"
            )

            left_methods = set(
                left.methods
            )

            right_methods = set(
                right.methods
            )

            common_methods = (
                left_methods
                & right_methods
            )

            left_only = (
                left_methods
                - right_methods
            )

            right_only = (
                right_methods
                - left_methods
            )

            print(
                "  common methods: "
                + (
                    ", ".join(
                        sorted(common_methods)
                    )
                    or "(none)"
                )
            )

            print(
                "  left-only methods: "
                + (
                    ", ".join(
                        sorted(left_only)
                    )
                    or "(none)"
                )
            )

            print(
                "  right-only methods: "
                + (
                    ", ".join(
                        sorted(right_only)
                    )
                    or "(none)"
                )
            )


def classify_architecture(
    definitions: list[SymbolDefinition],
    analyses: list[FileAnalysis],
) -> str:

    if not definitions:
        return "NO-DEFINITION"

    if len(definitions) == 1:
        definition = definitions[0]

        production_imports = [
            evidence
            for analysis in analyses
            if not analysis.is_test
            for evidence in analysis.imports
            if evidence.resolved_origin
            == definition.relative_path
        ]

        if production_imports:
            return "ACTIVE-SINGLE-MODEL"

        return "POSSIBLE-ORPHAN"

    layers = {
        layer_for_path(
            definition.relative_path
        )
        for definition in definitions
    }

    if len(layers) > 1:
        return "DISTINCT-REPRESENTATIONS-REVIEW"

    return "DUPLICATE-CANDIDATE"


def print_decision(
    definitions: list[SymbolDefinition],
    analyses: list[FileAnalysis],
) -> None:

    subsection(
        "ARCHITECTURAL DECISION SIGNAL"
    )

    decision = classify_architecture(
        definitions,
        analyses,
    )

    if decision == "NO-DEFINITION":

        print("NO-DEFINITION")

        return

    if decision == "ACTIVE-SINGLE-MODEL":

        print(
            "ACTIVE SINGLE MODEL"
        )

        print(
            "One active production representation "
            "was discovered."
        )

        return

    if decision == "POSSIBLE-ORPHAN":

        print(
            "POSSIBLE ORPHAN"
        )

        print(
            "No production import was statically "
            "resolved to the definition."
        )

        return

    if decision == "DISTINCT-REPRESENTATIONS-REVIEW":

        print(
            "DISTINCT REPRESENTATIONS — "
            "DO NOT CONSOLIDATE YET"
        )

        print(
            "Definitions exist in different "
            "architectural layers."
        )

        print(
            "First establish ownership and "
            "boundary contracts."
        )

        return

    print(
        "DUPLICATE CANDIDATE — "
        "REQUIRES CONTRACT REVIEW"
    )


# ============================================================================
# Source snippets
# ============================================================================

def print_source_snippets(
    definitions: list[SymbolDefinition],
) -> None:

    subsection(
        "TARGET SOURCE SNIPPETS"
    )

    for definition in definitions:

        try:

            lines = definition.file.read_text(
                encoding="utf-8",
                errors="replace",
            ).splitlines()

        except OSError as exc:

            print(
                f"Unable to read "
                f"{definition.relative_path}: "
                f"{exc}"
            )

            continue

        start = max(
            0,
            definition.line - 1,
        )

        end = min(
            len(lines),
            start + 100,
        )

        print()
        print(
            f"# {definition.relative_path}"
        )

        print(
            "#" + "-" * 76
        )

        for index in range(
            start,
            end,
        ):

            print(
                f"{index + 1:5}: "
                f"{lines[index]}"
            )


# ============================================================================
# Main audit
# ============================================================================

def run_audit(
    target_name: str,
    view: str = "full",
    show_code: bool = False,
) -> None:

    if target_name not in TARGETS:

        raise SystemExit(
            f"Unknown target: {target_name}"
        )

    config = TARGETS[
        target_name
    ]

    symbols = config[
        "symbols"
    ]

    section(
        "SANSKRITAI ARCHITECTURAL AUDIT"
    )

    print(
        f"Repository : {REPO_ROOT}"
    )

    print(
        f"Target     : {target_name}"
    )

    print(
        f"Symbols    : "
        f"{', '.join(symbols)}"
    )

    print()
    print(
        "Historical numbered Python files "
        "are excluded."
    )

    print(
        "Generated _G<number>.py files "
        "are excluded."
    )

    print(
        "Production and test code are "
        "analyzed separately."
    )

    python_files = [
        path
        for path in iter_python_files(
            REPO_ROOT
        )
        if (
            not config["paths"]
            or any(
                path.relative_to(
                    REPO_ROOT
                ).as_posix() == prefix
                or
                path.relative_to(
                    REPO_ROOT
                ).as_posix().startswith(
                    prefix.rstrip("/") + "/"
                )
                for prefix in config["paths"]
            )
        )
    ]

    print()
    print(
        f"Python files scanned: "
        f"{len(python_files)}"
    )

    analyses = [
        analyze_file(
            path,
            symbols,
        )
        for path in python_files
    ]

    resolve_all_imports(
        analyses
    )

    definitions = [
        definition
        for analysis in analyses
        for definition in analysis.definitions
    ]

    views = {
        "full",
        "summary",
        "definitions",
        "ownership",
        "semantics",
        "boundaries",
        "contracts",
    }

    if view not in views:

        raise SystemExit(
            f"Unknown view: {view}"
        )

    if view in {
        "full",
        "definitions",
    }:

        print_definitions(
            definitions
        )

    if view in {
        "full",
        "ownership",
    }:

        print_imports(
            analyses
        )

        print_consumers(
            analyses,
            definitions,
            symbols,
        )

        print_test_consumers(
            analyses,
            definitions,
            symbols,
        )

    if view in {
        "full",
        "semantics",
    }:

        print_exact_semantics(
            definitions
        )

        print_semantic_equivalence(
            definitions,
            config[
                "semantic_aliases"
            ],
        )

    if view in {
        "full",
        "boundaries",
    }:

        print_boundary_analysis(
            analyses,
            definitions,
        )

    if view in {
        "full",
        "contracts",
    }:

        print_contract_signals(
            definitions
        )

    if view in {
        "full",
        "summary",
    }:

        print_decision(
            definitions,
            analyses,
        )

    if show_code:

        print_source_snippets(
            definitions
        )

    section(
        "AUDIT SUMMARY"
    )

    production_imports = [
        evidence
        for analysis in analyses
        if not analysis.is_test
        for evidence in analysis.imports
    ]

    production_resolved = [
        evidence
        for evidence in production_imports
        if evidence.resolved_origin
        not in {
            "UNRESOLVED",
            "AMBIGUOUS",
        }
    ]

    production_consumers = set()

    for analysis in analyses:

        if analysis.is_test:
            continue

        if any(
            usage.symbol in symbols
            for usage in analysis.usages
        ):

            production_consumers.add(
                analysis.relative_path
            )

    test_consumers = set()

    for analysis in analyses:

        if not analysis.is_test:
            continue

        if any(
            usage.symbol in symbols
            for usage in analysis.usages
        ):

            test_consumers.add(
                analysis.relative_path
            )

    print(
        f"Target definitions : "
        f"{len(definitions)}"
    )

    print(
        f"Production imports : "
        f"{len(production_imports)}"
    )

    print(
        f"Resolved imports   : "
        f"{len(production_resolved)}"
    )

    print(
        f"Production users   : "
        f"{len(production_consumers)}"
    )

    print(
        f"Test users         : "
        f"{len(test_consumers)}"
    )

    print()

    decision = classify_architecture(
        definitions,
        analyses,
    )

    print(
        f"Decision: {decision}"
    )

    print()
    print(
        "Guiding principle:"
    )

    print(
        "Inspect architecture by "
        "ownership first, "
        "boundary second, "
        "semantics third, "
        "contract fourth, "
        "implementation last."
    )


# ============================================================================
# CLI
# ============================================================================

def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description=(
            "Reusable SanskritAI "
            "architectural audit engine."
        )
    )

    parser.add_argument(
        "--target",
        default="lexical-source",
        choices=sorted(TARGETS),
    )

    parser.add_argument(
        "--view",
        default="full",
        choices=[
            "full",
            "summary",
            "definitions",
            "ownership",
            "semantics",
            "boundaries",
            "contracts",
        ],
    )

    parser.add_argument(
        "--show-code",
        action="store_true",
        help=(
            "Show source snippets "
            "after architectural analysis."
        ),
    )

    return parser


def main() -> None:

    parser = build_parser()

    args = parser.parse_args()

    run_audit(
        target_name=args.target,
        view=args.view,
        show_code=args.show_code,
    )


if __name__ == "__main__":
    main()
