from __future__ import annotations

import ast
import re
from pathlib import Path
from collections import defaultdict


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
# Exact source-model identities
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
# Import resolution
# ---------------------------------------------------------------------------

def imported_targets(tree: ast.AST):
    """
    Return local aliases mapped to fully-qualified source-model identities.
    """

    aliases = {}

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue

            for alias in node.names:
                if alias.name == "*":
                    continue

                key = (node.module, alias.name)

                if key in TARGETS:
                    local_name = alias.asname or alias.name
                    aliases[local_name] = key

        elif isinstance(node, ast.Import):
            for alias in node.names:
                # Direct imports of target modules are uncommon, but keep
                # support for them.
                module = alias.name

                for target_module, target_class in TARGETS:
                    if module == target_module:
                        local_name = alias.asname or module.split(".")[-1]
                        aliases[local_name] = (
                            target_module,
                            target_class,
                        )

    return aliases


def target_from_expr(node, aliases):
    """
    Resolve Name / Attribute references where possible.
    """

    if isinstance(node, ast.Name):
        return aliases.get(node.id)

    return None


def annotation_contains_target(annotation, target_name):
    if annotation is None:
        return False

    try:
        text = ast.unparse(annotation)
    except Exception:
        return False

    return re.search(
        rf"\b{re.escape(target_name)}\b",
        text,
    ) is not None


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

usage = defaultdict(lambda: {
    "constructor": [],
    "annotation": [],
    "reference": [],
    "import": [],
})


for path in sorted(ROOT.rglob("*.py")):
    if not is_production_python(path):
        continue

    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except Exception:
        continue

    module = module_name(path)
    aliases = imported_targets(tree)

    if not aliases:
        continue

    # Imports
    for local_name, target in aliases.items():
        usage[target]["import"].append(
            (module, 0, local_name)
        )

    for node in ast.walk(tree):

        # ---------------------------------------------------------------
        # Constructor calls
        # ---------------------------------------------------------------
        if isinstance(node, ast.Call):
            target = target_from_expr(node.func, aliases)

            if target is not None:
                usage[target]["constructor"].append(
                    (
                        module,
                        node.lineno,
                        ast.unparse(node),
                    )
                )

        # ---------------------------------------------------------------
        # Type annotations
        # ---------------------------------------------------------------
        if isinstance(node, ast.AnnAssign):
            for local_name, target in aliases.items():
                if annotation_contains_target(
                    node.annotation,
                    local_name,
                ):
                    usage[target]["annotation"].append(
                        (
                            module,
                            node.lineno,
                            ast.unparse(node.annotation),
                        )
                    )

        elif isinstance(
            node,
            (
                ast.arg,
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            annotations = []

            if isinstance(node, ast.arg):
                annotations.append(node.annotation)

            else:
                annotations.append(node.returns)

                for arg in node.args.args:
                    annotations.append(arg.annotation)

                for arg in node.args.kwonlyargs:
                    annotations.append(arg.annotation)

            for annotation in annotations:
                for local_name, target in aliases.items():
                    if annotation_contains_target(
                        annotation,
                        local_name,
                    ):
                        usage[target]["annotation"].append(
                            (
                                module,
                                getattr(node, "lineno", 0),
                                ast.unparse(annotation),
                            )
                        )

        # ---------------------------------------------------------------
        # General references
        # ---------------------------------------------------------------
        if isinstance(node, ast.Name):
            target = aliases.get(node.id)

            if target is not None:
                usage[target]["reference"].append(
                    (
                        module,
                        node.lineno,
                        node.id,
                    )
                )


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

print("=" * 80)
print("SANSKRITAI — ACTIVE SOURCE MODEL CONSTRUCTION / TYPE USAGE AUDIT")
print("=" * 80)


for target_module, target_class in sorted(TARGETS):

    target = (target_module, target_class)
    data = usage[target]

    print()
    print("-" * 80)
    print(f"{target_class}")
    print(f"Canonical module: {target_module}")
    print("-" * 80)

    if data["constructor"]:
        print()
        print("CONSTRUCTOR CALLS")

        for module, line, text in data["constructor"]:
            print(f"  {module}:{line}")
            print(f"    {text}")
    else:
        print()
        print("CONSTRUCTOR CALLS")
        print("  (none)")

    if data["annotation"]:
        print()
        print("TYPE ANNOTATIONS")

        seen = set()

        for module, line, text in data["annotation"]:
            key = (module, line, text)

            if key in seen:
                continue

            seen.add(key)

            print(f"  {module}:{line} : {text}")
    else:
        print()
        print("TYPE ANNOTATIONS")
        print("  (none)")

    print()
    print("IMPORTS")

    seen = set()

    for module, line, local_name in data["import"]:
        key = (module, local_name)

        if key in seen:
            continue

        seen.add(key)

        print(
            f"  {module} -> {local_name}"
        )

    if not data["import"]:
        print("  (none)")

    print()
    print("ACTIVE COUNTS")
    print(
        f"  constructor calls : "
        f"{len(data['constructor'])}"
    )
    print(
        f"  type annotations  : "
        f"{len(data['annotation'])}"
    )
    print(
        f"  class references  : "
        f"{len(data['reference'])}"
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
