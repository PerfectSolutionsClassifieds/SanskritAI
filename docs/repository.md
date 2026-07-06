# SanskritAI v0.3.0 Final

# Repository Architecture

**Version:** v0.3.0 Final

**Status:** Stable

**Document Type:** Architecture Specification

---

# 1. Introduction

The Repository Layer provides the storage abstraction for SanskritAI.

Rather than allowing analysis engines, parsers, translators, or AI components to directly manipulate storage, all interactions with persistent lexical data occur through repository interfaces.

This separation ensures that the domain model remains independent of storage technology.

Whether lexical data is stored in memory, JSON files, PostgreSQL, Neo4j, MongoDB, or any future backend, the remainder of the SanskritAI platform continues to interact with the same public API.

---

# 2. Objectives

The Repository Layer was designed to satisfy several long-term architectural goals.

- Separate storage from domain logic.
- Support multiple interchangeable storage backends.
- Enable efficient indexing and retrieval.
- Centralize object lifecycle management.
- Preserve canonical lexical identities.
- Facilitate unit testing without requiring external databases.
- Allow future migration to enterprise-scale storage systems without altering higher-level modules.

---

# 3. Why a Repository?

Without a repository, application code tends to become tightly coupled to storage implementations.

For example:

```
Tokenizer

↓

Database Query

↓

Lexeme
```

This approach spreads storage logic throughout the application, making future changes difficult.

Instead, SanskritAI adopts the Repository Pattern.

```
Tokenizer

↓

Repository

↓

Storage Backend
```

The tokenizer never knows whether data comes from memory, PostgreSQL, or Neo4j.

---

# 4. Repository Pattern

The Repository Pattern provides a collection-like interface for domain objects.

Application components request objects from the repository rather than directly querying storage.

```
Analysis Engine

↓

Lexical Repository

↓

Lexeme
```

The repository becomes the single authority responsible for object retrieval and persistence.

---

# 5. Repository Hierarchy

The lexical repository architecture consists of three principal components.

```
LexicalRepositoryBase

↓

MemoryLexicalRepository

↓

Future Storage Backends
```

Repository creation is centralized through the factory.

```
LexicalRepositoryFactory

↓

Concrete Repository
```

---

# 6. Repository Interface

The abstract repository defines the public contract shared by every storage implementation.

Primary operations include:

```
add()

update()

remove()

clear()

get()

by_lemma()

by_transliteration()

by_dictionary()

all()
```

Every backend must implement the same behavior.

---

# 7. LexicalRepositoryBase

LexicalRepositoryBase is an abstract interface.

It contains no storage logic.

Its responsibility is to define the operations available to the rest of the platform.

Example:

```
repository.add(lexeme)

repository.get("LEX0001")

repository.by_lemma("राम")

repository.by_dictionary(
    DictionarySource.AMARAKOSHA,
    "राम"
)
```

All concrete repositories must satisfy this contract.

---

# 8. MemoryLexicalRepository

The default implementation in v0.3.0 is the in-memory repository.

This implementation is optimized for:

- development
- unit testing
- Google Colab
- notebooks
- small and medium lexical datasets

The repository stores Lexeme objects in Python collections while maintaining several internal indexes for efficient lookup.

---

# 9. Internal Indexes

To support efficient retrieval, the memory repository maintains multiple indexes.

```
Primary Index

Lexeme ID

↓

Lexeme
```

```
Lemma Index

Lemma

↓

Lexeme ID
```

```
Transliteration Index

Transliteration

↓

Lexeme ID
```

```
Dictionary Index

DictionarySource

↓

Headword

↓

Lexeme ID
```

These indexes provide near constant-time lookup for common operations.

---

# 10. Index Management

Indexes are managed internally.

The repository exposes two internal helper methods.

```
_index_lexeme()

_deindex_lexeme()
```

These methods ensure that every index remains synchronized whenever Lexeme objects are added, updated, or removed.

Application code never manipulates indexes directly.

---

# 11. Repository Lifecycle

Adding a Lexeme follows the sequence:

```
Lexeme

↓

Validation

↓

Primary Index

↓

Secondary Indexes

↓

Repository
```

Removing a Lexeme performs the reverse sequence, ensuring that all indexes remain consistent.

---

# 12. Lookup Operations

The repository supports several lookup strategies.

### By Lexeme ID

```
repository.get("LEX0001")
```

---

### By Lemma

```
repository.by_lemma("राम")
```

---

### By Transliteration

```
repository.by_transliteration("rāma")
```

---

### By Dictionary

```
repository.by_dictionary(
    DictionarySource.AMARAKOSHA,
    "राम"
)
```

Each lookup returns the canonical Lexeme object.

---

# 13. Dictionary Management

Dictionary entries are attached to Lexeme objects through the repository.

Example:

```
repository.add_dictionary_entry(
    lexeme_id,
    dictionary_entry
)
```

The repository updates both the Lexeme and the relevant dictionary indexes.

---

# 14. Repository Factory

Repositories are never instantiated directly by application code.

Instead, they are created through the factory.

```
repository = LexicalRepositoryFactory.create()
```

This approach allows storage implementations to be changed through configuration rather than code modifications.

---

# 15. Supported Backends

Current implementation:

```
Memory Repository
```

Planned implementations:

```
JSON Repository

PostgreSQL Repository

Neo4j Repository

MongoDB Repository

Redis Repository
```

Each backend will implement the same public interface.

---

# 16. Configuration

The repository factory selects the backend according to application configuration.

Example:

```
Config

↓

LEXICAL_REPOSITORY

↓

Factory

↓

Repository
```

Changing storage technology requires only a configuration change.

---

# 17. Object Ownership

The repository owns all registered Lexeme instances.

Analysis components should not maintain independent collections of Lexeme objects.

Instead:

```
Repository

↓

Canonical Lexeme

↓

Analysis Components
```

This guarantees object consistency throughout the application.

---

# 18. Serialization

Repositories provide serialization support.

```
Repository

↓

Lexeme

↓

DictionaryEntry

↓

DictionarySense

↓

Dictionary
```

Future backends may serialize directly to:

- JSON
- SQL records
- graph databases
- document stores

without altering the domain model.

---

# 19. Benefits of the Architecture

The Repository Layer provides several important advantages.

## Storage Independence

Domain objects remain unaware of storage implementation.

---

## Testability

Unit tests can execute entirely in memory without requiring external databases.

---

## Performance

Internal indexes provide efficient retrieval for frequent lookup operations.

---

## Maintainability

Storage logic is centralized in one location rather than scattered throughout the application.

---

## Extensibility

New storage technologies can be introduced by implementing the repository interface.

---

# 20. Future Roadmap

The repository architecture is intended to evolve with the SanskritAI platform.

Planned enhancements include:

- JSON persistence
- PostgreSQL persistence
- Neo4j graph storage
- MongoDB document storage
- Redis caching
- transaction support
- asynchronous repositories
- distributed repositories
- repository statistics
- query optimization
- batch operations
- lazy loading
- change tracking
- audit logging

These features can be introduced without modifying application logic because the public repository interface remains stable.

---

# 21. Design Principles

The Repository Layer follows several well-established software engineering principles.

## Repository Pattern

Separates domain logic from storage.

---

## Factory Pattern

Centralizes repository creation.

---

## Dependency Inversion Principle

Application code depends on abstractions rather than concrete implementations.

---

## Single Responsibility Principle

Repositories manage storage.

Domain objects represent Sanskrit knowledge.

Analysis engines perform linguistic computation.

Each component has one clearly defined responsibility.

---

# 22. Integration with SanskritAI

The Repository Layer occupies a central position within the overall architecture.

```
AI Components

↓

Services

↓

Repositories

↓

Lexical Objects

↓

Storage
```

All lexical data flows through the repository before reaching higher-level analysis engines.

---

# 23. Version History

## v0.3.0 Final

Initial repository architecture.

Features include:

- LexicalRepositoryBase
- MemoryLexicalRepository
- LexicalRepositoryFactory
- Primary and secondary indexes
- Repository serialization
- Configuration-driven backend selection
- Comprehensive unit testing

This architecture establishes the storage foundation for all future SanskritAI development.
