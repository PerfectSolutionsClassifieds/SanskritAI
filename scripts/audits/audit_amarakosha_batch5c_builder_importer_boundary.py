from __future__ import annotations

"""
BATCH 5C — AMARAKOSHA BUILDER / IMPORTER BOUNDARY AUDIT

Purpose
-------
Inspect the existing Amarakośa record -> builder -> domain -> registry
boundary before any production implementation is changed.

This audit is READ-ONLY.

It does NOT:
- modify production code
- instantiate abstract builders
- implement _create_instance()
- modify BaseAmarakoshaBuilder
- modify SynsetBuilder
- modify VargaBuilder
- modify AmarakoshaImporter
- modify AmarakoshaRegistry
- create an adapter
- modify canonical models

Primary architectural question
------------------------------
Should the existing Amarakośa builder/importer boundary be completed
before canonical integration?

Expected intended flow
----------------------
Source
  ↓
AmarakoshaParser
  ↓
SynsetRecord / VargaRecord
  ↓
Builder
  ↓
Synset / Varga
  ↓
AmarakoshaRegistry
  ↓
Canonical adapter
"""

from inspect import getsource, signature
from typing import Any

from SanskritAI.amarakosha.builders.base_amarakosha_builder import (
    BaseAmarakoshaBuilder,
)
from SanskritAI.amarakosha.builders.base_knowledge_record_builder import (
    BaseKnowledgeRecordBuilder,
)
from SanskritAI.amarakosha.builders.synset_builder import SynsetBuilder
from SanskritAI.amarakosha.builders.varga_builder import VargaBuilder

from SanskritAI.amarakosha.importers.amarakosha_importer import (
    AmarakoshaImporter,
)
from SanskritAI.amarakosha.registries.amarakosha_registry import (
    AmarakoshaRegistry,
)

from SanskritAI.amarakosha.records.synset_record import SynsetRecord
from SanskritAI.amarakosha.records.varga_record import VargaRecord

from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.models.varga import Varga
from SanskritAI.amarakosha.models.synset_metadata import SynsetMetadata
from SanskritAI.amarakosha.models.varga_metadata import VargaMetadata

from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexeme_metadata import LexemeMetadata


WIDTH = 118


def section(title: str) -> None:
    print()
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def show_signature(label: str, obj: Any) -> None:
    print()
    print(f"[{label}]")
    try:
        print(f"signature: {signature(obj)}")
    except Exception as exc:
        print(f"signature: <ERROR: {exc}>")


def show_source(label: str, obj: Any) -> None:
    print()
    print(f"[{label} source]")
    try:
        print(getsource(obj))
    except Exception as exc:
        print(f"<SOURCE UNAVAILABLE: {exc}>")


def show_abstract_contract(label: str, cls: type[Any]) -> None:
    print()
    print(f"[{label} abstract contract]")

    abstract_methods = sorted(
        getattr(cls, "__abstractmethods__", set())
    )

    print(f"abstract: {bool(abstract_methods)}")
    print(f"abstract methods: {abstract_methods}")

    for name in abstract_methods:
        try:
            member = getattr(cls, name)
            print()
            print(f"abstract method: {name}")
            print(f"signature: {signature(member)}")
            print(getsource(member))
        except Exception as exc:
            print(
                f"  unable to inspect abstract method "
                f"{name}: {exc}"
            )


def show_class_hierarchy(label: str, cls: type[Any]) -> None:
    print()
    print(f"[{label} MRO]")

    for index, base in enumerate(cls.__mro__):
        print(f"  {index}: {base}")


def show_public_methods(label: str, cls: type[Any]) -> None:
    print()
    print(f"[{label} public/candidate methods]")

    names = []

    for name in dir(cls):
        if name.startswith("_"):
            continue

        try:
            value = getattr(cls, name)
        except Exception:
            continue

        if callable(value):
            names.append(name)

    for name in names:
        try:
            print(f"  {name}{signature(getattr(cls, name))}")
        except Exception:
            print(f"  {name}")


def inspect_method(
    label: str,
    cls: type[Any],
    method_name: str,
) -> None:
    print()
    print(f"[{label}.{method_name}]")

    try:
        method = getattr(cls, method_name)
    except AttributeError:
        print("  <MISSING>")
        return

    try:
        print(f"signature: {signature(method)}")
    except Exception as exc:
        print(f"signature: <ERROR: {exc}>")

    try:
        print(getsource(method))
    except Exception as exc:
        print(f"<SOURCE UNAVAILABLE: {exc}>")


def main() -> None:
    section(
        "BATCH 5C — AMARAKOSHA BUILDER / IMPORTER BOUNDARY AUDIT"
    )

    print("Repository root : /content/SanskritAI")
    print("Audit mode      : READ-ONLY")
    print(
        "Architectural question : "
        "complete builder/importer boundary before canonical integration?"
    )

    # -------------------------------------------------------------
    # 1. Base builder hierarchy
    # -------------------------------------------------------------

    section("1. BASE BUILDER HIERARCHY")

    show_signature(
        "BaseKnowledgeRecordBuilder",
        BaseKnowledgeRecordBuilder,
    )
    show_class_hierarchy(
        "BaseKnowledgeRecordBuilder",
        BaseKnowledgeRecordBuilder,
    )
    show_abstract_contract(
        "BaseKnowledgeRecordBuilder",
        BaseKnowledgeRecordBuilder,
    )
    show_public_methods(
        "BaseKnowledgeRecordBuilder",
        BaseKnowledgeRecordBuilder,
    )

    show_signature(
        "BaseAmarakoshaBuilder",
        BaseAmarakoshaBuilder,
    )
    show_class_hierarchy(
        "BaseAmarakoshaBuilder",
        BaseAmarakoshaBuilder,
    )
    show_abstract_contract(
        "BaseAmarakoshaBuilder",
        BaseAmarakoshaBuilder,
    )
    show_public_methods(
        "BaseAmarakoshaBuilder",
        BaseAmarakoshaBuilder,
    )

    inspect_method(
        "BaseAmarakoshaBuilder",
        BaseAmarakoshaBuilder,
        "_create_instance",
    )

    inspect_method(
        "BaseAmarakoshaBuilder",
        BaseAmarakoshaBuilder,
        "build",
    )

    # -------------------------------------------------------------
    # 2. SynsetBuilder
    # -------------------------------------------------------------

    section("2. SYNSET BUILDER")

    show_signature("SynsetBuilder", SynsetBuilder)
    show_class_hierarchy("SynsetBuilder", SynsetBuilder)
    show_abstract_contract("SynsetBuilder", SynsetBuilder)
    show_public_methods("SynsetBuilder", SynsetBuilder)

    inspect_method(
        "SynsetBuilder",
        SynsetBuilder,
        "__init__",
    )

    inspect_method(
        "SynsetBuilder",
        SynsetBuilder,
        "with_identifier",
    )

    inspect_method(
        "SynsetBuilder",
        SynsetBuilder,
        "with_metadata",
    )

    inspect_method(
        "SynsetBuilder",
        SynsetBuilder,
        "add_lexeme",
    )

    inspect_method(
        "SynsetBuilder",
        SynsetBuilder,
        "build",
    )

    # -------------------------------------------------------------
    # 3. VargaBuilder
    # -------------------------------------------------------------

    section("3. VARGA BUILDER")

    show_signature("VargaBuilder", VargaBuilder)
    show_class_hierarchy("VargaBuilder", VargaBuilder)
    show_abstract_contract("VargaBuilder", VargaBuilder)
    show_public_methods("VargaBuilder", VargaBuilder)

    inspect_method(
        "VargaBuilder",
        VargaBuilder,
        "__init__",
    )

    inspect_method(
        "VargaBuilder",
        VargaBuilder,
        "with_identifier",
    )

    inspect_method(
        "VargaBuilder",
        VargaBuilder,
        "with_metadata",
    )

    inspect_method(
        "VargaBuilder",
        VargaBuilder,
        "add_synset",
    )

    inspect_method(
        "VargaBuilder",
        VargaBuilder,
        "build",
    )

    # -------------------------------------------------------------
    # 4. Domain construction contracts
    # -------------------------------------------------------------

    section("4. DOMAIN CONSTRUCTION CONTRACTS")

    show_signature("Synset", Synset)
    show_signature("Varga", Varga)

    show_signature("SynsetMetadata", SynsetMetadata)
    show_signature("VargaMetadata", VargaMetadata)

    show_signature("Lexeme", Lexeme)
    show_signature("LexemeMetadata", LexemeMetadata)

    # -------------------------------------------------------------
    # 5. Record → domain field compatibility
    # -------------------------------------------------------------

    section("5. RECORD → DOMAIN CONSTRUCTION COMPATIBILITY")

    print(
        "The following table identifies fields that can potentially "
        "be transferred without inventing new source data."
    )
    print()

    rows = [
        (
            "SynsetRecord.identifier",
            "Synset.identifier",
            "DIRECT",
            "Same conceptual identity boundary.",
        ),
        (
            "SynsetRecord.kanda",
            "SynsetMetadata.kanda",
            "DIRECT",
            "Same Amarakośa structural dimension.",
        ),
        (
            "SynsetRecord.varga",
            "SynsetMetadata.varga",
            "DIRECT",
            "Same source structural dimension.",
        ),
        (
            "SynsetRecord.verse",
            "SynsetMetadata.verse_number",
            "DIRECT",
            "Verse number maps naturally.",
        ),
        (
            "SynsetRecord.devanagari",
            "LexemeMetadata.lemma",
            "UNRESOLVED",
            "Requires semantic confirmation.",
        ),
        (
            "SynsetRecord.iast",
            "LexemeMetadata.transliteration",
            "CANDIDATE",
            "Potential transliteration mapping.",
        ),
        (
            "SynsetRecord.transliteration",
            "LexemeMetadata.transliteration",
            "CANDIDATE",
            "Potentially redundant with iast.",
        ),
        (
            "SynsetRecord.gloss",
            "SynsetMetadata.description",
            "CANDIDATE",
            "Could represent semantic description, but source semantics must be verified.",
        ),
        (
            "SynsetRecord.lexeme_ids",
            "Synset.lexemes",
            "RELATION",
            "Requires resolution of Lexeme identifiers to Lexeme objects.",
        ),
        (
            "VargaRecord.identifier",
            "Varga.identifier",
            "DIRECT",
            "Same source identity boundary.",
        ),
        (
            "VargaRecord.kanda",
            "VargaMetadata.kanda",
            "DIRECT",
            "Same structural dimension.",
        ),
        (
            "VargaRecord.varga_number",
            "VargaMetadata.varga_number",
            "DIRECT",
            "Same structural ordering.",
        ),
        (
            "VargaRecord.name",
            "VargaMetadata.name",
            "DIRECT",
            "Existing domain field.",
        ),
        (
            "VargaRecord.title",
            "VargaMetadata.title",
            "DIRECT",
            "Existing domain field.",
        ),
        (
            "VargaRecord.devanagari",
            "VargaMetadata.devanagari",
            "DIRECT",
            "Existing domain field.",
        ),
        (
            "VargaRecord.iast",
            "VargaMetadata.iast",
            "DIRECT",
            "Existing domain field.",
        ),
        (
            "VargaRecord.transliteration",
            "VargaMetadata.transliteration",
            "DIRECT",
            "Existing domain field.",
        ),
        (
            "VargaRecord.description",
            "VargaMetadata.description",
            "DIRECT",
            "Existing domain field.",
        ),
    ]

    header = (
        f"{'RECORD FIELD':<34} | "
        f"{'DOMAIN TARGET':<32} | "
        f"{'STATUS':<12} | "
        f"RATIONALE"
    )

    print(header)
    print("-" * len(header))

    for source, target, status, rationale in rows:
        print(
            f"{source:<34} | "
            f"{target:<32} | "
            f"{status:<12} | "
            f"{rationale}"
        )

    # -------------------------------------------------------------
    # 6. Importer contract
    # -------------------------------------------------------------

    section("6. IMPORTER BOUNDARY")

    show_signature(
        "AmarakoshaImporter",
        AmarakoshaImporter,
    )
    show_class_hierarchy(
        "AmarakoshaImporter",
        AmarakoshaImporter,
    )
    show_public_methods(
        "AmarakoshaImporter",
        AmarakoshaImporter,
    )

    inspect_method(
        "AmarakoshaImporter",
        AmarakoshaImporter,
        "__init__",
    )

    inspect_method(
        "AmarakoshaImporter",
        AmarakoshaImporter,
        "import_source",
    )

    print()
    print(
        "Importer dependency boundary:"
    )
    print(
        "  parser  : AmarakoshaParser"
    )
    print(
        "  registry: AmarakoshaRegistry"
    )

    # -------------------------------------------------------------
    # 7. Registry contract
    # -------------------------------------------------------------

    section("7. REGISTRY BOUNDARY")

    show_signature(
        "AmarakoshaRegistry",
        AmarakoshaRegistry,
    )
    show_class_hierarchy(
        "AmarakoshaRegistry",
        AmarakoshaRegistry,
    )
    show_public_methods(
        "AmarakoshaRegistry",
        AmarakoshaRegistry,
    )

    for method_name in (
        "register",
        "register_many",
        "get",
        "exists",
        "remove",
        "clear",
        "values",
        "items",
        "vargas",
        "synsets",
    ):
        inspect_method(
            "AmarakoshaRegistry",
            AmarakoshaRegistry,
            method_name,
        )

    # -------------------------------------------------------------
    # 8. Boundary graph
    # -------------------------------------------------------------

    section("8. CURRENT RUNTIME BOUNDARY GRAPH")

    print(
        "CURRENT:"
    )
    print(
        "  Source"
    )
    print(
        "    ↓"
    )
    print(
        "  AmarakoshaParser"
    )
    print(
        "    ↓"
    )
    print(
        "  SynsetRecord / VargaRecord"
    )
    print(
        "    ↓"
    )
    print(
        "  AmarakoshaImporter"
    )
    print(
        "    ↓"
    )
    print(
        "  [BUILDER INTEGRATION MISSING]"
    )
    print(
        "    ↓"
    )
    print(
        "  [REGISTRATION MISSING]"
    )

    print()
    print(
        "INTENDED:"
    )
    print(
        "  Source"
    )
    print(
        "    ↓"
    )
    print(
        "  AmarakoshaParser"
    )
    print(
        "    ↓"
    )
    print(
        "  SynsetRecord / VargaRecord"
    )
    print(
        "    ↓"
    )
    print(
        "  Builder"
    )
    print(
        "    ↓"
    )
    print(
        "  Synset / Varga"
    )
    print(
        "    ↓"
    )
    print(
        "  AmarakoshaRegistry"
    )

    # -------------------------------------------------------------
    # 9. Architectural observations
    # -------------------------------------------------------------

    section("9. ARCHITECTURAL OBSERVATIONS")

    observations = [
        (
            "O1",
            "SynsetBuilder already owns identifier, metadata, lexeme collection, "
            "and build() construction of Synset.",
        ),
        (
            "O2",
            "VargaBuilder already owns identifier, metadata, synset collection, "
            "and build() construction of Varga.",
        ),
        (
            "O3",
            "Both concrete builders are nevertheless abstract because "
            "_create_instance remains inherited and abstract.",
        ),
        (
            "O4",
            "This creates a mismatch between the apparent fluent builder "
            "implementation and the inherited abstract contract.",
        ),
        (
            "O5",
            "AmarakoshaImporter already receives parser and registry, making it "
            "the natural orchestration point for record-to-domain construction.",
        ),
        (
            "O6",
            "Registry already exposes separate synsets() and vargas() views, "
            "indicating that Synset and Varga are intended registry objects.",
        ),
        (
            "O7",
            "No evidence in this audit justifies creating a second Amarakośa "
            "domain construction abstraction.",
        ),
        (
            "O8",
            "No evidence justifies bypassing Synset/Varga and adapting raw "
            "records directly into canonical objects.",
        ),
        (
            "O9",
            "Lexeme resolution is the main unresolved runtime dependency "
            "inside Synset construction.",
        ),
    ]

    for number, observation in observations:
        print(f"{number}: {observation}")

    # -------------------------------------------------------------
    # 10. Decision gate
    # -------------------------------------------------------------

    section("10. BATCH 5C DECISION GATE")

    print(
        "PRELIMINARY ARCHITECTURAL DIRECTION:"
    )
    print()
    print(
        "  COMPLETE THE EXISTING AMARAKOSHA RECORD → DOMAIN BOUNDARY"
    )
    print(
        "  BEFORE IMPLEMENTING THE CANONICAL ADAPTER."
    )

    print()
    print("However, do NOT implement yet.")

    print()
    print("Batch 5D must first perform a runtime construction probe for:")
    print("  1. BaseAmarakoshaBuilder contract.")
    print("  2. _create_instance() requirements.")
    print("  3. SynsetBuilder construction.")
    print("  4. VargaBuilder construction.")
    print("  5. Lexeme construction from existing metadata.")
    print("  6. Registry registration.")
    print("  7. Record → builder data transfer feasibility.")

    print()
    print(
        "ADAPTER STATUS: BLOCKED"
    )

    print()
    print(
        "No production files were modified by this audit."
    )

    section("BATCH 5C COMPLETE")


if __name__ == "__main__":
    main()
