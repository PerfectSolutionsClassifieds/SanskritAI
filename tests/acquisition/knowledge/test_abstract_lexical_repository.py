import pytest
from SanskritAI.acquisition.knowledge.abstract_lexical_repository import (
    AbstractLexicalRepository,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexical_record import (
    CanonicalLexicalRecord,
)

# ---------------------------------------------------------------------------
# Test implementation
# ---------------------------------------------------------------------------

class DummyRepository(AbstractLexicalRepository):
    """Minimal in-memory repository used to exercise the abstract repository contract and its concrete helper methods."""

    def __init__(
        self,
        repository_name: str = "Test Repository",
        repository_version: str = "1.0.0",
    ) -> None:
        super().__init__(
            repository_name=repository_name,
            repository_version=repository_version,
        )
        self._records = []

    def add(
        self,
        record: CanonicalLexicalRecord,
    ) -> None:
        self._records.append(record)

    def get(
        self,
        headword: str,
    ) -> tuple[CanonicalLexicalRecord, ...]:
        return tuple(
            record for record in self._records if record.headword == headword
        )

    def contains(
        self,
        headword: str,
    ) -> bool:
        return bool(self.get(headword))

    def all(
        self,
    ) -> tuple[CanonicalLexicalRecord, ...]:
        return tuple(self._records)

    def clear(
        self,
    ) -> None:
        self._records.clear()

    @property
    def count(
        self,
    ) -> int:
        return len(self._records)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_repository(**overrides):
    values = {
        "repository_name": "Test Repository",
    }
    values.update(overrides)
    return DummyRepository(**values)


def make_record(
    headword: str = "राम",
):
    """Create a minimal CanonicalLexicalRecord using its actual constructor.

    The test intentionally discovers the model contract through the repository-facing ``headword`` field.
    """
    return CanonicalLexicalRecord(
        headword=headword,
    )


# ---------------------------------------------------------------------------
# Abstract contract
# ---------------------------------------------------------------------------

def test_abstract_repository_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AbstractLexicalRepository(
            repository_name="Test Repository",
        )


def test_concrete_repository_can_be_instantiated():
    repository = make_repository()
    assert isinstance(repository, AbstractLexicalRepository)


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

def test_repository_name_is_preserved():
    repository = make_repository(
        repository_name="Canonical Lexical Repository",
    )
    assert repository.repository_name == (
        "Canonical Lexical Repository"
    )


def test_default_repository_version_is_applied():
    repository = make_repository()
    assert repository.repository_version == "1.0.0"


def test_custom_repository_version_is_preserved():
    repository = make_repository(
        repository_version="2.0.0",
    )
    assert repository.repository_version == "2.0.0"


def test_identifier_alias_returns_repository_name():
    repository = make_repository(
        repository_name="Canonical",
    )
    assert repository.identifier == "Canonical"


# ---------------------------------------------------------------------------
# Insert
# ---------------------------------------------------------------------------

def test_add_inserts_one_record():
    repository = make_repository()
    record = make_record()

    repository.add(record)

    assert repository.count == 1
    assert repository.all() == (record,)


def test_add_all_inserts_every_record():
    repository = make_repository()

    records = (
        make_record("राम"),
        make_record("हरि"),
        make_record("कृष्ण"),
    )

    repository.add_all(records)

    assert repository.count == 3
    assert repository.all() == records


def test_add_all_accepts_any_iterable():
    repository = make_repository()

    records = [
        make_record("राम"),
        make_record("हरि"),
    ]

    repository.add_all(
        record for record in records
    )

    assert repository.all() == tuple(records)


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def test_get_returns_matching_headword_records():
    repository = make_repository()

    ram_1 = make_record("राम")
    hari = make_record("हरि")
    ram_2 = make_record("राम")

    repository.add_all(
        [
            ram_1,
            hari,
            ram_2,
        ]
    )

    result = repository.get("राम")

    assert result == (
        ram_1,
        ram_2,
    )


def test_get_returns_empty_tuple_for_missing_headword():
    repository = make_repository()

    repository.add(
        make_record("राम"),
    )

    assert repository.get("हरि") == ()


def test_contains_is_true_for_existing_headword():
    repository = make_repository()

    repository.add(
        make_record("राम"),
    )

    assert repository.contains("राम") is True


def test_contains_is_false_for_missing_headword():
    repository = make_repository()

    repository.add(
        make_record("राम"),
    )

    assert repository.contains("हरि") is False


def test_all_returns_all_records_in_insertion_order():
    repository = make_repository()

    records = (
        make_record("राम"),
        make_record("हरि"),
        make_record("कृष्ण"),
    )

    repository.add_all(records)

    assert repository.all() == records


# ---------------------------------------------------------------------------
# Maintenance
# ---------------------------------------------------------------------------

def test_clear_removes_all_records():
    repository = make_repository()

    repository.add_all(
        [
            make_record("राम"),
            make_record("हरि"),
        ]
    )

    repository.clear()

    assert repository.count == 0
    assert repository.all() == ()


def test_clear_on_empty_repository_is_safe():
    repository = make_repository()
    repository.clear()
    assert repository.count == 0


# ---------------------------------------------------------------------------
# Enumeration
# ---------------------------------------------------------------------------

def test_iteration_delegates_to_all():
    repository = make_repository()

    records = (
        make_record("राम"),
        make_record("हरि"),
    )

    repository.add_all(records)

    assert tuple(repository) == records


def test_len_delegates_to_count():
    repository = make_repository()

    repository.add_all(
        [
            make_record("राम"),
            make_record("हरि"),
        ]
    )

    assert len(repository) == 2


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------

def test_summary_contains_repository_diagnostics():
    repository = make_repository(
        repository_name="Canonical",
        repository_version="2.0.0",
    )

    repository.add_all(
        [
            make_record("राम"),
            make_record("हरि"),
        ]
    )

    assert repository.summary() == {
        "repository": "Canonical",
        "version": "2.0.0",
        "records": 2,
    }


def test_string_representation_contains_record_count():
    repository = make_repository()

    repository.add(
        make_record("राम"),
    )

    assert str(repository) == (
        "DummyRepository(records=1)"
    )

