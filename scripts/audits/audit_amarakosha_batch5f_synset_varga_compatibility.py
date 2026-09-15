
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

It determines whether the correct repair is:

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
            source = path.read_text(
                encoding="utf-8"
            )

            tree = ast.parse(
                source,
                filename=str(path),
            )

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

            module = importlib.import_module(
                module_name
            )

            if hasattr(module, symbol):

                obj = getattr(
                    module,
                    symbol,
                )

                print(
                    f"Resolved : "
                    f"{module_name}.{symbol}"
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
# Resolve core framework classes
# ======================================================================

print("-" * 118)
print("1. RESOLVE CORE FRAMEWORK CLASSES")
print("-" * 118)

_, ContainerNode = resolve_symbol(
    "ContainerNode"
)

_, BaseNode = resolve_symbol(
    "BaseNode"
)

_, NodeCollection = resolve_symbol(
    "NodeCollection"
)

_, Hierarchical = resolve_symbol(
    "Hierarchical"
)


# ======================================================================
# Resolve Amarakosha classes
# ======================================================================

print()
print("-" * 118)
print("2. RESOLVE AMARAKOSHA CLASSES")
print("-" * 118)

_, Synset = resolve_symbol(
    "Synset"
)

_, Varga = resolve_symbol(
    "Varga"
)

_, SynsetBuilder = resolve_symbol(
    "SynsetBuilder"
)

_, VargaBuilder = resolve_symbol(
    "VargaBuilder"
)

_, SynsetMetadata = resolve_symbol(
    "SynsetMetadata"
)

_, VargaMetadata = resolve_symbol(
    "VargaMetadata"
)


# ======================================================================
# Generic signature inspection
# ======================================================================

print()
print("-" * 118)
print("3. CONSTRUCTION SIGNATURES")
print("-" * 118)


def show_signature(
    label: str,
    obj,
) -> None:

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
        show_signature(
            label,
            obj,
        )


# ======================================================================
# MRO / abstract-method inspection
# ======================================================================

print()
print("-" * 118)
print("4. MRO AND ABSTRACT CONTRACTS")
print("-" * 118)


def inspect_class(
    label: str,
    cls,
) -> None:

    if cls is None:
        return

    print()
    print(f"[{label}]")

    print("MRO:")

    for item in cls.__mro__:

        print(
            f"  {item.__module__}."
            f"{item.__name__}"
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

    inspect_class(
        label,
        cls,
    )


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

        method = getattr(
            cls,
            method_name,
        )

        source = inspect.getsource(
            method
        )

        for line in source.splitlines():
            print(
                f"  {line}"
            )

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
# Runtime metadata construction
# ======================================================================

print()
print("-" * 118)
print("8. RUNTIME METADATA CONSTRUCTION")
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


# ======================================================================
# Runtime model construction without children
# ======================================================================

print()
print("-" * 118)
print("9. RUNTIME MODEL CONSTRUCTION WITHOUT CHILDREN")
print("-" * 118)


synset_runtime = None
varga_runtime = None


if Synset is not None:

    print()
    print("Synset(...)")

    try:

        synset_runtime = Synset(
            identifier="batch5f-synset",
            metadata=synset_metadata,
        )

        print(
            "  RESULT : SUCCESS"
        )

        print(
            f"  repr   : {synset_runtime!r}"
        )

        print(
            "  child_count :",
            getattr(
                synset_runtime,
                "child_count",
                "<missing>",
            ),
        )

        print(
            "  children type :",
            type(
                synset_runtime.children
            ).__name__,
        )

    except Exception as exc:

        print(
            "  RESULT : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


if Varga is not None:

    print()
    print("Varga(...)")

    try:

        varga_runtime = Varga(
            identifier="batch5f-varga",
            metadata=varga_metadata,
        )

        print(
            "  RESULT : SUCCESS"
        )

        print(
            f"  repr   : {varga_runtime!r}"
        )

        print(
            "  child_count :",
            getattr(
                varga_runtime,
                "child_count",
                "<missing>",
            ),
        )

        print(
            "  children type :",
            type(
                varga_runtime.children
            ).__name__,
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
print("10. EXPLICIT children= COMPATIBILITY")
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
print("11. CHILD MUTATION COMPATIBILITY")
print("-" * 118)


if synset_runtime is not None:

    print()
    print("Synset child API")

    print(
        "  add_child available :",
        hasattr(
            synset_runtime,
            "add_child",
        ),
    )

    print(
        "  extend available    :",
        hasattr(
            synset_runtime,
            "extend",
        ),
    )

    print(
        "  children available  :",
        hasattr(
            synset_runtime,
            "children",
        ),
    )


if varga_runtime is not None:

    print()
    print("Varga child API")

    print(
        "  add_child available :",
        hasattr(
            varga_runtime,
            "add_child",
        ),
    )

    print(
        "  extend available    :",
        hasattr(
            varga_runtime,
            "extend",
        ),
    )

    print(
        "  children available  :",
        hasattr(
            varga_runtime,
            "children",
        ),
    )


# ======================================================================
# Builder source inspection
# ======================================================================

print()
print("-" * 118)
print("12. BUILDER CONSTRUCTION CONTRACT")
print("-" * 118)


for cls in (
    SynsetBuilder,
    VargaBuilder,
):

    if cls is None:
        continue

    print()
    print(
        f"[{cls.__name__}]"
    )

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
print("13. BUILDER RUNTIME PROBES")
print("-" * 118)


for cls in (
    SynsetBuilder,
    VargaBuilder,
):

    if cls is None:
        continue

    print()
    print(
        cls.__name__
    )

    try:

        builder = cls()

        print(
            "  instantiation : SUCCESS"
        )

        print(
            "  abstractmethods :",
            sorted(
                getattr(
                    cls,
                    "__abstractmethods__",
                    set(),
                )
            ),
        )

    except Exception as exc:

        print(
            "  instantiation : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


# ======================================================================
# AST constructor pattern search
# ======================================================================

print()
print("-" * 118)
print("14. ACTIVE PRODUCTION CONSTRUCTOR PATTERN SEARCH")
print("-" * 118)


patterns = {
    "children= passed to ContainerNode/super": [],
    "direct add_child calls": [],
    "direct extend calls": [],
}


for path in REPO_ROOT.rglob("*.py"):

    if not is_production_python_file(path):
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

    module_name = module_name_from_path(
        path
    )

    if not module_name:
        continue

    for node in ast.walk(tree):

        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        text = (
            ast.get_source_segment(
                source,
                node,
            )
            or ""
        )

        compact = text.replace(
            "\n",
            " ",
        )

        if (
            "children=" in text
            and (
                "ContainerNode" in text
                or "super(" in text
            )
        ):

            patterns[
                "children= passed to ContainerNode/super"
            ].append(
                (
                    module_name,
                    node.lineno,
                    compact[:300],
                )
            )

        if ".add_child(" in text:

            patterns[
                "direct add_child calls"
            ].append(
                (
                    module_name,
                    node.lineno,
                    compact[:300],
                )
            )

        if ".extend(" in text:

            patterns[
                "direct extend calls"
            ].append(
                (
                    module_name,
                    node.lineno,
                    compact[:300],
                )
            )


for pattern_name, matches in patterns.items():

    print()
    print(pattern_name)

    if not matches:

        print(
            "  NONE"
        )

        continue

    for (
        module_name,
        lineno,
        text,
    ) in matches[:40]:

        print(
            f"  {module_name}:{lineno}: {text}"
        )


# ======================================================================
# Builder contract comparison
# ======================================================================

print()
print("-" * 118)
print("15. BUILDER CONTRACT COMPARISON")
print("-" * 118)


def builder_contract(
    cls,
) -> dict[str, object]:

    if cls is None:
        return {
            "resolved": False,
        }

    abstract_methods = set(
        getattr(
            cls,
            "__abstractmethods__",
            set(),
        )
    )

    has_create_instance = hasattr(
        cls,
        "_create_instance",
    )

    has_build = hasattr(
        cls,
        "build",
    )

    return {
        "resolved": True,
        "abstract": bool(
            abstract_methods
        ),
        "abstract_methods": sorted(
            abstract_methods
        ),
        "has_create_instance": has_create_instance,
        "has_build": has_build,
    }


for name, cls in (
    (
        "SynsetBuilder",
        SynsetBuilder,
    ),
    (
        "VargaBuilder",
        VargaBuilder,
    ),
):

    print()
    print(
        name,
        ":",
        builder_contract(cls),
    )


# ======================================================================
# Model contract comparison
# ======================================================================

print()
print("-" * 118)
print("16. MODEL CONTRACT COMPARISON")
print("-" * 118)


def constructor_parameters(
    cls,
) -> list[str]:

    if cls is None:
        return []

    try:

        signature = inspect.signature(
            cls
        )

    except Exception:

        return []

    return [
        parameter.name
        for parameter in signature.parameters.values()
        if parameter.name != "self"
    ]


for name, cls in (
    ("ContainerNode", ContainerNode),
    ("Synset", Synset),
    ("Varga", Varga),
):

    print()
    print(
        f"{name}:"
    )

    print(
        "  parameters :",
        constructor_parameters(cls),
    )


# ======================================================================
# Final architectural decision
# ======================================================================

print()
print("=" * 118)
print("BATCH 5F — DECISION GATE")
print("=" * 118)

print()
print("CURRENT FRAMEWORK CONTRACT")
print("--------------------------")

print(
    "ContainerNode constructor:"
)

print(
    "  identifier + metadata"
)

print(
    "ContainerNode child ownership:"
)

print(
    "  NodeCollection"
)

print(
    "ContainerNode child population:"
)

print(
    "  add_child / extend / remove_child / clear_children"
)

print()
print(
    "BaseBuilder contract:"
)

print(
    "  _create_instance() is abstract"
)

print()
print(
    "Amarakosha builder state:"
)

print(
    "  SynsetBuilder currently implements build()"
)

print(
    "  VargaBuilder currently implements build()"
)

print(
    "  neither implements _create_instance()"
)

print()
print(
    "Amarakosha model state:"
)

print(
    "  Synset/Varga currently accept children="
)

print(
    "  but ContainerNode does not"
)

print()
print("REPAIR BOUNDARY")
print("---------------")

print(
    "1. Do NOT modify ContainerNode."
)

print(
    "2. Do NOT modify BaseBuilder."
)

print(
    "3. Repair Synset/Varga construction against the existing"
)
print(
    "   ContainerNode + NodeCollection contract."
)

print(
    "4. Repair SynsetBuilder/VargaBuilder against the existing"
)
print(
    "   BaseBuilder/NodeBuilder contract."
)

print(
    "5. Preserve the existing fluent builder API."
)

print(
    "6. Keep SynsetRecordBuilder unchanged until the repaired"
)
print(
    "   SynsetBuilder can be exercised."
)

print(
    "7. Do NOT implement the canonical Amarakośa adapter yet."
)

print()
print("NEXT IMPLEMENTATION")
print("-------------------")
print(
    "Batch 5G — Conservative Synset/Varga + Builder Repair"
)

print()
print("=" * 118)
print("BATCH 5F COMPLETE — READ-ONLY AUDIT")
print("=" * 118)
