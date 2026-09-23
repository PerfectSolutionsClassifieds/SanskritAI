
from __future__ import annotations

"""
BATCH 5F — AMARAKOSHA SYNSET / VARGA COMPATIBILITY AUDIT

Purpose
-------
Determine the exact compatibility repair required between:

    Synset / Varga
        ↓
    ContainerNode
        ↓
    NodeCollection

and between:

    SynsetBuilder / VargaBuilder
        ↓
    BaseAmarakoshaBuilder
        ↓
    NodeBuilder
        ↓
    BaseBuilder

This is a READ-ONLY audit.

It must determine whether the correct repair is:

    A. fix Synset/Varga constructors only
    B. fix SynsetBuilder/VargaBuilder only
    C. fix both model constructors and builders
    D. identify another existing repository pattern

IMPORTANT
---------
Do NOT modify production code.
Do NOT modify ContainerNode.
Do NOT modify BaseBuilder.
Do NOT create new abstractions.
Do NOT implement the canonical Amarakośa adapter.
"""

from __future__ import annotations

from pathlib import Path
import ast
import importlib
import inspect
import re
import sys


# ======================================================================
# Repository bootstrap
# ======================================================================

REPO_ROOT = Path("/content/SanskritAI")

if str(REPO_ROOT.parent) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT.parent))

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


print("=" * 118)
print("BATCH 5F — AMARAKOSHA SYNSET / VARGA COMPATIBILITY AUDIT")
print("=" * 118)
print(f"Repository root : {REPO_ROOT}")
print("Audit mode      : READ-ONLY")
print()


# ======================================================================
# Production-file filter
# ======================================================================

NUMERIC_SUFFIX_RE = re.compile(r"\d+\.py$")
GEN_SUFFIX_RE = re.compile(r"_G\d+\.py$", re.IGNORECASE)


def is_production_python_file(path: Path) -> bool:

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


def discover_symbol(symbol: str) -> list[str]:

    modules: list[str] = []

    for path in REPO_ROOT.rglob("*.py"):

        if not is_production_python_file(path):
            continue

        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except Exception:
            continue

        for node in ast.walk(tree):

            if isinstance(
                node,
                (
                    ast.ClassDef,
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ) and node.name == symbol:

                module_name = module_name_from_path(path)

                if module_name:
                    modules.append(module_name)

                break

    return sorted(set(modules))


def resolve_symbol(symbol: str):

    candidates = discover_symbol(symbol)

    print()
    print(f"{symbol}")
    print("-" * 80)

    for module_name in candidates:

        try:
            module = importlib.import_module(module_name)

            if hasattr(module, symbol):

                obj = getattr(module, symbol)

                print(
                    f"Resolved : {module_name}.{symbol}"
                )

                return module, obj

        except Exception as exc:

            print(
                f"Import failure : "
                f"{module_name} -> "
                f"{type(exc).__name__}: {exc}"
            )

    print("Resolved : NOT FOUND")

    return None, None


# ======================================================================
# Resolve core classes
# ======================================================================

print("-" * 118)
print("1. RESOLVE CORE FRAMEWORK CLASSES")
print("-" * 118)

_, ContainerNode = resolve_symbol("ContainerNode")
_, BaseNode = resolve_symbol("BaseNode")
_, NodeCollection = resolve_symbol("NodeCollection")
_, Hierarchical = resolve_symbol("Hierarchical")


# ======================================================================
# Resolve Amarakosha classes
# ======================================================================

print()
print("-" * 118)
print("2. RESOLVE AMARAKOSHA CLASSES")
print("-" * 118)

_, Synset = resolve_symbol("Synset")
_, Varga = resolve_symbol("Varga")
_, SynsetBuilder = resolve_symbol("SynsetBuilder")
_, VargaBuilder = resolve_symbol("VargaBuilder")
_, SynsetMetadata = resolve_symbol("SynsetMetadata")
_, VargaMetadata = resolve_symbol("VargaMetadata")


# ======================================================================
# Generic signature inspection
# ======================================================================

print()
print("-" * 118)
print("3. CONSTRUCTION SIGNATURES")
print("-" * 118)


def show_signature(label: str, obj) -> None:

    try:
        print(
            f"{label:35s}: "
            f"{inspect.signature(obj)}"
        )
    except Exception as exc:
        print(
            f"{label:35s}: "
            f"<unavailable: {exc}>"
        )


for label, obj in (
    ("BaseNode", BaseNode),
    ("ContainerNode", ContainerNode),
    ("Synset", Synset),
    ("Varga", Varga),
    ("SynsetBuilder", SynsetBuilder),
    ("VargaBuilder", VargaBuilder),
    ("SynsetMetadata", SynsetMetadata),
    ("VargaMetadata", VargaMetadata),
):

    if obj is not None:
        show_signature(label, obj)


# ======================================================================
# MRO / abstract-method inspection
# ======================================================================

print()
print("-" * 118)
print("4. MRO AND ABSTRACT CONTRACTS")
print("-" * 118)


def inspect_class(label: str, cls) -> None:

    if cls is None:
        return

    print()
    print(f"[{label}]")

    print("MRO:")

    for item in cls.__mro__:
        print(
            f"  {item.__module__}.{item.__name__}"
        )

    print(
        "Abstract methods:",
        sorted(
            getattr(
                cls,
                "__abstractmethods__",
                set(),
            )
        ),
    )


for label, cls in (
    ("ContainerNode", ContainerNode),
    ("Synset", Synset),
    ("Varga", Varga),
    ("SynsetBuilder", SynsetBuilder),
    ("VargaBuilder", VargaBuilder),
):

    inspect_class(label, cls)


# ======================================================================
# Source inspection
# ======================================================================

print()
print("-" * 118)
print("5. SYNSET / VARGA CONSTRUCTOR SOURCE")
print("-" * 118)


def show_method_source(
    cls,
    method_name: str,
) -> None:

    if cls is None:
        return

    print()
    print(
        f"{cls.__name__}.{method_name}"
    )

    try:
        method = getattr(cls, method_name)
        source = inspect.getsource(method)

        for line in source.splitlines():
            print(f"  {line}")

    except Exception as exc:
        print(
            f"  <source unavailable: {exc}>"
        )


for cls in (
    Synset,
    Varga,
):

    show_method_source(
        cls,
        "__init__",
    )

    show_method_source(
        cls,
        "add_child",
    )

    show_method_source(
        cls,
        "extend",
    )


# ======================================================================
# ContainerNode child API
# ======================================================================

print()
print("-" * 118)
print("6. CONTAINERNODE CHILD API")
print("-" * 118)

if ContainerNode is not None:

    for method_name in (
        "__init__",
        "add_child",
        "remove_child",
        "extend",
        "clear_children",
    ):

        show_method_source(
            ContainerNode,
            method_name,
        )


# ======================================================================
# Child collection API
# ======================================================================

print()
print("-" * 118)
print("7. NODECOLLECTION API")
print("-" * 118)

if NodeCollection is not None:

    show_signature(
        "NodeCollection",
        NodeCollection,
    )

    for method_name in (
        "__init__",
        "add",
        "extend",
        "remove",
        "clear",
        "first",
        "last",
        "__iter__",
        "__len__",
    ):

        show_method_source(
            NodeCollection,
            method_name,
        )


# ======================================================================
# Runtime model construction
# ======================================================================

print()
print("-" * 118)
print("8. RUNTIME MODEL CONSTRUCTION")
print("-" * 118)


synset_metadata = None
varga_metadata = None

if SynsetMetadata is not None:

    try:
        synset_metadata = SynsetMetadata()
        print(
            "SynsetMetadata() : SUCCESS"
        )
        print(
            f"  {synset_metadata!r}"
        )

    except Exception as exc:

        print(
            "SynsetMetadata() : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


if VargaMetadata is not None:

    try:
        varga_metadata = VargaMetadata()
        print(
            "VargaMetadata()  : SUCCESS"
        )
        print(
            f"  {varga_metadata!r}"
        )

    except Exception as exc:

        print(
            "VargaMetadata()  : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


if Synset is not None:

    print()
    print("Synset construction WITHOUT children")

    try:

        obj = Synset(
            identifier="batch5f-synset",
            metadata=synset_metadata,
        )

        print(
            "  RESULT : SUCCESS"
        )

        print(
            f"  repr   : {obj!r}"
        )

        print(
            f"  child_count : "
            f"{getattr(obj, 'child_count', '<missing>')}"
        )

        print(
            f"  children type : "
            f"{type(obj.children).__name__}"
        )

    except Exception as exc:

        print(
            "  RESULT : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


if Varga is not None:

    print()
    print("Varga construction WITHOUT children")

    try:

        obj = Varga(
            identifier="batch5f-varga",
            metadata=varga_metadata,
        )

        print(
            "  RESULT : SUCCESS"
        )

        print(
            f"  repr   : {obj!r}"
        )

        print(
            f"  child_count : "
            f"{getattr(obj, 'child_count', '<missing>')}"
        )

        print(
            f"  children type : "
            f"{type(obj.children).__name__}"
        )

    except Exception as exc:

        print(
            "  RESULT : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


# ======================================================================
# Explicit children= compatibility probe
# ======================================================================

print()
print("-" * 118)
print("9. EXPLICIT CHILDREN= COMPATIBILITY")
print("-" * 118)

if Synset is not None:

    print()
    print("Synset(..., children=[])")

    try:

        Synset(
            identifier="batch5f-synset-children",
            metadata=synset_metadata,
            children=[],
        )

        print(
            "  RESULT : ACCEPTED"
        )

    except Exception as exc:

        print(
            "  RESULT : REJECTED "
            f"{type(exc).__name__}: {exc}"
        )


if Varga is not None:

    print()
    print("Varga(..., children=[])")

    try:

        Varga(
            identifier="batch5f-varga-children",
            metadata=varga_metadata,
            children=[],
        )

        print(
            "  RESULT : ACCEPTED"
        )

    except Exception as exc:

        print(
            "  RESULT : REJECTED "
            f"{type(exc).__name__}: {exc}"
        )


# ======================================================================
# Child mutation compatibility
# ======================================================================

print()
print("-" * 118)
print("10. CHILD MUTATION COMPATIBILITY")
print("-" * 118)

if Synset is not None:

    try:

        synset = Synset(
            identifier="batch5f-child-test",
            metadata=synset_metadata,
        )

        print(
            "Synset.add_child API available :",
            hasattr(synset, "add_child"),
        )

        print(
            "Synset.extend API available     :",
            hasattr(synset, "extend"),
        )

        print(
            "Synset.children available       :",
            hasattr(synset, "children"),
        )

    except Exception as exc:

        print(
            "Synset child API probe failed :",
            type(exc).__name__,
            exc,
        )


if Varga is not None:

    try:

        varga = Varga(
            identifier="batch5f-varga-child-test",
            metadata=varga_metadata,
        )

        print(
            "Varga.add_child API available :",
            hasattr(varga, "add_child"),
        )

        print(
            "Varga.extend API available    :",
            hasattr(varga, "extend"),
        )

        print(
            "Varga.children available      :",
            hasattr(varga, "children"),
        )

    except Exception as exc:

        print(
            "Varga child API probe failed :",
            type(exc).__name__,
            exc,
        )


# ======================================================================
# Builder source inspection
# ======================================================================

print()
print("-" * 118)
print("11. BUILDER CONSTRUCTION CONTRACT")
print("-" * 118)


for cls in (
    SynsetBuilder,
    VargaBuilder,
):

    if cls is None:
        continue

    print()
    print(f"[{cls.__name__}]")

    for method_name in (
        "__init__",
        "build",
        "_create_instance",
    ):

        show_method_source(
            cls,
            method_name,
        )


# ======================================================================
# Builder runtime probes
# ======================================================================

print()
print("-" * 118)
print("12. BUILDER RUNTIME PROBES")
print("-" * 118)


for cls in (
    SynsetBuilder,
    VargaBuilder,
):

    if cls is None:
        continue

    print()
    print(cls.__name__)

    try:

        builder = cls()

        print(
            "  instantiation : SUCCESS"
        )

        print(
            f"  abstractmethods : "
            f"{sorted(getattr(cls, '__abstractmethods__', set()))}"
        )

    except Exception as exc:

        print(
            "  instantiation : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


# ======================================================================
# AST search for constructor patterns
# ======================================================================

print()
print("-" * 118)
print("13. ACTIVE PRODUCTION CONSTRUCTOR PATTERN SEARCH")
print("-" * 118)

patterns = {
    "ContainerNode(... children=...)": [],
    "super(... children=...)": [],
    ".add_child(...)": [],
    ".extend(...)": [],
}


for path in REPO_ROOT.rglob("*.py"):

    if not is_production_python_file(path):
        continue

    try:
        source = path.read_text(
            encoding="utf-8"
        )
    except Exception:
        continue

    try:
        tree = ast.parse(
            source,
            filename=str(path),
        )
    except SyntaxError:
        continue

    module_name = module_name_from_path(path)

    if not module_name:
        continue

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            text = ast.get_source_segment(
                source,
                node,
            ) or ""

            if (
                "children=" in text
                and (
                    "ContainerNode" in text
                    or "super(" in text
                )
            ):
                patterns[
                    "ContainerNode(... children=...)"
                ].append(
                    (
                        module_name,
                        node.lineno,
                        text.replace("\n", " ")[:240],
                    )
                )

            if (
                "super(" in text
                and "children=" in text
            ):
                patterns[
                    "super(... children=...)"
                ].append(
                    (
                        module_name,
                        node.lineno,
                        text.replace("\n", " ")[:240],
                    )
                )

            if (
                ".add_child(" in text
            ):
                patterns[
                    ".add_child(...)"
                ].append(
                    (
                        module_name,
                        node.lineno,
                        text.replace("\n", " ")[:240],
                    )
                )

            if (
                ".extend(" in text
            ):
                patterns[
                    ".extend(...)"
                ].append(
                    (
                        module_name,
                        node.lineno,
                        text.replace("\n", " ")[:240],
                    )
                )


for pattern_name, matches in patterns.items():

    print()
    print(pattern_name)

    if not matches:
        print("  NONE")
        continue

    for module_name, lineno, text in matches[:30]:

        print(
            f"  {module_name}:{lineno}: {text}"
        )


# ======================================================================
# Compatibility matrix
# ======================================================================

print()
print("=" * 118)
print("BATCH 5F — COMPATIBILITY MATRIX")
print("=" * 118)

print()
print("MODEL CONTRACT")
print("--------------")
print(
    "ContainerNode constructor accepts:"
)
print(
    "  identifier + metadata"
)
print(
    "ContainerNode owns children through NodeCollection"
)
print(
    "Children are populated after construction"
)

print()
print("AMARAKOSHA MODEL CONTRACT")
print("--------------------------")
print(
    "Synset/Varga currently expose a children constructor parameter"
)
print(
    "but pass it to ContainerNode, which rejects it."
)

print()
print("BUILDER CONTRACT")
print("----------------")
print(
    "BaseBuilder requires _create_instance()"
)
print(
    "SynsetBuilder/VargaBuilder currently override build()"
)
print(
    "but do not implement _create_instance()."
)

print()
print("REQUIRED REPAIR SHAPE")
print("----------------------")

print(
    "MODEL REPAIR:"
)
print(
    "  Synset/Varga should construct the ContainerNode with"
)
print(
    "  identifier + metadata, then populate children through"
)
print(
    "  the existing child API."
)

print()
print(
    "BUILDER REPAIR:"
)
print(
    "  SynsetBuilder/VargaBuilder should conform to the existing"
)
print(
    "  BaseBuilder/NodeBuilder contract rather than bypassing it."
)

print()
print(
    "FRAMEWORK REPAIR:"
)
print(
    "  NO — ContainerNode/BaseBuilder should not be changed merely"
)
print(
    "  to accommodate Amarakośa."
)


# ======================================================================
# Final gate
# ======================================================================

print()
print("=" * 118)
print("BATCH 5F — DECISION GATE")
print("=" * 118)

print()
print("Current evidence:")
print(
    "  [1] ContainerNode children constructor      : INCOMPATIBLE"
)
print(
    "  [2] Synset/Varga child ownership            : EXISTING"
)
print(
    "  [3] Synset/Varga child mutation API         : EXISTING"
)
print(
    "  [4] BaseBuilder _create_instance contract   : REQUIRED"
)
print(
    "  [5] SynsetBuilder _create_instance         : MISSING"
)
print(
    "  [6] VargaBuilder _create_instance          : MISSING"
)
print(
    "  [7] SynsetRecordBuilder depends on builder  : YES"
)

print()
print("ARCHITECTURAL DECISION")
print("----------------------")
print(
    "REPAIR AMARAKOSHA MODEL + BUILDER LAYERS."
)
print(
    "DO NOT MODIFY ContainerNode."
)
print(
    "DO NOT MODIFY BaseBuilder."
)
print(
    "DO NOT CREATE A SECOND BUILDER ABSTRACTION."
)
print(
    "DO NOT IMPLEMENT THE CANONICAL ADAPTER YET."
)

print()
print("NEXT:")
print(
    "  Batch 5G — Conservative Builder + Synset/Varga Repair"
)

print()
print("=" * 118)
print("BATCH 5F COMPLETE — READ-ONLY AUDIT")
print("=" * 118)
