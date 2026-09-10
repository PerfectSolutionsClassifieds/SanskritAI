from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path("/content/SanskritAI")


# ---------------------------------------------------------------------------
# Historical / duplicate filtering
# ---------------------------------------------------------------------------

def is_historical_duplicate(path: Path) -> bool:
    stem = path.stem

    if re.search(r"\d+$", stem):
        return True

    if re.search(r"_G\d+$", stem, flags=re.IGNORECASE):
        return True

    return False


def is_production_python(path: Path) -> bool:
    if path.suffix != ".py":
        return False

    if "__pycache__" in path.parts:
        return False

    if "tests" in path.parts:
        return False

    if is_historical_duplicate(path):
        return False

    return True


def module_name(path: Path) -> str:
    relative = path.relative_to(ROOT).with_suffix("")
    return ".".join(relative.parts)


# ---------------------------------------------------------------------------
# Target definitions
# ---------------------------------------------------------------------------

TARGETS = {
    (
        "acquisition.knowledge.models.canonical_source",
        "CanonicalSource",
    ),

    (
        "acquisition.models.corpus_source",
        "CorpusSource",
    ),

    (
        "domain.lexical.lexical_source",
        "LexicalSource",
    ),

    (
        "lexical.models.lexical_source",
        "LexicalSource",
    ),

    (
        "acquisition.lexical.monier_williams.monier_williams_source",
        "MonierWilliamsSource",
    ),

    (
        "acquisition.sources.monier_williams",
        "MonierWilliamsSource",
    ),
}


# ---------------------------------------------------------------------------
# Semantic field groups
#
# These are audit concepts only.
# They do NOT modify or imply a production abstraction.
# ---------------------------------------------------------------------------

SEMANTIC_GROUPS = {
    "identity": {
        "source_id",
        "identifier",
        "source",
        "SOURCE",
    },

    "name": {
        "name",
        "title",
        "short_name",
        "source_name",
    },

    "type": {
        "source_type",
    },

    "format": {
        "source_format",
    },

    "version": {
        "version",
    },

    "edition": {
        "edition",
    },

    "language": {
        "language",
    },

    "script": {
        "script",
    },

    "description": {
        "description",
    },

    "author": {
        "author",
    },

    "editor": {
        "editor",
    },

    "publisher": {
        "publisher",
    },

    "publication_year": {
        "publication_year",
        "year",
    },

    "website": {
        "website",
        "url",
    },

    "download": {
        "download_url",
        "download_urls",
    },

    "api": {
        "api_endpoint",
    },

    "license": {
        "license",
    },

    "metadata": {
        "metadata",
    },

    "notes": {
        "notes",
    },

    "encoding": {
        "encoding",
    },

    "acquisition_status": {
        "status",
    },

    "local_storage": {
        "local_path",
        "cache_directory",
    },

    "checksum": {
        "checksum",
        "checksum_algorithm",
    },

    "tags": {
        "tags",
    },
}


# Reverse lookup
FIELD_TO_SEMANTIC = {}

for semantic_name, fields in SEMANTIC_GROUPS.items():
    for field in fields:
        FIELD_TO_SEMANTIC[field] = semantic_name


# ---------------------------------------------------------------------------
# Extract class contract
# ---------------------------------------------------------------------------

def extract_class_contract(path: Path, target_name: str):
    tree = ast.parse(
        path.read_text(encoding="utf-8"),
        filename=str(path),
    )

    for node in ast.walk(tree):

        if not isinstance(node, ast.ClassDef):
            continue

        if node.name != target_name:
            continue

        fields = set()
        methods = set()
        properties = set()
        bases = set()
        decorators = set()

        for base in node.bases:
            try:
                bases.add(ast.unparse(base))
            except Exception:
                pass

        for decorator in node.decorator_list:
            try:
                decorators.add(ast.unparse(decorator))
            except Exception:
                pass

        for item in node.body:

            if isinstance(
                item,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                methods.add(item.name)

                for decorator in item.decorator_list:
                    if (
                        isinstance(decorator, ast.Name)
                        and decorator.id == "property"
                    ):
                        properties.add(item.name)

            elif isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    fields.add(item.target.id)

            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        fields.add(target.id)

        return {
            "line": node.lineno,
            "fields": fields,
            "methods": methods,
            "properties": properties,
            "bases": bases,
            "decorators": decorators,
        }

    return None


# ---------------------------------------------------------------------------
# Discover target definitions
# ---------------------------------------------------------------------------

definitions = []

for path in sorted(ROOT.rglob("*.py")):

    if not is_production_python(path):
        continue

    module = module_name(path)

    for target_module, target_name in TARGETS:

        if module != target_module:
            continue

        contract = extract_class_contract(
            path,
            target_name,
        )

        if contract is None:
            continue

        definitions.append({
            "module": module,
            "name": target_name,
            "path": path,
            **contract,
        })


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def semantic_fields(fields):
    result = {}

    for field in fields:
        semantic = FIELD_TO_SEMANTIC.get(
            field,
            f"UNMAPPED:{field}",
        )

        result.setdefault(semantic, set()).add(field)

    return result


def format_set(values):
    if not values:
        return "(none)"

    return ", ".join(sorted(values))


# ---------------------------------------------------------------------------
# Output individual contracts
# ---------------------------------------------------------------------------

print("=" * 80)
print("SANSKRITAI — ACTIVE SOURCE MODEL CONTRACT COMPARISON")
print("=" * 80)

print()
print(f"Active production definitions: {len(definitions)}")


for item in definitions:

    print()
    print("-" * 80)
    print(item["name"])
    print(f"Module      : {item['module']}")
    print(f"File        : {item['path']}")
    print(f"Line        : {item['line']}")
    print(
        "Decorators  : "
        + format_set(item["decorators"])
    )
    print(
        "Bases       : "
        + format_set(item["bases"])
    )
    print(
        "Fields      : "
        + format_set(item["fields"])
    )
    print(
        "Methods     : "
        + format_set(item["methods"])
    )
    print(
        "Properties  : "
        + format_set(item["properties"])
    )


# ---------------------------------------------------------------------------
# Exact structural comparison
# ---------------------------------------------------------------------------

print()
print("=" * 80)
print("EXACT STRUCTURAL OVERLAP")
print("=" * 80)

for i in range(len(definitions)):

    for j in range(i + 1, len(definitions)):

        left = definitions[i]
        right = definitions[j]

        common_fields = (
            left["fields"] & right["fields"]
        )

        common_methods = (
            left["methods"] & right["methods"]
        )

        common_properties = (
            left["properties"] & right["properties"]
        )

        common_bases = (
            left["bases"] & right["bases"]
        )

        if not any([
            common_fields,
            common_methods,
            common_properties,
            common_bases,
        ]):
            continue

        print()
        print(
            f"{left['module']}.{left['name']}"
        )
        print(
            f"  VS"
        )
        print(
            f"{right['module']}.{right['name']}"
        )

        print(
            f"  Common fields      : "
            f"{format_set(common_fields)}"
        )

        print(
            f"  Common methods     : "
            f"{format_set(common_methods)}"
        )

        print(
            f"  Common properties  : "
            f"{format_set(common_properties)}"
        )

        print(
            f"  Common bases       : "
            f"{format_set(common_bases)}"
        )


# ---------------------------------------------------------------------------
# Semantic comparison
# ---------------------------------------------------------------------------

print()
print("=" * 80)
print("SEMANTIC FIELD OVERLAP")
print("=" * 80)

for i in range(len(definitions)):

    for j in range(i + 1, len(definitions)):

        left = definitions[i]
        right = definitions[j]

        left_semantic = semantic_fields(
            left["fields"]
        )

        right_semantic = semantic_fields(
            right["fields"]
        )

        common_semantics = (
            set(left_semantic)
            & set(right_semantic)
        )

        if not common_semantics:
            continue

        print()
        print(
            f"{left['module']}.{left['name']}"
        )
        print(
            f"  VS"
        )
        print(
            f"{right['module']}.{right['name']}"
        )

        for semantic in sorted(common_semantics):

            left_fields = left_semantic[semantic]
            right_fields = right_semantic[semantic]

            print(
                f"  {semantic:20s}: "
                f"{format_set(left_fields)}"
                f"  <->  "
                f"{format_set(right_fields)}"
            )


# ---------------------------------------------------------------------------
# Semantic identity summary
# ---------------------------------------------------------------------------

print()
print("=" * 80)
print("SEMANTIC CONTRACT SUMMARY")
print("=" * 80)

for item in definitions:

    semantic = semantic_fields(
        item["fields"]
    )

    print()
    print(
        f"{item['module']}.{item['name']}"
    )

    for concept in sorted(semantic):
        print(
            f"  {concept:20s}: "
            f"{format_set(semantic[concept])}"
        )


# ---------------------------------------------------------------------------
# Architectural observations generated from structure
# ---------------------------------------------------------------------------

print()
print("=" * 80)
print("ARCHITECTURAL SIGNALS")
print("=" * 80)

print()
print("1. Acquisition-state concentration:")

for item in definitions:
    acquisition_fields = (
        semantic_fields(item["fields"])
        .keys()
    )

    relevant = {
        "acquisition_status",
        "download",
        "local_storage",
        "checksum",
        "tags",
    } & acquisition_fields

    if relevant:
        print(
            f"  - {item['module']}.{item['name']}"
            f" -> {format_set(relevant)}"
        )

print()
print("2. Lexical-source semantic overlap:")

lexical_defs = [
    item for item in definitions
    if item["name"] == "LexicalSource"
]

if len(lexical_defs) == 2:

    left, right = lexical_defs

    left_semantic = semantic_fields(left["fields"])
    right_semantic = semantic_fields(right["fields"])

    common = (
        set(left_semantic)
        & set(right_semantic)
    )

    print(
        f"  {left['module']}"
    )
    print(
        f"  {right['module']}"
    )
    print(
        f"  Shared semantic concepts: "
        f"{format_set(common)}"
    )

else:
    print("  Expected two active LexicalSource definitions.")

print()
print("3. Monier-Williams source separation:")

mw_defs = [
    item for item in definitions
    if item["name"] == "MonierWilliamsSource"
]

for item in mw_defs:
    print(
        f"  - {item['module']}"
        f" -> fields={len(item['fields'])}, "
        f"methods={len(item['methods'])}"
    )

print()
print("Interpretation:")
print(
    "  The audit reports structural and semantic overlap only."
)
print(
    "  It does NOT recommend consolidation automatically."
)
print(
    "  Production architecture must be decided from ownership,"
)
print(
    "  lifecycle, consumers, and construction boundaries."
)


print()
print("=" * 80)
print("HISTORICAL / DUPLICATE FILE FILTER")
print("=" * 80)
print()
print("Excluded:")
print("  *<number>.py")
print("  *_G<number>.py")
print("  tests/")
print("  __pycache__/")

print()
print("=" * 80)
print("AUDIT COMPLETE — NO FILES MODIFIED")
print("=" * 80)
