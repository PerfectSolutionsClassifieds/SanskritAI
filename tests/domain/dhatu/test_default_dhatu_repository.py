from __future__ import annotations

import pytest

from SanskritAI.domain.dhatu.default_dhatu_repository import (
    DefaultDhatuRepository,
)
from SanskritAI.domain.dhatu.dhatu import Dhatu
from SanskritAI.domain.dhatu.dhatu_gana import (
    BVADI,
    TUDADI,
)


def make_dhatu(
    identifier: str,
    root: str,
    gana=None,
    transliteration: str = "",
    meaning: str = "",
    notes: str = "",
) -> Dhatu:
    return Dhatu(
        identifier=identifier,
        root=root,
        transliteration=transliteration,
        meaning=meaning,
        gana=gana,
        notes=notes,
    )


class TestDefaultDhatuRepository:

    def test_can_be_created_empty(self):
        repository = DefaultDhatuRepository()

        assert repository is not None
        assert repository.count == 0
        assert len(repository) == 0

    def test_accepts_initial_dhatus(self):
        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
            gana=BVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        assert repository.count == 1
        assert repository.get("gam") is dhatu

    def test_get_unknown_returns_none(self):
        repository = DefaultDhatuRepository()

        assert repository.get("unknown") is None

    def test_contains_identifier(self):
        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
            gana=BVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        assert repository.contains("gam")
        assert "gam" in repository
        assert not repository.contains("unknown")

    def test_find_by_root(self):
        first = make_dhatu(
            identifier="gam",
            root="गम्",
            gana=BVADI,
        )

        second = make_dhatu(
            identifier="gam_alt",
            root="गम्",
            gana=TUDADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(first, second)
        )

        result = repository.find_by_root("गम्")

        assert result.count == 2
        assert first in result
        assert second in result

    def test_find_by_root_unknown_returns_empty(self):
        repository = DefaultDhatuRepository()

        result = repository.find_by_root("अज्ञात")

        assert result.is_empty

    def test_find_by_gana(self):
        first = make_dhatu(
            identifier="gam",
            root="गम्",
            gana=BVADI,
        )

        second = make_dhatu(
            identifier="bhu",
            root="भू",
            gana=BVADI,
        )

        third = make_dhatu(
            identifier="tud",
            root="तुद्",
            gana=TUDADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(first, second, third)
        )

        result = repository.find_by_gana(BVADI)

        assert result.count == 2
        assert first in result
        assert second in result
        assert third not in result

    def test_find_by_gana_unknown_returns_empty(self):
        repository = DefaultDhatuRepository()

        result = repository.find_by_gana(BVADI)

        assert result.is_empty

    def test_search_by_identifier(self):
        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
            gana=BVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        result = repository.search("gam")

        assert result.count == 1
        assert result.first is dhatu

    def test_search_by_root(self):
        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
            gana=BVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        result = repository.search("गम्")

        assert result.count == 1
        assert result.first is dhatu

    def test_search_by_transliteration(self):
        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
            transliteration="gam",
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        result = repository.search("gam")

        assert result.count == 1

    def test_search_by_meaning(self):
        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
            meaning="to go",
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        result = repository.search("go")

        assert result.count == 1

    def test_search_by_notes(self):
        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
            notes="movement",
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        result = repository.search("movement")

        assert result.count == 1

    def test_search_by_gana_name(self):
        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
            gana=BVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        result = repository.search("भ्वादि")

        assert result.count == 1

    def test_search_is_case_insensitive_for_latin_fields(self):
        dhatu = make_dhatu(
            identifier="GAM",
            root="गम्",
            transliteration="Gam",
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        result = repository.search("gam")

        assert result.count == 1

    def test_empty_search_returns_empty(self):
        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        assert repository.search("").is_empty

    def test_unknown_search_returns_empty(self):
        repository = DefaultDhatuRepository()

        assert repository.search("unknown").is_empty

    def test_all_returns_insertion_order(self):
        first = make_dhatu(
            identifier="gam",
            root="गम्",
            gana=BVADI,
        )

        second = make_dhatu(
            identifier="bhu",
            root="भू",
            gana=BVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(first, second)
        )

        result = repository.all()

        assert result.count == 2
        assert result[0] is first
        assert result[1] is second

    def test_register_adds_dhatu(self):
        repository = DefaultDhatuRepository()

        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
            gana=BVADI,
        )

        repository.register(dhatu)

        assert repository.count == 1
        assert repository.get("gam") is dhatu

    def test_register_replaces_same_identifier(self):
        first = make_dhatu(
            identifier="gam",
            root="गम्",
            gana=BVADI,
        )

        second = make_dhatu(
            identifier="gam",
            root="गम्",
            gana=TUDADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(first,)
        )

        repository.register(second)

        assert repository.count == 1
        assert repository.get("gam") is second

    def test_register_many(self):
        first = make_dhatu(
            identifier="gam",
            root="गम्",
        )

        second = make_dhatu(
            identifier="bhu",
            root="भू",
        )

        repository = DefaultDhatuRepository()

        repository.register_many(
            (first, second)
        )

        assert repository.count == 2

    def test_register_rejects_none(self):
        repository = DefaultDhatuRepository()

        with pytest.raises(ValueError):
            repository.register(None)

    def test_register_rejects_wrong_type(self):
        repository = DefaultDhatuRepository()

        with pytest.raises(TypeError):
            repository.register(object())

    def test_register_rejects_empty_identifier(self):
        repository = DefaultDhatuRepository()

        dhatu = make_dhatu(
            identifier="",
            root="गम्",
        )

        with pytest.raises(ValueError):
            repository.register(dhatu)

    def test_register_rejects_empty_root(self):
        repository = DefaultDhatuRepository()

        dhatu = make_dhatu(
            identifier="gam",
            root="",
        )

        with pytest.raises(ValueError):
            repository.register(dhatu)

    def test_remove_existing(self):
        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        assert repository.remove("gam") is True
        assert repository.count == 0
        assert repository.get("gam") is None

    def test_remove_unknown_returns_false(self):
        repository = DefaultDhatuRepository()

        assert repository.remove("unknown") is False

    def test_clear(self):
        dhatu = make_dhatu(
            identifier="gam",
            root="गम्",
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        repository.clear()

        assert repository.count == 0
        assert repository.all().is_empty
