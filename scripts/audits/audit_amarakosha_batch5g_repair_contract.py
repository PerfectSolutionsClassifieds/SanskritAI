
"""
BATCH 5G-0 — AMARAKOSHA REPAIR CONTRACT VERIFICATION

Purpose
-------
Verify the exact existing BaseBuilder / NodeBuilder construction
semantics immediately before making the minimal Amarakośa repair.

This audit is READ-ONLY.

It specifically answers:

1. How does BaseBuilder.build() use _create_instance()?
2. Does BaseBuilder.validate() impose any additional construction
   requirements?
3. Does NodeBuilder alter the BaseBuilder contract?
4. Are there existing production builder subclasses that implement
   _create_instance()?
5. Can SynsetBuilder/VargaBuilder safely implement _create_instance()
   while retaining their current fluent build() API?
6. Can Synset/Varga safely initialize ContainerNode first and then
   populate children using extend()?

Production-file filters:
    tests excluded
    __pycache__ excluded
    numeric historical suffixes excluded
    _G<number>.py excluded

IMPORTANT
---------
This script does not modify production code.
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
print("BATCH 5G-0 — AMARAKOSHA REPAIR CONTRACT VERIFICATION")
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

    parts_lower = {
        part.lower()
        for part in path.parts
    }

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


def module_name_from_path(path: Path) -> str | None:

    try:
        relative = path.relative_to(REPO_ROOT)
    except ValueError:
        return None

    if relative.name == "__init__.py":
        parts = list(relative.parts[:-1])
    else:
        parts = list(
            relative.with_suffix("").parts
        )

    if not parts:
        return None

    return ".".join(
        ["SanskritAI", *parts]
    )


# ======================================================================
# Symbol discovery
# ======================================================================

def discover_symbol(
    symbol: str,
) -> list[str]:

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

            if (
                isinstance(
                    node,
                    ast.ClassDef,
                )
                and node.name == symbol
            ):

                module_name = (
                    module_name_from_path(path)
                )

                if module_name:
                    modules.append(
                        module_name
                    )

                break

    return sorted(
        set(modules)
    )


def resolve_symbol(
    symbol: str,
):

    candidates = discover_symbol(
        symbol
    )

    print()
    print(symbol)
    print("-" * 90)

    for module_name in candidates:

        try:

            module = importlib.import_module(
                module_name
            )

            if hasattr(
                module,
                symbol,
            ):

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
# Resolve framework
# ======================================================================

print("-" * 118)
print("1. FRAMEWORK RESOLUTION")
print("-" * 118)

base_builder_module, BaseBuilder = resolve_symbol(
    "BaseBuilder"
)

node_builder_module, NodeBuilder = resolve_symbol(
    "NodeBuilder"
)

container_module, ContainerNode = resolve_symbol(
    "ContainerNode"
)

node_collection_module, NodeCollection = resolve_symbol(
    "NodeCollection"
)


# ======================================================================
# Resolve Amarakośa
# ======================================================================

print()
print("-" * 118)
print("2. AMARAKOSHA RESOLUTION")
print("-" * 118)

_, SynsetBuilder = resolve_symbol(
    "SynsetBuilder"
)

_, VargaBuilder = resolve_symbol(
    "VargaBuilder"
)

_, Synset = resolve_symbol(
    "Synset"
)

_, Varga = resolve_symbol(
    "Varga"
)

_, SynsetMetadata = resolve_symbol(
    "SynsetMetadata"
)

_, VargaMetadata = resolve_symbol(
    "VargaMetadata"
)


# ======================================================================
# BaseBuilder source
# ======================================================================

print()
print("-" * 118)
print("3. BASEBUILDER CONSTRUCTION SEMANTICS")
print("-" * 118)


def show_source(
    cls,
    method_name: str,
) -> None:

    if cls is None:
        return

    print()
    print(
        f"{cls.__module__}."
        f"{cls.__name__}.{method_name}"
    )

    try:

        source = inspect.getsource(
            getattr(
                cls,
                method_name,
            )
        )

        for line in source.splitlines():

            print(
                f"  {line}"
            )

    except Exception as exc:

        print(
            f"  <source unavailable: "
            f"{type(exc).__name__}: {exc}>"
        )


if BaseBuilder is not None:

    print(
        "BaseBuilder signature:",
        inspect.signature(BaseBuilder),
    )

    print(
        "Abstract methods:",
        sorted(
            getattr(
                BaseBuilder,
                "__abstractmethods__",
                set(),
            )
        ),
    )

    show_source(
        BaseBuilder,
        "__init__",
    )

    show_source(
        BaseBuilder,
        "build",
    )

    show_source(
        BaseBuilder,
        "_create_instance",
    )

    show_source(
        BaseBuilder,
        "validate",
    )


# ======================================================================
# NodeBuilder source
# ======================================================================

print()
print("-" * 118)
print("4. NODEBUILDER SEMANTICS")
print("-" * 118)

if NodeBuilder is not None:

    print(
        "NodeBuilder signature:",
        inspect.signature(NodeBuilder),
    )

    print(
        "Abstract methods:",
        sorted(
            getattr(
                NodeBuilder,
                "__abstractmethods__",
                set(),
            )
        ),
    )

    show_source(
        NodeBuilder,
        "__init__",
    )

    show_source(
        NodeBuilder,
        "build",
    )

    show_source(
        NodeBuilder,
        "_create_instance",
    )

    show_source(
        NodeBuilder,
        "validate",
    )


# ======================================================================
# Amarakośa builder source
# ======================================================================

print()
print("-" * 118)
print("5. AMARAKOSHA BUILDER METHODS")
print("-" * 118)

for cls in (
    SynsetBuilder,
    VargaBuilder,
):

    if cls is None:
        continue

    print()
    print(
        f"[{cls.__module__}.{cls.__name__}]"
    )

    print(
        "Constructor:",
        inspect.signature(cls),
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

    for method_name in (
        "__init__",
        "build",
        "_create_instance",
    ):

        show_source(
            cls,
            method_name,
        )


# ======================================================================
# ContainerNode semantics
# ======================================================================

print()
print("-" * 118)
print("6. CONTAINERNODE SEMANTICS")
print("-" * 118)

if ContainerNode is not None:

    print(
        "Constructor:",
        inspect.signature(
            ContainerNode
        ),
    )

    show_source(
        ContainerNode,
        "__init__",
    )

    show_source(
        ContainerNode,
        "add_child",
    )

    show_source(
        ContainerNode,
        "extend",
    )

    show_source(
        ContainerNode,
        "clear_children",
    )


# ======================================================================
# NodeCollection semantics
# ======================================================================

print()
print("-" * 118)
print("7. NODECOLLECTION SEMANTICS")
print("-" * 118)

if NodeCollection is not None:

    print(
        "Constructor:",
        inspect.signature(
            NodeCollection
        ),
    )

    show_source(
        NodeCollection,
        "__init__",
    )

    show_source(
        NodeCollection,
        "add",
    )

    show_source(
        NodeCollection,
        "extend",
    )


# ======================================================================
# Runtime model construction
# ======================================================================

print()
print("-" * 118)
print("8. CURRENT MODEL CONSTRUCTION")
print("-" * 118)

synset_metadata = None
varga_metadata = None

if SynsetMetadata is not None:

    try:

        synset_metadata = SynsetMetadata()

        print(
            "SynsetMetadata() : SUCCESS"
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
            "VargaMetadata() : SUCCESS"
        )

    except Exception as exc:

        print(
            "VargaMetadata() : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


# ======================================================================
# Existing model construction probe
# ======================================================================

print()
print("-" * 118)
print("9. CURRENT SYNSET / VARGA CONSTRUCTION")
print("-" * 118)

if Synset is not None:

    try:

        Synset(
            identifier="batch5g-current-synset",
            metadata=synset_metadata,
        )

        print(
            "Synset without children : SUCCESS"
        )

    except Exception as exc:

        print(
            "Synset without children : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


if Varga is not None:

    try:

        Varga(
            identifier="batch5g-current-varga",
            metadata=varga_metadata,
        )

        print(
            "Varga without children : SUCCESS"
        )

    except Exception as exc:

        print(
            "Varga without children : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


# ======================================================================
# Simulated post-repair construction
# ======================================================================

print()
print("-" * 118)
print("10. SIMULATED CONTAINERNODE-COMPATIBLE CONSTRUCTION")
print("-" * 118)

print(
    "This section does NOT modify Synset/Varga."
)

if ContainerNode is not None:

    print()
    print(
        "ContainerNode(identifier, metadata)"
    )

    try:

        simulated = ContainerNode(
            identifier="batch5g-simulated",
            metadata=synset_metadata,
        )

        print(
            "  construction : SUCCESS"
        )

        print(
            "  child_count  :",
            getattr(
                simulated,
                "child_count",
                "<missing>",
            ),
        )

        print(
            "  children     :",
            type(
                simulated.children
            ).__name__,
        )

    except Exception as exc:

        print(
            "  construction : FAILED "
            f"{type(exc).__name__}: {exc}"
        )


# ======================================================================
# Existing production builder subclass discovery
# ======================================================================

print()
print("-" * 118)
print("11. EXISTING PRODUCTION BUILDER SUBCLASSES")
print("-" * 118)


builder_class_names = {
    "BaseBuilder",
    "NodeBuilder",
    "RecordBuilder",
    "ValidatedBuilder",
    "BaseAmarakoshaBuilder",
    "SynsetBuilder",
    "VargaBuilder",
    "SynsetRecordBuilder",
}


found_builder_subclasses: list[
    tuple[str, str, str]
] = []


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

    for node in tree.body:

        if not isinstance(
            node,
            ast.ClassDef,
        ):
            continue

        bases: list[str] = []

        for base in node.bases:

            if isinstance(
                base,
                ast.Name,
            ):

                bases.append(
                    base.id
                )

            elif isinstance(
                base,
                ast.Attribute,
            ):

                bases.append(
                    base.attr
                )

        if not any(
            base in builder_class_names
            for base in bases
        ):
            continue

        methods = {
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

        found_builder_subclasses.append(
            (
                module_name,
                node.name,
                ", ".join(bases),
            )
        )

        print()
        print(
            f"{module_name}.{node.name}"
        )

        print(
            "  bases   :",
            ", ".join(bases),
        )

        print(
            "  methods :",
            ", ".join(
                sorted(methods)
            ),
        )

        print(
            "  _create_instance :",
            "_create_instance" in methods,
        )


if not found_builder_subclasses:

    print(
        "No production builder subclasses "
        "discovered by AST scan."
    )


# ======================================================================
# Explicit source-level repair candidates
# ======================================================================

print()
print("-" * 118)
print("12. REPAIR CANDIDATE ANALYSIS")
print("-" * 118)

print()
print("MODEL REPAIR")
print("------------")

print(
    "Current:"
)

print(
    "  Synset.__init__ -> "
    "super().__init__(identifier, metadata, children)"
)

print(
    "  Varga.__init__  -> "
    "super().__init__(identifier, metadata, children)"
)

print(
    "Existing ContainerNode:"
)

print(
    "  super().__init__(identifier, metadata)"
)

print(
    "  self._children = NodeCollection()"
)

print(
    "Therefore candidate repair:"
)

print(
    "  call ContainerNode with identifier + metadata"
)

print(
    "  then call self.extend(children) when children exists"
)

print()
print("BUILDER REPAIR")
print("--------------")

print(
    "Current:"
)

print(
    "  SynsetBuilder.build() directly constructs Synset"
)

print(
    "  VargaBuilder.build() directly constructs Varga"
)

print(
    "Framework:"
)

print(
    "  _create_instance() is abstract"
)

print(
    "Therefore candidate repair:"
)

print(
    "  implement _create_instance() in each concrete builder"
)

print(
    "  preserve existing fluent methods"
)

print(
    "  preserve existing public build() method"
)


# ======================================================================
# Final gate
# ======================================================================

print()
print("=" * 118)
print("BATCH 5G-0 — DECISION GATE")
print("=" * 118)

base_builder_ok = BaseBuilder is not None
node_builder_ok = NodeBuilder is not None
container_ok = ContainerNode is not None
synset_ok = Synset is not None
varga_ok = Varga is not None
synset_builder_ok = SynsetBuilder is not None
varga_builder_ok = VargaBuilder is not None

print()
print(
    "BaseBuilder resolved       :",
    base_builder_ok,
)

print(
    "NodeBuilder resolved       :",
    node_builder_ok,
)

print(
    "ContainerNode resolved     :",
    container_ok,
)

print(
    "Synset resolved             :",
    synset_ok,
)

print(
    "Varga resolved              :",
    varga_ok,
)

print(
    "SynsetBuilder resolved      :",
    synset_builder_ok,
)

print(
    "VargaBuilder resolved       :",
    varga_builder_ok,
)

print()
print("REPAIR PRINCIPLES")
print("------------------")

print(
    "1. ContainerNode remains unchanged."
)

print(
    "2. BaseBuilder remains unchanged."
)

print(
    "3. NodeBuilder remains unchanged."
)

print(
    "4. Synset/Varga remain ContainerNode subclasses."
)

print(
    "5. Existing child ownership remains NodeCollection."
)

print(
    "6. Existing fluent builder API remains unchanged."
)

print(
    "7. No new abstraction is introduced."
)

print(
    "8. No canonical adapter is implemented."
)

print()
print("NEXT STEP")
print("----------")

print(
    "If BaseBuilder.build() confirms that _create_instance()"
)
print(
    "is the intended concrete construction hook, proceed to:"
)

print(
    "  BATCH 5G — MINIMAL SYNSET / VARGA + BUILDER REPAIR"
)

print()
print("=" * 118)
print("BATCH 5G-0 COMPLETE — READ-ONLY")
print("=" * 118)
