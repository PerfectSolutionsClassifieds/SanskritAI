
from __future__ import annotations

import inspect
import sys
from pathlib import Path
from typing import Any


ROOT = Path("/content/SanskritAI")

if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))


# =====================================================================
# Helpers
# =====================================================================

def section(title: str) -> None:
    print()
    print("=" * 118)
    print(title)
    print("=" * 118)


def safe_signature(obj: Any) -> str:
    try:
        return str(inspect.signature(obj))
    except Exception as exc:
        return f"<SIGNATURE UNAVAILABLE: {type(exc).__name__}: {exc}>"


def safe_source(obj: Any, max_lines: int = 180) -> str:
    try:
        source = inspect.getsource(obj)
    except Exception as exc:
        return (
            f"<SOURCE UNAVAILABLE: {type(exc).__name__}: {exc}>"
        )

    lines = source.splitlines()

    if len(lines) <= max_lines:
        return source

    return "\n".join(lines[:max_lines]) + (
        f"\n... <TRUNCATED: {len(lines) - max_lines} lines> ..."
    )


def print_class_report(cls: type[Any], label: str) -> None:
    print(f"[{label}]")
    print(f"  class    : {cls}")
    print(f"  module   : {cls.__module__}")
    print(f"  qualname : {cls.__qualname__}")
    print(f"  abstract : {inspect.isabstract(cls)}")
    print(f"  abstract methods: {sorted(getattr(cls, '__abstractmethods__', ())) }")

    print("  MRO:")
    for index, base in enumerate(cls.__mro__):
        print(f"    {index}: {base}")


def print_method(cls: type[Any], name: str) -> None:
    print(f"\n[{cls.__name__}.{name}]")

    try:
        method = getattr(cls, name)
    except AttributeError:
        print("  NOT FOUND")
        return

    print(f"  signature: {safe_signature(method)}")
    print(safe_source(method))


def print_owner(cls: type[Any], name: str) -> None:
    print(f"\n  {name}:")

    for base in cls.__mro__:
        if name in getattr(base, "__dict__", {}):
            owner = base
            print(f"    owner      : {owner}")
            print(f"    owner name : {owner.__name__}")

            try:
                attr = owner.__dict__[name]
                print(f"    signature  : {safe_signature(attr)}")
            except Exception:
                pass

            break
    else:
        print("    owner      : NOT FOUND")


def instantiate_probe(cls: type[Any], label: str) -> Any | None:
    print(f"\n[{label}() construction probe]")

    try:
        instance = cls()
        print("  SUCCESS")
        print(f"  type : {type(instance)}")
        print(f"  repr : {instance!r}")
        return instance
    except Exception as exc:
        print("  FAILURE")
        print(f"  {type(exc).__name__}: {exc}")
        return None


# =====================================================================
# Imports
# =====================================================================

section("BATCH 5E — AMARAKOSHA BUILDER FRAMEWORK CONTRACT AUDIT")

print(f"Repository root : {ROOT}")
print("Audit mode      : READ-ONLY")
print("Purpose         : determine existing BaseBuilder / NodeBuilder /")
print("                  ContainerNode construction semantics before repair")
print()
print("Production-file filter:")
print("  tests excluded")
print("  __pycache__ excluded")
print("  numeric historical suffixes excluded")
print("  _G<number> files excluded")


try:
    from SanskritAI.core.builders.base_builder import BaseBuilder
    from SanskritAI.core.builders.validated_builder import ValidatedBuilder
    from SanskritAI.core.builders.record_builder import RecordBuilder

    from SanskritAI.corpus.builders.base_builder import BaseBuilder as CorpusBaseBuilder
    from SanskritAI.corpus.builders.node_builder import NodeBuilder

    from SanskritAI.corpus.models.base_node import BaseNode
    from SanskritAI.corpus.models.container_node import ContainerNode

    from SanskritAI.amarakosha.builders.base_amarakosha_builder import (
        BaseAmarakoshaBuilder,
    )
    from SanskritAI.amarakosha.builders.synset_builder import SynsetBuilder
    from SanskritAI.amarakosha.builders.varga_builder import VargaBuilder

    from SanskritAI.amarakosha.models.synset import Synset
    from SanskritAI.amarakosha.models.varga import Varga

    print()
    print("All framework imports: SUCCESS")

except Exception as exc:
    print()
    print("IMPORT FAILURE:")
    print(f"  {type(exc).__name__}: {exc}")
    raise


# =====================================================================
# 1. BaseBuilder
# =====================================================================

section("1. CORE BASE BUILDER CONTRACT")

print_class_report(BaseBuilder, "Core BaseBuilder")

for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "reset",
    "instance",
    "from_instance",
    "clone",
    "validate",
):
    print_method(BaseBuilder, method_name)

print("\nBaseBuilder method ownership:")
for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "reset",
    "instance",
    "from_instance",
    "clone",
    "validate",
):
    print_owner(BaseBuilder, method_name)


# =====================================================================
# 2. Corpus BaseBuilder
# =====================================================================

section("2. CORPUS BASE BUILDER CONTRACT")

print_class_report(CorpusBaseBuilder, "Corpus BaseBuilder")

for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "reset",
    "instance",
    "from_instance",
    "clone",
    "validate",
):
    print_method(CorpusBaseBuilder, method_name)

print("\nCorpus BaseBuilder method ownership:")
for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "reset",
    "instance",
    "from_instance",
    "clone",
    "validate",
):
    print_owner(CorpusBaseBuilder, method_name)


# =====================================================================
# 3. ValidatedBuilder
# =====================================================================

section("3. VALIDATED BUILDER CONTRACT")

print_class_report(ValidatedBuilder, "ValidatedBuilder")

for method_name in (
    "__init__",
    "validate",
    "build",
):
    print_method(ValidatedBuilder, method_name)


# =====================================================================
# 4. NodeBuilder
# =====================================================================

section("4. NODE BUILDER CONTRACT")

print_class_report(NodeBuilder, "NodeBuilder")

for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "validate",
    "reset",
    "instance",
    "from_instance",
    "clone",
    "with_identifier",
    "with_metadata",
    "with_parent_identifier",
    "with_sequence_number",
    "with_title",
    "with_description",
):
    print_method(NodeBuilder, method_name)

print("\nNodeBuilder method ownership:")
for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "validate",
    "reset",
    "instance",
    "from_instance",
    "clone",
):
    print_owner(NodeBuilder, method_name)


# =====================================================================
# 5. BaseAmarakoshaBuilder
# =====================================================================

section("5. BASE AMARAKOSHA BUILDER CONTRACT")

print_class_report(
    BaseAmarakoshaBuilder,
    "BaseAmarakoshaBuilder",
)

for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "validate",
    "reset",
    "instance",
    "from_instance",
    "clone",
):
    print_method(BaseAmarakoshaBuilder, method_name)

print("\nBaseAmarakoshaBuilder method ownership:")
for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "validate",
    "reset",
    "instance",
    "from_instance",
    "clone",
):
    print_owner(BaseAmarakoshaBuilder, method_name)


# =====================================================================
# 6. SynsetBuilder
# =====================================================================

section("6. SYNSET BUILDER FRAMEWORK COMPATIBILITY")

print_class_report(SynsetBuilder, "SynsetBuilder")

print("\nSynsetBuilder ownership:")
for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "validate",
    "reset",
    "instance",
    "from_instance",
    "clone",
    "with_identifier",
    "with_metadata",
    "add_lexeme",
):
    print_owner(SynsetBuilder, method_name)

for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "validate",
):
    print_method(SynsetBuilder, method_name)


# =====================================================================
# 7. VargaBuilder
# =====================================================================

section("7. VARGA BUILDER FRAMEWORK COMPATIBILITY")

print_class_report(VargaBuilder, "VargaBuilder")

print("\nVargaBuilder ownership:")
for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "validate",
    "reset",
    "instance",
    "from_instance",
    "clone",
    "with_identifier",
    "with_metadata",
    "add_synset",
):
    print_owner(VargaBuilder, method_name)

for method_name in (
    "__init__",
    "_create_instance",
    "build",
    "validate",
):
    print_method(VargaBuilder, method_name)


# =====================================================================
# 8. ContainerNode
# =====================================================================

section("8. CONTAINER NODE CONSTRUCTION CONTRACT")

print_class_report(ContainerNode, "ContainerNode")

for method_name in (
    "__init__",
    "add_child",
    "remove_child",
    "children",
):
    print_method(ContainerNode, method_name)

print("\nContainerNode constructor signature:")
print(f"  {safe_signature(ContainerNode.__init__)}")


# =====================================================================
# 9. BaseNode
# =====================================================================

section("9. BASE NODE CONSTRUCTION CONTRACT")

print_class_report(BaseNode, "BaseNode")

for method_name in (
    "__init__",
):
    print_method(BaseNode, method_name)

print("\nBaseNode constructor signature:")
print(f"  {safe_signature(BaseNode.__init__)}")


# =====================================================================
# 10. Synset model constructor
# =====================================================================

section("10. SYNSET MODEL CONSTRUCTOR COMPATIBILITY")

print_class_report(Synset, "Synset")

print("\nSynset constructor:")
print(f"  {safe_signature(Synset.__init__)}")

print("\nSynset source:")
print(safe_source(Synset))


# =====================================================================
# 11. Varga model constructor
# =====================================================================

section("11. VARGA MODEL CONSTRUCTOR COMPATIBILITY")

print_class_report(Varga, "Varga")

print("\nVarga constructor:")
print(f"  {safe_signature(Varga.__init__)}")

print("\nVarga source:")
print(safe_source(Varga))


# =====================================================================
# 12. Construction matrix
# =====================================================================

section("12. CONSTRUCTION CONTRACT MATRIX")

print(
    "COMPONENT                  | CONCRETE | ABSTRACT METHOD       | CONSTRUCTOR"
)
print("-" * 118)

for cls in (
    BaseBuilder,
    CorpusBaseBuilder,
    NodeBuilder,
    BaseAmarakoshaBuilder,
    SynsetBuilder,
    VargaBuilder,
    Synset,
    Varga,
):
    abstract_methods = sorted(
        getattr(cls, "__abstractmethods__", ())
    )

    print(
        f"{cls.__name__:26} | "
        f"{str(not inspect.isabstract(cls)):8} | "
        f"{','.join(abstract_methods) if abstract_methods else '-':21} | "
        f"{safe_signature(cls.__init__)}"
    )


# =====================================================================
# 13. Runtime instantiation probes
# =====================================================================

section("13. READ-ONLY RUNTIME INSTANTIATION PROBES")

synset_builder = instantiate_probe(
    SynsetBuilder,
    "SynsetBuilder",
)

varga_builder = instantiate_probe(
    VargaBuilder,
    "VargaBuilder",
)

synset = None
varga = None

print("\n[Synset minimal constructor probe]")

try:
    synset = Synset(
        identifier="probe:synset",
        metadata=None,  # intentional compatibility probe
    )
    print("  SUCCESS")
    print(f"  repr : {synset!r}")
except Exception as exc:
    print("  FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


print("\n[Varga minimal constructor probe]")

try:
    varga = Varga(
        identifier="probe:varga",
        metadata=None,  # intentional compatibility probe
    )
    print("  SUCCESS")
    print(f"  repr : {varga!r}")
except Exception as exc:
    print("  FAILURE")
    print(f"  {type(exc).__name__}: {exc}")


# =====================================================================
# 14. Explicit children compatibility probe
# =====================================================================

section("14. CHILDREN ARGUMENT COMPATIBILITY")

print("[Synset(children=...) signature compatibility]")

try:
    sig = inspect.signature(Synset.__init__)
    has_children = "children" in sig.parameters

    print(f"  declared children parameter : {has_children}")

    try:
        Synset(
            identifier="probe:synset",
            metadata=None,
            children=[],
        )
        print("  runtime children argument   : ACCEPTED")
    except Exception as exc:
        print("  runtime children argument   : REJECTED")
        print(f"    {type(exc).__name__}: {exc}")

except Exception as exc:
    print("  probe failure:")
    print(f"    {type(exc).__name__}: {exc}")


print("\n[Varga(children=...) signature compatibility]")

try:
    sig = inspect.signature(Varga.__init__)
    has_children = "children" in sig.parameters

    print(f"  declared children parameter : {has_children}")

    try:
        Varga(
            identifier="probe:varga",
            metadata=None,
            children=[],
        )
        print("  runtime children argument   : ACCEPTED")
    except Exception as exc:
        print("  runtime children argument   : REJECTED")
        print(f"    {type(exc).__name__}: {exc}")

except Exception as exc:
    print("  probe failure:")
    print(f"    {type(exc).__name__}: {exc}")


# =====================================================================
# 15. Builder build implementation comparison
# =====================================================================

section("15. BUILDER BUILD IMPLEMENTATION VS BASE CONTRACT")

for cls in (SynsetBuilder, VargaBuilder):

    print(f"\n[{cls.__name__}]")

    try:
        build_method = cls.__dict__.get("build")
        create_method = cls.__dict__.get("_create_instance")

        print(
            "  subclass defines build()           : "
            f"{build_method is not None}"
        )
        print(
            "  subclass defines _create_instance(): "
            f"{create_method is not None}"
        )

        if build_method is not None:
            print("\n  subclass build() source:")
            print(safe_source(build_method))

        if create_method is not None:
            print("\n  subclass _create_instance() source:")
            print(safe_source(create_method))

    except Exception as exc:
        print(
            f"  comparison failure: "
            f"{type(exc).__name__}: {exc}"
        )


# =====================================================================
# 16. Framework semantic comparison
# =====================================================================

section("16. FRAMEWORK SEMANTIC QUESTIONS")

questions = [
    (
        "Q1",
        "Does BaseBuilder.build() depend on _create_instance(), "
        "or does it only return an already-created _instance?"
    ),
    (
        "Q2",
        "Does NodeBuilder initialize _instance through _create_instance(), "
        "or is _instance populated another way?"
    ),
    (
        "Q3",
        "Is BaseAmarakoshaBuilder._create_instance() actually required "
        "by the runtime semantics of SynsetBuilder/VargaBuilder?"
    ),
    (
        "Q4",
        "Are Synset/Varga expected to construct children through "
        "ContainerNode's constructor or through post-construction methods?"
    ),
    (
        "Q5",
        "Does the existing framework provide an established pattern "
        "for concrete ContainerNode subclasses?"
    ),
    (
        "Q6",
        "Should SynsetBuilder/VargaBuilder implement _create_instance(), "
        "or should their current build() implementations be aligned with "
        "BaseBuilder semantics?"
    ),
]

for code, question in questions:
    print(f"{code}: {question}")


# =====================================================================
# 17. Existing ContainerNode subclass discovery
# =====================================================================

section("17. EXISTING CONTAINERNODE SUBCLASS PATTERN DISCOVERY")

print("Searching active production Python files for ContainerNode subclasses.")
print("Historical duplicate files and tests are excluded.")

matches: list[Path] = []

for path in ROOT.rglob("*.py"):

    relative = path.relative_to(ROOT)
    parts = relative.parts

    if "tests" in parts:
        continue

    if "__pycache__" in parts:
        continue

    name = path.name

    stem = path.stem

    # Exclude numeric historical suffixes:
    # foo1.py, foo2.py, foo10.py, etc.
    if stem.rstrip("0123456789") != stem:
        continue

    # Exclude _G<number>.py
    import re

    if re.search(r"_G\d+$", stem):
        continue

    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        continue

    if "ContainerNode" in text and "(ContainerNode" in text:
        matches.append(path)


if matches:
    for path in sorted(matches):
        print(f"  {path}")
else:
    print("  No active ContainerNode subclass source pattern found.")


# =====================================================================
# 18. Preliminary architectural interpretation
# =====================================================================

section("18. BATCH 5E PRELIMINARY ARCHITECTURAL INTERPRETATION")

print(
    "The following are evidence classifications only; "
    "no production change is made."
)

print()
print("E1: SynsetBuilder/VargaBuilder abstractness")
print(
    "    Investigate BaseBuilder / NodeBuilder initialization semantics "
    "before implementing _create_instance()."
)

print()
print("E2: Synset/Varga children incompatibility")
print(
    "    Investigate ContainerNode constructor and existing subclasses "
    "before changing Synset/Varga constructors."
)

print()
print("E3: Existing Lexeme ownership")
print(
    "    Lexeme belongs to domain.lexical.lexeme.Lexeme. "
    "No LexemeMetadata replacement should be created."
)

print()
print("E4: Registry")
print(
    "    AmarakoshaRegistry remains a valid registration boundary."
)

print()
print("E5: SynsetRecordBuilder")
print(
    "    It is concrete, but its current build path depends on "
    "SynsetBuilder and therefore inherits the builder compatibility issue."
)

print()
print("E6: Canonical adapter")
print(
    "    Canonical adapter implementation remains BLOCKED until "
    "the Amarakośa runtime graph can be constructed reliably."
)


# =====================================================================
# 19. Decision gate
# =====================================================================

section("19. BATCH 5E DECISION GATE")

print("NEXT ACTIONS DEPEND ON THE EVIDENCE ABOVE:")
print()
print("  CASE A:")
print("    If BaseBuilder/NodeBuilder semantics show _create_instance()")
print("    is the intended construction hook:")
print("      -> inspect existing concrete builder patterns")
print("      -> repair SynsetBuilder/VargaBuilder using that pattern")
print()
print("  CASE B:")
print("    If Synset/Varga constructor semantics conflict with ContainerNode:")
print("      -> inspect existing ContainerNode subclasses")
print("      -> repair the model constructors using the established pattern")
print()
print("  CASE C:")
print("    If both mismatches are confirmed:")
print("      -> perform a narrowly scoped framework-compatible repair")
print("      -> add focused Amarakośa construction tests")
print("      -> then complete importer orchestration")
print()
print("  CASE D:")
print("    If the framework reveals an existing reusable construction path:")
print("      -> reuse it; do not introduce another builder abstraction")
print()
print("CANONICAL ADAPTER STATUS: BLOCKED")
print("PRODUCTION FILES MODIFIED: NO")
print()
print("BATCH 5E COMPLETE")
print("=" * 118)
