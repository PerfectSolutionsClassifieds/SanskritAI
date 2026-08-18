from __future__ import annotations

import pytest

from SanskritAI.domain.morphology.grammatical_category_collection import (
    GrammaticalCategoryCollection,
)
from SanskritAI.domain.morphology.vibhakti import Vibhakti
from SanskritAI.domain.morphology.vacana import Vacana
from SanskritAI.domain.morphology.linga import Linga


class TestGrammaticalCategoryCollection:
    """
    Behavioural tests for the immutable
    GrammaticalCategoryCollection.
    """

    def _create_collection(
        self,
    ) -> GrammaticalCategoryCollection:

        return GrammaticalCategoryCollection(
            items=(
                Vibhakti(),
                Vacana(),
                Linga(),
            )
        )

    # =========================================================
    # Construction
    # =========================================================

    def test_default_construction(self):
        collection = GrammaticalCategoryCollection()

        assert collection.is_empty
        assert collection.count == 0

    def test_construction_with_items(self):
        collection = self._create_collection()

        assert collection.count == 3
        assert not collection.is_empty

    # =========================================================
    # Iteration
    # =========================================================

    def test_iteration(self):
        collection = self._create_collection()

        items = tuple(collection)

        assert len(items) == 3
        assert isinstance(items[0], Vibhakti)
        assert isinstance(items[1], Vacana)
        assert isinstance(items[2], Linga)

    # =========================================================
    # Length
    # =========================================================

    def test_len(self):
        collection = self._create_collection()

        assert len(collection) == 3

    # =========================================================
    # Indexing
    # =========================================================

    def test_indexing(self):
        collection = self._create_collection()

        assert isinstance(
            collection[0],
            Vibhakti,
        )

        assert isinstance(
            collection[1],
            Vacana,
        )

        assert isinstance(
            collection[2],
            Linga,
        )

    # =========================================================
    # First / Last
    # =========================================================

    def test_first(self):
        collection = self._create_collection()

        assert isinstance(
            collection.first,
            Vibhakti,
        )

    def test_last(self):
        collection = self._create_collection()

        assert isinstance(
            collection.last,
            Linga,
        )

    def test_first_on_empty_collection(self):
        collection = GrammaticalCategoryCollection()

        assert collection.first is None

    def test_last_on_empty_collection(self):
        collection = GrammaticalCategoryCollection()

        assert collection.last is None

    # =========================================================
    # Membership
    # =========================================================

    def test_contains_existing_category(self):
        collection = self._create_collection()

        for category in collection:
            assert category in collection

    # =========================================================
    # Search
    # =========================================================

    def test_find_existing_identifier(self):
        collection = self._create_collection()

        category = collection[0]

        result = collection.find(
            category.identifier,
        )

        assert result is category

    def test_find_missing_identifier(self):
        collection = self._create_collection()

        result = collection.find(
            "__does_not_exist__",
        )

        assert result is None

    # =========================================================
    # Immutability
    # =========================================================

    def test_collection_is_immutable(self):
        collection = self._create_collection()

        with pytest.raises(AttributeError):
            collection.items = ()

    def test_items_are_tuple(self):
        collection = self._create_collection()

        assert isinstance(
            collection.items,
            tuple,
        )

    # =========================================================
    # Display
    # =========================================================

    def test_display_name(self):
        collection = self._create_collection()

        assert (
            collection.display_name
            == "Grammatical Categories"
        )

    def test_display_text(self):
        collection = self._create_collection()

        assert (
            collection.display_text
            == "3 Categories"
        )

    def test_display_description(self):
        collection = self._create_collection()

        assert collection.display_description

    def test_string_representation(self):
        collection = self._create_collection()

        assert (
            str(collection)
            == collection.display_text
        )
