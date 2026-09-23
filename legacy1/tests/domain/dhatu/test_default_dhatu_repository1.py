from __future__ import annotations

import pytest

from SanskritAI.domain.dhatu.default_dhatu_repository import (
    DefaultDhatuRepository,
)
from SanskritAI.domain.dhatu.dhatu import Dhatu
from SanskritAI.domain.dhatu.dhatu_gana import DhatuGana


def make_dhatu(
    identifier: str,
    root: str,
    gana: DhatuGana,
) -> Dhatu:
    return Dhatu(
        identifier=identifier,
        root=root,
        gana=gana,
    )


class TestDefaultDhatuRepository:

    def test_repository_can_be_created(self):
        repository = DefaultDhatuRepository()

        assert repository is not None
        assert repository.count == 0

    def test_repository_accepts_initial_dhatus(self):
        dhatu = make_dhatu(
            "gam",
            "गम्",
            DhatuGana.BHVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        assert repository.count == 1
        assert repository.get("gam") is dhatu

    def test_get_returns_none_for_unknown_identifier(self):
        repository = DefaultDhatuRepository()

        assert repository.get("unknown") is None

    def test_contains(self):
        dhatu = make_dhatu(
            "gam",
            "गम्",
            DhatuGana.BHVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        assert repository.contains("gam")
        assert "gam" in repository
        assert not repository.contains("unknown")

    def test_find_by_root(self):
        first = make_dhatu(
            "gam",
            "गम्",
            DhatuGana.BHVADI,
        )

        second = make_dhatu(
            "gam2",
            "गम्",
            DhatuGana.ADVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(first, second)
        )

        result = repository.find_by_root("गम्")

        assert result.count == 2
        assert first in result
        assert second in result

    def test_find_by_gana(self):
        first = make_dhatu(
            "gam",
            "गम्",
            DhatuGana.BHVADI,
        )

        second = make_dhatu(
            "bhu",
            "भू",
            DhatuGana.BHVADI,
        )

        third = make_dhatu(
            "kr",
            "कृ",
            DhatuGana.TUDADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(first, second, third)
        )

        result = repository.find_by_gana(
            DhatuGana.BHVADI
        )

        assert result.count == 2
        assert first in result
        assert second in result
        assert third not in result

    def test_search_by_identifier(self):
        dhatu = make_dhatu(
            "gam",
            "गम्",
            DhatuGana.BHVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        result = repository.search("gam")

        assert result.count == 1
        assert result.first is dhatu

    def test_search_by_root(self):
        dhatu = make_dhatu(
            "gam",
            "गम्",
            DhatuGana.BHVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        result = repository.search("गम्")

        assert result.count == 1
        assert result.first is dhatu

    def test_search_is_case_insensitive_for_identifier(self):
        dhatu = make_dhatu(
            "Gam",
            "गम्",
            DhatuGana.BHVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(dhatu,)
        )

        result = repository.search("gam")

        assert result.count == 1

    def test_search_unknown_returns_empty_collection(self):
        repository = DefaultDhatuRepository()

        result = repository.search("unknown")

        assert result.is_empty

    def test_all_returns_all_dhatus(self):
        first = make_dhatu(
            "gam",
            "गम्",
            DhatuGana.BHVADI,
        )

        second = make_dhatu(
            "bhu",
            "भू",
            DhatuGana.BHVADI,
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
            "gam",
            "गम्",
            DhatuGana.BHVADI,
        )

        repository.register(dhatu)

        assert repository.count == 1
        assert repository.get("gam") is dhatu

    def test_register_replaces_existing_identifier(self):
        first = make_dhatu(
            "gam",
            "गम्",
            DhatuGana.BHVADI,
        )

        second = make_dhatu(
            "gam",
            "गम्",
            DhatuGana.TUDADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(first,)
        )

        repository.register(second)

        assert repository.count == 1
        assert repository.get("gam") is second

    def test_register_rejects_none(self):
        repository = DefaultDhatuRepository()

        with pytest.raises(ValueError):
            repository.register(None)

    def test_register_rejects_wrong_type(self):
        repository = DefaultDhatuRepository()

        with pytest.raises(TypeError):
            repository.register(object())

    def test_remove_existing(self):
        dhatu = make_dhatu(
            "gam",
            "गम्",
            DhatuGana.BHVADI,
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
        first = make_dhatu(
            "gam",
            "गम्",
            DhatuGana.BHVADI,
        )

        second = make_dhatu(
            "bhu",
            "भू",
            DhatuGana.BHVADI,
        )

        repository = DefaultDhatuRepository(
            dhatus=(first, second)
        )

        repository.clear()

        assert repository.count == 0
        assert repository.all().is_empty
