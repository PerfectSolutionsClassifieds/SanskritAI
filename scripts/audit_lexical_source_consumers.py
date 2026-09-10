from __future__ import annotations

import ast
import re
from pathlib import Path
from collections import defaultdict


ROOT = Path("/content/SanskritAI")


# ============================================================================
# FILE FILTERING
# ============================================================================

def is_historical_duplicate(path: Path) -> bool:
    """
    Exclude historical numbered copies:

        mapper1.py
        mapper2.py
        source4.py

    Also exclude generation copies:

        source_G1.py
        canonical_lexicon_G4.py
    """
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


# ============================================================================
# TARGETS
# ============================================================================

DOMAIN_LEXICAL_SOURCE = (
    "domain.lexical.lexical_source",
    "LexicalSource",
)

MODEL_LEXICAL_SOURCE = (
    "lexical.models.lexical_source",
    "LexicalSource",
)

TARGETS = {
    DOMAIN_LEXICAL_SOURCE,
    MODEL_LEXICAL_SOURCE,
}


# ============================================================================
# IMPORT RESOLUTION
# ============================================================================

def resolve_relative_import(
    current_module: str,
    node: ast.ImportFrom,
) -> str | None:
    """
    Resolve imports such as:

        from .lexical_source import LexicalSource
        from ..models.lexical_source import LexicalSource
    """

    if node.level == 0:
        return node.module

    parts = current_module.split(".")

    # current_module points to a module, not a package.
    package_parts = parts[:-1]

    if node.level > len(package_parts):
        return node.module

    base = package_parts[: len(package_parts) - node.level + 1]

    if node.module:
        base.extend(node.module.split("."))

    return ".".join(base)


def imported_lexical_sources(
    tree: ast.AST,
    current_module: str,
):
    """
    Return aliases mapped to the exact LexicalSource implementation.
    """

    aliases = {}

    for node in ast.walk(tree):

        if not isinstance(node, ast.ImportFrom):
            continue

        resolved_module = resolve_relative_import(
            current_module,
            node,
        )

        if resolved_module is None:
            continue

        for alias in node.names:

            if alias.name != "LexicalSource":
                continue

            target = (
                resolved_module,
                "LexicalSource",
            )

            if target not in TARGETS:
                continue

            local_name = alias.asname or alias.name

            aliases[local_name] = target

    return aliases


# ============================================================================
# AST HELPERS
# ============================================================================

def expression_contains_alias(node, aliases):
    """
    Return target models referenced by an AST expression.
    """

    found = []

    for child in ast.walk(node):

        if isinstance(child, ast.Name):
            target = aliases.get(child.id)

            if target is not None:
                found.append(target)

    return found


def annotation_text(annotation):
    if annotation is None:
        return None

    try:
        return ast.unparse(annotation)
    except Exception:
        return None


def call_is_target(node: ast.Call, aliases):
    if isinstance(node.func, ast.Name):
        return aliases.get(node.func.id)

    return None


# ============================================================================
# AUDIT DATA
# ============================================================================

usage = {
    DOMAIN_LEXICAL_SOURCE: {
        "imports": [],
        "constructors": [],
        "annotations": [],
        "references": [],
        "attribute_access": [],
        "functions": [],
    },

    MODEL_LEXICAL_SOURCE: {
        "imports": [],
        "constructors": [],
        "annotations": [],
        "references": [],
        "attribute_access": [],
        "functions": [],
    },
}


# ============================================================================
# SCAN PRODUCTION FILES
# ============================================================================

for path in sorted(ROOT.rglob("*.py")):

    if not is_production_python(path):
        continue

    try:
        source = path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(
            source,
            filename=str(path),
        )

    except Exception:
        continue

    current_module = module_name(path)

    aliases = imported_lexical_sources(
        tree,
        current_module,
    )

    if not aliases:
        continue

    # ------------------------------------------------------------------------
    # Imports
    # ------------------------------------------------------------------------

    for local_name, target in aliases.items():

        usage[target]["imports"].append(
            (
                current_module,
                local_name,
            )
        )

    # ------------------------------------------------------------------------
    # AST scan
    # ------------------------------------------------------------------------

    for node in ast.walk(tree):

        # --------------------------------------------------------------------
        # Constructor calls
        # --------------------------------------------------------------------

        if isinstance(node, ast.Call):

            target = call_is_target(
                node,
                aliases,
            )

            if target is not None:

                try:
                    text = ast.unparse(node)
                except Exception:
                    text = target[1]

                usage[target]["constructors"].append(
                    (
                        current_module,
                        node.lineno,
                        text,
                    )
                )

        # --------------------------------------------------------------------
        # Variable annotations
        # --------------------------------------------------------------------

        if isinstance(node, ast.AnnAssign):

            for target in expression_contains_alias(
                node.annotation,
                aliases,
            ):

                usage[target]["annotations"].append(
                    (
                        current_module,
                        node.lineno,
                        annotation_text(node.annotation),
                    )
                )

        # --------------------------------------------------------------------
        # Function annotations
        # --------------------------------------------------------------------

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):

            annotations = []

            if node.returns is not None:
                annotations.append(
                    ("return", node.returns)
                )

            for arg in node.args.args:
                if arg.annotation is not None:
                    annotations.append(
                        (arg.arg, arg.annotation)
                    )

            for arg in node.args.kwonlyargs:
                if arg.annotation is not None:
                    annotations.append(
                        (arg.arg, arg.annotation)
                    )

            for label, annotation in annotations:

                for target in expression_contains_alias(
                    annotation,
                    aliases,
                ):

                    usage[target]["annotations"].append(
                        (
                            current_module,
                            node.lineno,
                            f"{label}: "
                            f"{annotation_text(annotation)}",
                        )
                    )

        # --------------------------------------------------------------------
        # Name references
        # --------------------------------------------------------------------

        if isinstance(node, ast.Name):

            target = aliases.get(node.id)

            if target is not None:

                usage[target]["references"].append(
                    (
                        current_module,
                        node.lineno,
                        node.id,
                    )
                )

        # --------------------------------------------------------------------
        # Attribute access
        # --------------------------------------------------------------------

        if isinstance(node, ast.Attribute):

            if isinstance(node.value, ast.Name):

                target = aliases.get(
                    node.value.id
                )

                if target is not None:

                    usage[target]["attribute_access"].append(
                        (
                            current_module,
                            node.lineno,
                            node.attr,
                        )
                    )

        # --------------------------------------------------------------------
        # Function / method ownership
        # --------------------------------------------------------------------

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):

            for child in ast.walk(node):

                if isinstance(child, ast.Name):

                    target = aliases.get(
                        child.id
                    )

                    if target is not None:

                        usage[target]["functions"].append(
                            (
                                current_module,
                                node.lineno,
                                node.name,
                            )
                        )


# ============================================================================
# DEDUPLICATION
# ============================================================================

def unique(items):
    seen = set()
    result = []

    for item in items:

        if item in seen:
            continue

        seen.add(item)
        result.append(item)

    return result


for target in TARGETS:

    for category in usage[target]:

        usage[target][category] = unique(
            usage[target][category]
        )


# ============================================================================
# OUTPUT
# ============================================================================

print("=" * 80)
print("SANSKRITAI — LEXICALSOURCE CONSUMER / OWNERSHIP AUDIT")
print("=" * 80)

print()
print("This audit compares the TWO active LexicalSource implementations.")
print()
print("Target A:")
print(
    "  domain.lexical.lexical_source.LexicalSource"
)
print()
print("Target B:")
print(
    "  lexical.models.lexical_source.LexicalSource"
)

# ============================================================================
# PER IMPLEMENTATION
# ============================================================================

for target in (
    DOMAIN_LEXICAL_SOURCE,
    MODEL_LEXICAL_SOURCE,
):

    data = usage[target]

    print()
    print("-" * 80)
    print(
        f"{target[0]}.{target[1]}"
    )
    print("-" * 80)

    print()
    print("IMPORTING MODULES")

    importing_modules = sorted(
        {
            module
            for module, _ in data["imports"]
        }
    )

    if importing_modules:
        for module in importing_modules:
            print(f"  - {module}")
    else:
        print("  (none)")

    print()
    print("CONSTRUCTOR CALLS")

    if data["constructors"]:
        for module, line, text in data["constructors"]:
            print(
                f"  {module}:{line}"
            )
            print(
                f"    {text}"
            )
    else:
        print("  (none)")

    print()
    print("TYPE ANNOTATIONS")

    if data["annotations"]:
        for module, line, text in data["annotations"]:
            print(
                f"  {module}:{line} : {text}"
            )
    else:
        print("  (none)")

    print()
    print("CLASS REFERENCES")

    if data["references"]:
        for module, line, text in data["references"]:
            print(
                f"  {module}:{line} : {text}"
            )
    else:
        print("  (none)")

    print()
    print("ATTRIBUTE ACCESS")

    if data["attribute_access"]:
        attributes = sorted(
            {
                attr
                for _, _, attr
                in data["attribute_access"]
            }
        )

        print(
            "  "
            + ", ".join(attributes)
        )
    else:
        print("  (none)")

    print()
    print("FUNCTIONS / METHODS USING SOURCE")

    functions = sorted(
        {
            f"{module}:{line} -> {name}"
            for module, line, name
            in data["functions"]
        }
    )

    if functions:
        for item in functions:
            print(f"  - {item}")
    else:
        print("  (none)")

    print()
    print("COUNTS")

    print(
        f"  importing modules : "
        f"{len(importing_modules)}"
    )

    print(
        f"  constructors      : "
        f"{len(data['constructors'])}"
    )

    print(
        f"  annotations       : "
        f"{len(data['annotations'])}"
    )

    print(
        f"  references        : "
        f"{len(data['references'])}"
    )


# ============================================================================
# SIDE-BY-SIDE CONSUMER COMPARISON
# ============================================================================

domain_modules = {
    module
    for module, _
    in usage[DOMAIN_LEXICAL_SOURCE]["imports"]
}

model_modules = {
    module
    for module, _
    in usage[MODEL_LEXICAL_SOURCE]["imports"]
}

shared_modules = domain_modules & model_modules

domain_only = domain_modules - model_modules
model_only = model_modules - domain_modules


print()
print("=" * 80)
print("CONSUMER SET COMPARISON")
print("=" * 80)

print()
print("SHARED CONSUMERS")

if shared_modules:
    for module in sorted(shared_modules):
        print(f"  - {module}")
else:
    print("  (none)")


print()
print("DOMAIN-ONLY CONSUMERS")

if domain_only:
    for module in sorted(domain_only):
        print(f"  - {module}")
else:
    print("  (none)")


print()
print("LEXICAL-MODEL-ONLY CONSUMERS")

if model_only:
    for module in sorted(model_only):
        print(f"  - {module}")
else:
    print("  (none)")


# ============================================================================
# ARCHITECTURAL INTERPRETATION
# ============================================================================

print()
print("=" * 80)
print("ARCHITECTURAL INTERPRETATION")
print("=" * 80)

print()
print("The audit is intentionally evidence-only.")

print()
print("Questions this audit is designed to answer:")

print(
    "  1. Are both LexicalSource implementations actively consumed?"
)

print(
    "  2. Which production modules depend on each implementation?"
)

print(
    "  3. Are the consumers concentrated in different architectural layers?"
)

print(
    "  4. Are there shared consumers that would make consolidation risky?"
)

print(
    "  5. Are either implementations actually constructed directly?"
)

print()
print("No production files are modified by this audit.")


# ============================================================================
# FILTER SUMMARY
# ============================================================================

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
