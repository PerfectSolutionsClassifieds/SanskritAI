
from pathlib import Path


ROOT = Path("/content/SanskritAI")
OUTPUT = ROOT / "_audit" / "amarakosha_batch5_mapping_matrix.md"

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


HEADER = """# Amarakośa → Canonical Knowledge Mapping Matrix

Status: REVIEW ONLY

This document must be populated from the Batch 4 Amarakośa
implementation audit.

No production implementation should be created merely because
a row exists in this matrix.

## Canonical targets

- CanonicalSource
- CanonicalContext
- CanonicalDictionaryEntry
- CanonicalDictionarySense
- CanonicalLexicon
- CanonicalKnowledgeRepository

## Mapping matrix

| # | Amarakośa concept | Existing Amarakośa type / field | Existing owner | Canonical target | Mapping rule | Transformation | Provenance preserved? | Lossless? | Confidence | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Synset | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |
| 2 | Synonym | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |
| 3 | Varga | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |
| 4 | Varga hierarchy | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |
| 5 | Gloss / meaning | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |
| 6 | Sanskrit headword | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |
| 7 | Transliteration | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |
| 8 | Source / edition | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |
| 9 | Verse / citation | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |
| 10 | Grammatical information | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |
| 11 | Metadata | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |
| 12 | Relationships | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | REVIEW |

## Architecture questions

### A. Source ownership

Does the existing Amarakośa source metadata map to:

`CanonicalSource`

or is an existing source model already the correct owner?

Decision:

`TBD`

### B. Synset ownership

Does an Amarakośa `Synset` represent:

- one `CanonicalDictionaryEntry`,
- one `CanonicalDictionarySense`,
- a group of canonical entries,
- or a canonical context/relationship structure?

Decision:

`TBD`

### C. Varga ownership

Does `Varga` represent:

- source organization,
- semantic context,
- hierarchical taxonomy,
- citation metadata,
- or a combination?

Decision:

`TBD`

### D. Synonym relationships

Determine whether synonym membership should become:

- multiple canonical dictionary entries,
- lexical relations,
- sense-level metadata,
- or remain Amarakośa-specific source metadata.

Decision:

`TBD`

### E. Provenance

Every mapping must answer:

1. Can the original Amarakośa source be identified?
2. Can the original source record be identified?
3. Can the original Varga/Synset location be recovered?
4. Can the original citation/reference be recovered?

Decision:

`TBD`

### F. Information loss

For every Amarakośa field not mapped into a canonical field:

- determine whether it is redundant,
- provenance,
- source-specific metadata,
- semantic information,
- or genuinely unsupported by the canonical model.

Do not discard information merely because no obvious canonical field exists.

Decision:

`TBD`

## Implementation gate

The Amarakośa canonical adapter must NOT be implemented until:

- [ ] Batch 4A complete
- [ ] Batch 4B complete
- [ ] Batch 4C complete
- [ ] all active Amarakośa production types identified
- [ ] actual construction path identified
- [ ] repository/registry ownership identified
- [ ] Synset semantics established
- [ ] Varga semantics established
- [ ] source/provenance mapping established
- [ ] information-loss decisions documented
- [ ] canonical target mapping reviewed
"""


OUTPUT.write_text(
    HEADER,
    encoding="utf-8",
)

print("=" * 80)
print("BATCH 5 — AMARAKOSHA MAPPING MATRIX SCAFFOLD")
print("=" * 80)
print()
print(f"Created: {OUTPUT}")
print()
print("This is a review artifact only.")
print("No production code has been changed.")
