# SanskritAI v0.3.0 Final

# Lexical Layer Architecture

**Version:** v0.3.0 Final

**Status:** Stable

**Document Type:** Architecture Specification

---

# 1. Introduction

The Lexical Layer is the canonical representation of words within the SanskritAI platform.

Every textual source—whether from the Vedas, Upaniṣads, Purāṇas, Itihāsas, Kāvyas, dictionaries, or user input—is ultimately normalized into a collection of **Lexeme** objects.

Rather than treating every inflected form as an independent object, SanskritAI models language around canonical lexical identities.

For example,

```
रामः
रामम्
रामेण
रामस्य
रामे
```

all represent grammatical realizations of the same lexical concept:

```
Lexeme("राम")
```

The lexical layer therefore provides a stable semantic identity independent of grammatical variation.

---

# 2. Design Goals

The lexical layer was designed according to the following principles.

## Canonical Identity

Every lexical concept exists exactly once.

Multiple dictionary entries, grammatical analyses, and corpus occurrences all reference the same Lexeme.

---

## Dictionary Independence

A Lexeme does not belong to any one dictionary.

Instead,

```
Lexeme

├── Amarakośa
├── Monier-Williams
├── Apte
├── Vācaspatyam
├── Śabdakalpadruma
└── User Dictionary
```

Each dictionary contributes information without becoming the owner of the lexical object.

---

## Extensibility

New dictionaries can be added without modifying existing code.

Likewise,

- new relation types
- additional metadata
- future linguistic annotations

can all be introduced without redesigning the architecture.

---

## Fast Lookup

The object model supports efficient lookup through internal indexes.

Examples include

- dictionary source
- lexical ID
- transliteration
- lemma

The implementation aims for O(1) access wherever practical.

---

# 3. Core Objects

The lexical layer consists of four principal classes.

```
Lexeme

DictionaryEntry

DictionarySense

LexicalRelation
```

These four classes form the canonical lexical model.

---

# 4. Lexeme

## Purpose

Lexeme represents one canonical lexical unit.

Everything else in SanskritAI ultimately resolves to a Lexeme.

Examples include

```
राम

गम्

अग्नि

ब्रह्म

धर्म
```

A Lexeme is **not** an inflected word.

It represents the abstract lexical identity.

---

## Primary Fields

```
lexeme_id

lemma

language

script

transliteration

etymology

notes
```

---

## Collections

A Lexeme owns two principal collections.

```
dictionary_entries

relations
```

---

## Internal Indexes

To improve lookup performance, every Lexeme maintains an internal dictionary index.

```
DictionarySource

↓

DictionaryEntry
```

This allows retrieval of dictionary entries in constant time.

Example:

```
lexeme.get_entry(
    DictionarySource.AMARAKOSHA
)
```

---

# 5. DictionaryEntry

A DictionaryEntry represents one lexical record originating from a single dictionary.

For example,

```
Lexeme("राम")

↓

Amarakośa

↓

DictionaryEntry
```

and

```
Lexeme("राम")

↓

Monier-Williams

↓

DictionaryEntry
```

are two independent DictionaryEntry objects attached to the same Lexeme.

---

## Identity

A DictionaryEntry is uniquely identified by

```
entry_id
```

and

```
DictionarySource
```

---

## Contents

Each DictionaryEntry contains

```
headword

source

senses

references

notes
```

---

# 6. DictionarySense

One dictionary entry may contain several meanings.

Each meaning is represented by a DictionarySense.

Example

```
अग्नि

↓

Fire

↓

Sacrificial Fire

↓

Vedic Deity

↓

Digestive Fire
```

Each of the above meanings is represented by an independent DictionarySense.

---

## Contents

```
sense_id

definition

language

examples

notes
```

---

# 7. LexicalRelation

LexicalRelation represents semantic relationships between Lexemes.

Examples include

```
Synonym

Antonym

Derived From

Variant

Related

Parent

Child
```

The actual relation categories are defined by

```
RelationType
```

---

## ID-Based References

Relations store

```
target_lexeme_id
```

rather than textual references.

This guarantees stable links regardless of dictionary wording.

---

# 8. Enumerations

The lexical layer relies upon the shared enum package.

Important enums include

```
Language

Script

DictionarySource

RelationType
```

These enums are shared throughout SanskritAI.

No duplicate enum definitions should exist inside the lexical package.

---

# 9. Repository Integration

Lexeme objects are never managed directly by analysis engines.

Instead they are stored within a repository.

```
Analysis

↓

Repository

↓

Lexeme
```

The repository provides

- indexing
- searching
- updates
- persistence

without exposing storage details.

---

# 10. Object Relationships

```
                 Lexeme
                    │
     ┌──────────────┴──────────────┐
     │                             │
DictionaryEntry             LexicalRelation
     │
     │
DictionarySense
```

This hierarchy represents the complete lexical object model.

---

# 11. Serialization

Every lexical object supports serialization.

```
Lexeme

↓

DictionaryEntry

↓

DictionarySense

↓

dict
```

This enables future storage in

- JSON
- PostgreSQL
- Neo4j
- MongoDB

without modifying the object model.

---

# 12. Architectural Principles

The lexical layer follows several established software engineering principles.

## Single Responsibility Principle

Each class has one clearly defined purpose.

---

## Repository Pattern

Storage is separated from the domain model.

---

## Factory Pattern

Repositories are created through a factory rather than direct instantiation.

---

## Canonical Identity

Every lexical concept exists only once.

---

## Strong Typing

Enums replace raw strings wherever practical.

---

## Internal Indexing

Frequently accessed information is indexed for performance.

---

# 13. Example Workflow

```
User Input

↓

Tokenizer

↓

Morphology

↓

Canonical Lemma

↓

Lexeme

↓

Dictionary Entries

↓

Dictionary Senses

↓

AI Explanation
```

Every analysis pipeline eventually converges on the canonical Lexeme.

---

# 14. Future Extensions

The lexical layer has been designed to accommodate future enhancements without breaking compatibility.

Planned extensions include:

- Amarakośa integration
- Dhātupāṭha integration
- Monier-Williams dictionary import
- Apte dictionary import
- Vācaspatyam import
- Śabdakalpadruma import
- multilingual glosses
- semantic graphs
- ontology support
- Neo4j graph storage
- corpus frequency statistics
- lexical embeddings
- AI-assisted semantic search

---

# 15. Version History

## v0.3.0 Final

Initial stable implementation of the canonical lexical layer.

Features include:

- Lexeme
- DictionaryEntry
- DictionarySense
- LexicalRelation
- RelationType
- DictionarySource
- Repository abstraction
- Memory repository
- Repository factory
- Serialization support
- Comprehensive unit tests

This version establishes the lexical foundation upon which all future SanskritAI modules will be built.
