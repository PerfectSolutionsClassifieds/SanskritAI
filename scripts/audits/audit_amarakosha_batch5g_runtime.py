from __future__ import annotations

"""
BATCH 5G — AMARAKOSHA RUNTIME REPAIR VERIFICATION

Read-only verification of the minimal Synset/Varga and Builder repair.

This audit does not modify production files.
"""

from SanskritAI.amarakosha.builders.synset_builder import SynsetBuilder
from SanskritAI.amarakosha.builders.varga_builder import VargaBuilder
from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.models.synset_metadata import SynsetMetadata
from SanskritAI.amarakosha.models.varga import Varga
from SanskritAI.amarakosha.models.varga_metadata import VargaMetadata
from SanskritAI.domain.lexical.lexeme import Lexeme


def section(title: str) -> None:
    print()
    print("-" * 100)
    print(title)
    print("-" * 100)


print("=" * 110)
print("BATCH 5G — AMARAKOSHA RUNTIME REPAIR VERIFICATION")
print("=" * 110)


section("1. DIRECT SYNSET CONSTRUCTION")

synset = Synset(
    identifier="synset:test:1",
    metadata=SynsetMetadata(
        title="Test Synset",
    ),
)

print("Synset:", synset)
print("Identifier:", synset.identifier)
print("Child count:", len(synset.children))


section("2. DIRECT VARGA CONSTRUCTION")

varga = Varga(
    identifier="varga:test:1",
    metadata=VargaMetadata(
        title="Test Varga",
    ),
)

print("Varga:", varga)
print("Identifier:", varga.identifier)
print("Child count:", len(varga.children))


section("3. SYNSET CHILD POPULATION")

lexeme_1 = Lexeme(
    identifier="lexeme:test:1",
    lemma="हरि",
    language="sanskrit",
    script="devanagari",
    transliteration="hari",
)

lexeme_2 = Lexeme(
    identifier="lexeme:test:2",
    lemma="विष्णु",
    language="sanskrit",
    script="devanagari",
    transliteration="viṣṇu",
)

synset_with_children = Synset(
    identifier="synset:test:2",
    metadata=SynsetMetadata(
        title="Hari Synset",
    ),
    children=[lexeme_1, lexeme_2],
)

print("Synset child count:", len(synset_with_children.children))
print(
    "Child identifiers:",
    [child.identifier for child in synset_with_children.children],
)


section("4. VARGA CHILD POPULATION")

varga_with_children = Varga(
    identifier="varga:test:2",
    metadata=VargaMetadata(
        title="Test Varga",
    ),
    children=[synset_with_children],
)

print("Varga child count:", len(varga_with_children.children))
print(
    "Child identifiers:",
    [child.identifier for child in varga_with_children.children],
)


section("5. SYNSET BUILDER")

synset_builder = SynsetBuilder()

print("Instantiated:", True)
print("Abstract methods:", getattr(SynsetBuilder, "__abstractmethods__", None))

built_synset = (
    synset_builder
    .with_identifier("synset:builder:1")
    .add_lexeme(lexeme_1)
    .add_lexeme(lexeme_2)
    .build()
)

print("Built identifier:", built_synset.identifier)
print("Built child count:", len(built_synset.children))


section("6. VARGA BUILDER")

varga_builder = VargaBuilder()

print("Instantiated:", True)
print("Abstract methods:", getattr(VargaBuilder, "__abstractmethods__", None))

built_varga = (
    varga_builder
    .with_identifier("varga:builder:1")
    .add_synset(built_synset)
    .build()
)

print("Built identifier:", built_varga.identifier)
print("Built child count:", len(built_varga.children))


section("7. BUILDER ISOLATION")

synset_builder_2 = (
    SynsetBuilder()
    .with_identifier("synset:builder:2")
    .add_lexeme(lexeme_1)
)

built_a = synset_builder_2.build()

synset_builder_2.add_lexeme(lexeme_2)

built_b = synset_builder_2.build()

print("First build child count:", len(built_a.children))
print("Second build child count:", len(built_b.children))

assert len(built_a.children) == 1
assert len(built_b.children) == 2


section("8. DECISION GATE")

assert len(synset.children) == 0
assert len(varga.children) == 0

assert len(synset_with_children.children) == 2
assert len(varga_with_children.children) == 1

assert len(built_synset.children) == 2
assert len(built_varga.children) == 1

assert not getattr(SynsetBuilder, "__abstractmethods__", None)
assert not getattr(VargaBuilder, "__abstractmethods__", None)

print("Synset construction       : PASS")
print("Varga construction        : PASS")
print("Synset child population   : PASS")
print("Varga child population    : PASS")
print("SynsetBuilder runtime     : PASS")
print("VargaBuilder runtime      : PASS")
print("Builder isolation         : PASS")

print()
print("BATCH 5G — DECISION GATE: PASS")
print("NEXT: Verify SynsetRecordBuilder -> Synset runtime construction.")
print()
