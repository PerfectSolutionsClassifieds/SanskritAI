
from __future__ import annotations

"""
BATCH 5E — AMARAKOSHA BUILDER FRAMEWORK CONTRACT AUDIT

Purpose
-------
Determine the existing BaseBuilder / NodeBuilder / ContainerNode
construction semantics before making any Amarakosha builder/model repair.

IMPORTANT
---------
READ-ONLY AUDIT.

This script does NOT:
- modify production code
- create new abstractions
- repair builders
- repair Synset/Varga
- implement an Amarakosha canonical adapter

Production-file filter:
- tests excluded
- __pycache__ excluded
- numeric historical suffixes excluded
- _G<number>.py files excluded
"""

from pathlib import Path
import ast
import importlib
import inspect
import re
import sys
import traceback


# ======================================================================
# Repository bootstrap
# ======================================================================

REPO_ROOT = Path("/content/SanskritAI")

if str(REPO_ROOT.parent) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT.parent))

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

print("=" * 118)
print("BATCH 5E — AMARAKOSHA BUILDER FRAMEWORK CONTRACT AUDIT")
print("=" * 118)
print(f"Repository root : {REPO_ROOT}")
print("Audit mode      : READ-ONLY")
print("Purpose         : determine existing BaseBuilder / NodeBuilder /")
print("                  ContainerNode construction semantics before repair")
print()
print("Production-file filter:")
print("  tests excluded")
print("  __pycache__ excluded")
print("  numeric historical suffixes excluded")
print("  _G<number> files excluded")
print()


# ======================================================================
# Production-file filtering
# ======================================================================

NUMERIC_SUFFIX_RE = re.compile(r"\d+\.py$")
GEN_SUFFIX_RE = re.compile(r"_G\d+\.py$", re.IGNORECASE)


def is_production_python_file(path: Path) -> bool:
    """
    Return True only for active production Python files.

    Historical/generated variants are deliberately excluded.
    """
    parts_lower = {part.lower() for part in path.parts}

    if "tests" in parts_lower:
        return False

    if "__pycache__" in parts_lower:
        return False

    if not path.name.endswith(".py"):
        return False

    if NUMERIC_SUFFIX_RE.search(path.name):
        return False

    if GEN_SUFFIX_RE.search(path.name):
        return False

    return True


# ======================================================================
# Module discovery
# ======================================================================

def module_name_from_path(path: Path) -> str | None:
    try:
        relative = path.relative_to(REPO_ROOT)
    except ValueError:
        return None

    if relative.name == "__init__.py":
        parts = list(relative.parts[:-1])
    else:
        parts = list(relative.with_suffix("").parts)

    if not parts:
        return None

    return ".".join(["SanskritAI", *parts])


def discover_modules_containing_symbol(symbol: str) -> list[str]:
    """
    Discover production modules whose source defines the requested symbol.

    This avoids assuming an architecture path such as:
        SanskritAI.core.builders.base_builder
    when the actual repository may own the symbol elsewhere.
    """
    results: list[str] = []

    if not REPO_ROOT.exists():
        return results

    for path in REPO_ROOT.rglob("*.py"):
        if not is_production_python_file(path):
            continue

        try:
            source = path.read_text(encoding="utf-8")
        except Exception:
            continue

        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError:
            continue

        found = False

        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == symbol:
                    found = True
                    break

        if found:
            module_name = module_name_from_path(path)
            if module_name:
                results.append(module_name)

    return sorted(set(results))


def import_first_working(module_names: list[str], symbol: str):
    """
    Import the first module that successfully exposes symbol.
    """
    failures: list[tuple[str, str]] = []

    for module_name in module_names:
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            failures.append(
                (
                    module_name,
                    f"{type(exc).__name__}: {exc}",
                )
            )
            continue

        if hasattr(module, symbol):
            return module, getattr(module, symbol), failures

        failures.append(
            (
                module_name,
                f"Imported successfully but symbol {symbol!r} not exposed",
            )
        )

    return None, None, failures


# ======================================================================
# Initial symbol discovery
# ======================================================================

print("-" * 118)
print("1. FRAMEWORK SYMBOL DISCOVERY")
print("-" * 118)

symbols_to_discover = [
    "BaseBuilder",
    "ValidatedBuilder",
    "RecordBuilder",
    "NodeBuilder",
    "BaseNode",
    "ContainerNode",
]

discovered: dict[str, list[str]] = {}

for symbol in symbols_to_discover:
    modules = discover_modules_containing_symbol(symbol)
    discovered[symbol] = modules

    print(f"\n{symbol}")
    if modules:
        for module_name in modules:
            print(f"  {module_name}")
    else:
        print("  NOT FOUND")


# ======================================================================
# Import framework symbols
# ======================================================================

print()
print("-" * 118)
print("2. FRAMEWORK IMPORT RESOLUTION")
print("-" * 118)

resolved: dict[str, tuple[object, type] | None] = {}

for symbol in symbols_to_discover:
    module, obj, failures = import_first_working(
        discovered.get(symbol, []),
        symbol,
    )

    if module is not None and obj is not None:
        resolved[symbol] = (module, obj)

        print(
            f"{symbol:22s} -> "
            f"{module.__name__}.{getattr(obj, '__name__', symbol)}"
        )
    else:
        resolved[symbol] = None

        print(f"{symbol:22s} -> NOT RESOLVED")

        for module_name, error in failures[:5]:
            print(f"  {module_name}: {error}")


# ======================================================================
# Helper inspection functions
# ======================================================================

def print_signature(label: str, obj) -> None:
    try:
        print(f"{label}: {inspect.signature(obj)}")
    except Exception as exc:
        print(f"{label}: <signature unavailable: {exc}>")


def print_source(label: str, obj, max_lines: int = 120) -> None:
    print(f"\n{label}")

    try:
        source = inspect.getsource(obj)
    except Exception as exc:
        print(f"  <source unavailable: {exc}>")
        return

    lines = source.splitlines()

    for line in lines[:max_lines]:
        print(f"  {line}")

    if len(lines) > max_lines:
        print(f"  ... ({len(lines) - max_lines} additional lines omitted)")


def print_mro(label: str, cls) -> None:
    print(f"\n{label}")

    try:
        for item in cls.__mro__:
            print(f"  {item.__module__}.{item.__name__}")
    except Exception as exc:
        print(f"  <MRO unavailable: {exc}>")


def print_abstracts(label: str, cls) -> None:
    print(f"\n{label}")

    try:
        print(f"  __abstractmethods__ = {sorted(cls.__abstractmethods__)}")
    except Exception as exc:
        print(f"  <abstract-method information unavailable: {exc}>")


# ======================================================================
# Framework class inspection
# ======================================================================

print()
print("-" * 118)
print("3. FRAMEWORK CLASS SEMANTICS")
print("-" * 118)

for symbol in symbols_to_discover:
    entry = resolved.get(symbol)

    if not entry:
        continue

    module, cls = entry

    print()
    print(f"[{symbol}]")
    print(f"module       : {module.__name__}")
    print(f"class        : {cls}")
    print_signature("constructor", cls)
    print_mro("MRO", cls)
    print_abstracts("Abstract contract", cls)

    for method_name in (
        "__init__",
        "build",
        "_create_instance",
        "validate",
    ):
        if hasattr(cls, method_name):
            method = getattr(cls, method_name)

            try:
                print_signature(f"{method_name}", method)
            except Exception:
                pass


# ======================================================================
# Amarakosha imports
# ======================================================================

print()
print("-" * 118)
print("4. AMARAKOSHA BUILDER / MODEL IMPORTS")
print("-" * 118)

amarakosha_targets = [
    ("BaseAmarakoshaBuilder", "SanskritAI.amarakosha.builders.base_amarakosha_builder"),
    ("SynsetBuilder", "SanskritAI.amarakosha.builders.synset_builder"),
    ("VargaBuilder", "SanskritAI.amarakosha.builders.varga_builder"),
    ("SynsetRecordBuilder", "SanskritAI.amarakosha.builders.synset_record_builder"),
    ("Synset", "SanskritAI.amarakosha.models.synset"),
    ("Varga", "SanskritAI.amarakosha.models.varga"),
    ("SynsetRecord", "SanskritAI.amarakosha.records.synset_record"),
    ("VargaRecord", "SanskritAI.amarakosha.records.varga_record"),
    ("AmarakoshaRegistry", "SanskritAI.amarakosha.registries.amarakosha_registry"),
]


amarakosha: dict[str, object] = {}

for symbol, module_name in amarakosha_targets:
    try:
        module = importlib.import_module(module_name)

        if not hasattr(module, symbol):
            print(
                f"{symbol:24s} -> IMPORTED MODULE BUT SYMBOL NOT FOUND "
                f"({module_name})"
            )
            continue

        obj = getattr(module, symbol)
        amarakosha[symbol] = obj

        print(
            f"{symbol:24s} -> "
            f"{module_name}.{symbol}"
        )

    except Exception as exc:
        print(
            f"{symbol:24s} -> "
            f"IMPORT FAILURE: {type(exc).__name__}: {exc}"
        )


# ======================================================================
# Amarakosha builder inspection
# ======================================================================

print()
print("-" * 118)
print("5. AMARAKOSHA BUILDER CONTRACT")
print("-" * 118)

for symbol in (
    "BaseAmarakoshaBuilder",
    "SynsetBuilder",
    "VargaBuilder",
    "SynsetRecordBuilder",
):
    cls = amarakosha.get(symbol)

    if cls is None:
        continue

    print()
    print(f"[{symbol}]")
    print_mro("MRO", cls)
    print_abstracts("Abstract methods", cls)
    print_signature("Constructor", cls)

    for method_name in (
        "__init__",
        "build",
        "_create_instance",
        "identifier",
        "metadata",
        "add_lexeme",
        "add_synset",
    ):
        if hasattr(cls, method_name):
            method = getattr(cls, method_name)
            print_signature(method_name, method)

    print_source(f"{symbol} source", cls, max_lines=180)


# ======================================================================
# Amarakosha model inspection
# ======================================================================

print()
print("-" * 118)
print("6. SYNSET / VARGA MODEL CONSTRUCTION CONTRACT")
print("-" * 118)

for symbol in (
    "Synset",
    "Varga",
):
    cls = amarakosha.get(symbol)

    if cls is None:
        continue

    print()
    print(f"[{symbol}]")
    print_signature("Constructor", cls)
    print_mro("MRO", cls)
    print_abstracts("Abstract methods", cls)

    print_source(f"{symbol} source", cls, max_lines=180)


# ======================================================================
# ContainerNode constructor semantics
# ======================================================================

print()
print("-" * 118)
print("7. CONTAINERNODE CONSTRUCTION SEMANTICS")
print("-" * 118)

container_entry = resolved.get("ContainerNode")

if container_entry:
    container_module, ContainerNode = container_entry

    print(f"ContainerNode owner : {container_module.__name__}")
    print_signature("ContainerNode", ContainerNode)
    print_mro("ContainerNode MRO", ContainerNode)
    print_abstracts("ContainerNode abstract contract", ContainerNode)

    print_source(
        "ContainerNode source",
        ContainerNode,
        max_lines=220,
    )
else:
    print("ContainerNode could not be resolved.")


# ======================================================================
# BaseNode constructor semantics
# ======================================================================

print()
print("-" * 118)
print("8. BASENODE CONSTRUCTION SEMANTICS")
print("-" * 118)

base_node_entry = resolved.get("BaseNode")

if base_node_entry:
    base_node_module, BaseNode = base_node_entry

    print(f"BaseNode owner : {base_node_module.__name__}")
    print_signature("BaseNode", BaseNode)
    print_mro("BaseNode MRO", BaseNode)
    print_abstracts("BaseNode abstract contract", BaseNode)

    print_source(
        "BaseNode source",
        BaseNode,
        max_lines=220,
    )
else:
    print("BaseNode could not be resolved.")


# ======================================================================
# Runtime builder instantiation probes
# ======================================================================

print()
print("-" * 118)
print("9. RUNTIME BUILDER INSTANTIATION PROBES")
print("-" * 118)

for symbol in (
    "BaseAmarakoshaBuilder",
    "SynsetBuilder",
    "VargaBuilder",
    "SynsetRecordBuilder",
):
    cls = amarakosha.get(symbol)

    if cls is None:
        continue

    print(f"\n{symbol}")

    try:
        instance = cls()
        print("  instantiation : SUCCESS")
        print(f"  instance      : {instance!r}")

    except Exception as exc:
        print(
            f"  instantiation : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


# ======================================================================
# Runtime model construction probes
# ======================================================================

print()
print("-" * 118)
print("10. RUNTIME SYNSET / VARGA CONSTRUCTION PROBES")
print("-" * 118)

synset_cls = amarakosha.get("Synset")
varga_cls = amarakosha.get("Varga")

synset_metadata_cls = None
varga_metadata_cls = None

try:
    metadata_module = importlib.import_module(
        "SanskritAI.amarakosha.models.synset_metadata"
    )
    synset_metadata_cls = getattr(
        metadata_module,
        "SynsetMetadata",
        None,
    )
except Exception:
    pass

try:
    metadata_module = importlib.import_module(
        "SanskritAI.amarakosha.models.varga_metadata"
    )
    varga_metadata_cls = getattr(
        metadata_module,
        "VargaMetadata",
        None,
    )
except Exception:
    pass


if synset_cls is not None:
    print("\nSynset")

    try:
        metadata = (
            synset_metadata_cls()
            if synset_metadata_cls is not None
            else None
        )

        print(
            "  metadata type :",
            type(metadata).__name__ if metadata is not None else "None",
        )

        instance = synset_cls(
            identifier="batch5e-probe-synset",
            metadata=metadata,
            children=[],
        )

        print("  children=[]   : SUCCESS")
        print(f"  instance      : {instance!r}")

    except Exception as exc:
        print(
            f"  children=[]   : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


if varga_cls is not None:
    print("\nVarga")

    try:
        metadata = (
            varga_metadata_cls()
            if varga_metadata_cls is not None
            else None
        )

        print(
            "  metadata type :",
            type(metadata).__name__ if metadata is not None else "None",
        )

        instance = varga_cls(
            identifier="batch5e-probe-varga",
            metadata=metadata,
            children=[],
        )

        print("  children=[]   : SUCCESS")
        print(f"  instance      : {instance!r}")

    except Exception as exc:
        print(
            f"  children=[]   : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


# ======================================================================
# Production ContainerNode subclass discovery
# ======================================================================

print()
print("-" * 118)
print("11. ACTIVE PRODUCTION CONTAINERNODE SUBCLASS DISCOVERY")
print("-" * 118)

container_subclasses: list[tuple[str, str]] = []

for path in REPO_ROOT.rglob("*.py"):
    if not is_production_python_file(path):
        continue

    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except Exception:
        continue

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        for base in node.bases:
            base_name = ""

            if isinstance(base, ast.Name):
                base_name = base.id

            elif isinstance(base, ast.Attribute):
                parts = []
                current = base

                while isinstance(current, ast.Attribute):
                    parts.append(current.attr)
                    current = current.value

                if isinstance(current, ast.Name):
                    parts.append(current.id)

                base_name = ".".join(reversed(parts))

            if base_name.endswith("ContainerNode") or base_name == "ContainerNode":
                module_name = module_name_from_path(path)

                if module_name:
                    container_subclasses.append(
                        (
                            module_name,
                            node.name,
                        )
                    )

                break


if container_subclasses:
    for module_name, class_name in sorted(set(container_subclasses)):
        print(f"  {module_name}.{class_name}")
else:
    print("  No direct ContainerNode subclasses discovered by AST scan.")


# ======================================================================
# Production BaseBuilder subclass discovery
# ======================================================================

print()
print("-" * 118)
print("12. ACTIVE PRODUCTION BASEBUILDER SUBCLASS DISCOVERY")
print("-" * 118)

builder_subclasses: list[tuple[str, str]] = []

for path in REPO_ROOT.rglob("*.py"):
    if not is_production_python_file(path):
        continue

    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except Exception:
        continue

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        for base in node.bases:
            base_name = ""

            if isinstance(base, ast.Name):
                base_name = base.id

            elif isinstance(base, ast.Attribute):
                parts = []
                current = base

                while isinstance(current, ast.Attribute):
                    parts.append(current.attr)
                    current = current.value

                if isinstance(current, ast.Name):
                    parts.append(current.id)

                base_name = ".".join(reversed(parts))

            if (
                base_name.endswith("BaseBuilder")
                or base_name in {
                    "BaseBuilder",
                    "NodeBuilder",
                    "RecordBuilder",
                }
            ):
                module_name = module_name_from_path(path)

                if module_name:
                    builder_subclasses.append(
                        (
                            module_name,
                            node.name,
                        )
                    )

                break


if builder_subclasses:
    for module_name, class_name in sorted(set(builder_subclasses)):
        print(f"  {module_name}.{class_name}")
else:
    print("  No direct BaseBuilder/NodeBuilder/RecordBuilder subclasses discovered.")


# ======================================================================
# Construction-method source comparison
# ======================================================================

print()
print("-" * 118)
print("13. BUILDER CONSTRUCTION METHOD COMPARISON")
print("-" * 118)

for symbol in (
    "SynsetBuilder",
    "VargaBuilder",
    "SynsetRecordBuilder",
):
    cls = amarakosha.get(symbol)

    if cls is None:
        continue

    print()
    print(f"[{symbol}]")

    for method_name in (
        "build",
        "_create_instance",
    ):
        if hasattr(cls, method_name):
            method = getattr(cls, method_name)

            try:
                source = inspect.getsource(method)

                print(f"\n  {method_name}:")
                for line in source.splitlines():
                    print(f"    {line}")

            except Exception as exc:
                print(
                    f"  {method_name}: "
                    f"<source unavailable: {exc}>"
                )


# ======================================================================
# Final architectural decision gate
# ======================================================================

print()
print("=" * 118)
print("BATCH 5E — DECISION GATE")
print("=" * 118)

base_builder_found = resolved.get("BaseBuilder") is not None
node_builder_found = resolved.get("NodeBuilder") is not None
container_node_found = resolved.get("ContainerNode") is not None

synset_builder = amarakosha.get("SynsetBuilder")
varga_builder = amarakosha.get("VargaBuilder")

synset_abstract = (
    bool(synset_builder is not None)
    and bool(getattr(synset_builder, "__abstractmethods__", set()))
)

varga_abstract = (
    bool(varga_builder is not None)
    and bool(getattr(varga_builder, "__abstractmethods__", set()))
)

print()
print(f"BaseBuilder discovered       : {base_builder_found}")
print(f"NodeBuilder discovered       : {node_builder_found}")
print(f"ContainerNode discovered     : {container_node_found}")
print(f"SynsetBuilder abstract       : {synset_abstract}")
print(f"VargaBuilder abstract        : {varga_abstract}")

print()
print("ARCHITECTURAL INTERPRETATION")
print("-----------------------------")

if not base_builder_found:
    print(
        "CASE A — BaseBuilder ownership is not yet resolved."
    )
    print(
        "Do NOT create SanskritAI.core.builders.base_builder."
    )
    print(
        "The repository must first establish the actual BaseBuilder owner."
    )

elif not node_builder_found or not container_node_found:
    print(
        "CASE B — Builder/node framework is only partially discoverable."
    )
    print(
        "Do NOT repair Amarakosha builders yet."
    )

elif synset_abstract or varga_abstract:
    print(
        "CASE C — Amarakosha builders remain abstract under the existing framework."
    )
    print(
        "The next step is to compare concrete production subclasses and determine"
    )
    print(
        "whether _create_instance() is intentionally required or whether the"
    )
    print(
        "Amarakosha builders are following an existing alternate build contract."
    )

else:
    print(
        "CASE D — Builder classes are concrete under the discovered framework."
    )
    print(
        "Proceed to the Synset/Varga model compatibility decision."
    )

print()
print("CANONICAL ADAPTER STATUS")
print("------------------------")
print("BLOCKED")
print()
print(
    "Reason: Batch 5E is a framework-contract audit only. "
    "No Amarakosha canonical adapter should be implemented until"
)
print(
    "the existing builder/model construction semantics are understood "
    "and the Synset/Varga compatibility boundary is resolved."
)

print()
print("=" * 118)
print("BATCH 5E COMPLETE — READ-ONLY AUDIT")
print("=" * 118)
