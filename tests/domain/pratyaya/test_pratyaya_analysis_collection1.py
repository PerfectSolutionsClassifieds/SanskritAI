
from __future__ import annotations

import pytest

from SanskritAI.domain.pratyaya.pratyaya_analysis import PratyayaAnalysis
from SanskritAI.domain.pratyaya.pratyaya_analysis_collection import (
    PratyayaAnalysisCollection,
)


def make_analysis(
    identifier: str = "analysis-1",
    pratyaya: str = "क्त",
    *,
    transliteration: str = "",
    meaning: str = "",
    confidence: float = 1.0,
    matched_rule: str = "",
    notes: str = "",
) -> PratyayaAnalysis:
    return PratyayaAnalysis(
        identifier=identifier,
        pratyaya=pratyaya,
        transliteration=transliteration,
        meaning=meaning,
        confidence=confidence,
        matched_rule=matched_rule,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_default_collection_is_empty():
    collection = PratyayaAnalysisCollection()

    assert collection.analyses == ()
    assert collection.count == 0
    assert collection.is_empty


def test_collection_accepts_tuple_of_analyses():
    first = make_analysis()
    second = make_analysis(
        identifier="analysis-2",
        pratyaya="तव्य",
    )

    collection = PratyayaAnalysisCollection(
        analyses=(first, second),
    )

    assert collection.analyses == (first, second)
    assert collection.count == 2
    assert not collection.is_empty


# ---------------------------------------------------------------------------
# has_analyses
# ---------------------------------------------------------------------------


def test_empty_collection_has_no_analyses():
    collection = PratyayaAnalysisCollection()

    assert collection.has_analyses is False


def test_non_empty_collection_has_analyses():
    analysis = make_analysis()

    collection = PratyayaAnalysisCollection(
        analyses=(analysis,),
    )

    assert collection.has_analyses is True


def test_has_analyses_is_consistent_with_is_empty():
    empty = PratyayaAnalysisCollection()
    non_empty = PratyayaAnalysisCollection(
        analyses=(make_analysis(),),
    )

    assert empty.has_analyses == (not empty.is_empty)
    assert non_empty.has_analyses == (not non_empty.is_empty)


# ---------------------------------------------------------------------------
# count / is_empty
# ---------------------------------------------------------------------------


def test_count_returns_number_of_analyses():
    first = make_analysis()
    second = make_analysis(
        identifier="analysis-2",
        pratyaya="तव्य",
    )
    third = make_analysis(
        identifier="analysis-3",
        pratyaya="अनीयर्",
    )

    collection = PratyayaAnalysisCollection(
        analyses=(first, second, third),
    )

    assert collection.count == 3


def test_is_empty_returns_false_for_non_empty_collection():
    collection = PratyayaAnalysisCollection(
        analyses=(make_analysis(),),
    )

    assert collection.is_empty is False


# ---------------------------------------------------------------------------
# first
# ---------------------------------------------------------------------------


def test_first_returns_none_for_empty_collection():
    collection = PratyayaAnalysisCollection()

    assert collection.first is None


def test_first_returns_first_analysis():
    first = make_analysis(
        identifier="first",
        pratyaya="क्त",
    )
    second = make_analysis(
        identifier="second",
        pratyaya="तव्य",
    )

    collection = PratyayaAnalysisCollection(
        analyses=(first, second),
    )

    assert collection.first is first


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------


def test_add_returns_new_collection():
    original = PratyayaAnalysisCollection()
    analysis = make_analysis()

    result = original.add(analysis)

    assert result is not original
    assert result.analyses == (analysis,)


def test_add_does_not_mutate_original_collection():
    original = PratyayaAnalysisCollection()
    analysis = make_analysis()

    result = original.add(analysis)

    assert original.analyses == ()
    assert original.count == 0
    assert original.is_empty
    assert original.has_analyses is False

    assert result.analyses == (analysis,)
    assert result.count == 1
    assert result.is_empty is False
    assert result.has_analyses is True


def test_add_preserves_existing_order():
    first = make_analysis(
        identifier="first",
        pratyaya="क्त",
    )
    second = make_analysis(
        identifier="second",
        pratyaya="तव्य",
    )

    original = PratyayaAnalysisCollection(
        analyses=(first,),
    )

    result = original.add(second)

    assert result.analyses == (first, second)
    assert result.first is first


# ---------------------------------------------------------------------------
# extend
# ---------------------------------------------------------------------------


def test_extend_combines_two_collections():
    first = make_analysis(
        identifier="first",
        pratyaya="क्त",
    )
    second = make_analysis(
        identifier="second",
        pratyaya="तव्य",
    )

    left = PratyayaAnalysisCollection(
        analyses=(first,),
    )
    right = PratyayaAnalysisCollection(
        analyses=(second,),
    )

    result = left.extend(right)

    assert result.analyses == (first, second)
    assert result.count == 2
    assert result.has_analyses is True


def test_extend_preserves_order():
    analyses_left = (
        make_analysis(identifier="a", pratyaya="क्त"),
        make_analysis(identifier="b", pratyaya="तव्य"),
    )
    analyses_right = (
        make_analysis(identifier="c", pratyaya="अनीयर्"),
        make_analysis(identifier="d", pratyaya="ल्युट्"),
    )

    left = PratyayaAnalysisCollection(analyses=analyses_left)
    right = PratyayaAnalysisCollection(analyses=analyses_right)

    result = left.extend(right)

    assert result.analyses == analyses_left + analyses_right


def test_extend_does_not_mutate_either_collection():
    first = make_analysis(
        identifier="first",
        pratyaya="क्त",
    )
    second = make_analysis(
        identifier="second",
        pratyaya="तव्य",
    )

    left = PratyayaAnalysisCollection(
        analyses=(first,),
    )
    right = PratyayaAnalysisCollection(
        analyses=(second,),
    )

    result = left.extend(right)

    assert left.analyses == (first,)
    assert right.analyses == (second,)
    assert result.analyses == (first, second)


def test_extend_empty_collection_returns_expected_values():
    analysis = make_analysis()

    collection = PratyayaAnalysisCollection(
        analyses=(analysis,),
    )
    empty = PratyayaAnalysisCollection()

    result_left = collection.extend(empty)
    result_right = empty.extend(collection)

    assert result_left.analyses == (analysis,)
    assert result_right.analyses == (analysis,)


# ---------------------------------------------------------------------------
# Iteration / indexing / length
# ---------------------------------------------------------------------------


def test_collection_is_iterable():
    first = make_analysis(
        identifier="first",
        pratyaya="क्त",
    )
    second = make_analysis(
        identifier="second",
        pratyaya="तव्य",
    )

    collection = PratyayaAnalysisCollection(
        analyses=(first, second),
    )

    assert tuple(collection) == (first, second)


def test_len_matches_count():
    analyses = (
        make_analysis(identifier="first"),
        make_analysis(identifier="second", pratyaya="तव्य"),
    )

    collection = PratyayaAnalysisCollection(
        analyses=analyses,
    )

    assert len(collection) == collection.count


def test_index_access_returns_analysis():
    first = make_analysis(
        identifier="first",
        pratyaya="क्त",
    )
    second = make_analysis(
        identifier="second",
        pratyaya="तव्य",
    )

    collection = PratyayaAnalysisCollection(
        analyses=(first, second),
    )

    assert collection[0] is first
    assert collection[1] is second


def test_index_access_supports_negative_indices():
    first = make_analysis(
        identifier="first",
        pratyaya="क्त",
    )
    second = make_analysis(
        identifier="second",
        pratyaya="तव्य",
    )

    collection = PratyayaAnalysisCollection(
        analyses=(first, second),
    )

    assert collection[-1] is second
    assert collection[-2] is first


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


def test_collection_is_immutable():
    collection = PratyayaAnalysisCollection(
        analyses=(make_analysis(),),
    )

    with pytest.raises((AttributeError, TypeError)):
        collection.analyses = ()


def test_collection_uses_tuple_for_storage():
    collection = PratyayaAnalysisCollection(
        analyses=(make_analysis(),),
    )

    assert isinstance(collection.analyses, tuple)


# ---------------------------------------------------------------------------
# Display semantics
# ---------------------------------------------------------------------------


def test_display_name():
    collection = PratyayaAnalysisCollection()

    assert collection.display_name == "Pratyaya Analyses"


def test_display_text_for_empty_collection():
    collection = PratyayaAnalysisCollection()

    assert collection.display_text == "0 analyses"


def test_display_text_for_non_empty_collection():
    collection = PratyayaAnalysisCollection(
        analyses=(
            make_analysis(identifier="first"),
            make_analysis(identifier="second", pratyaya="तव्य"),
        ),
    )

    assert collection.display_text == "2 analyses"


def test_display_description():
    collection = PratyayaAnalysisCollection()

    assert (
        collection.display_description
        == "Immutable collection of Pratyaya analyses."
    )


def test_str_uses_display_text():
    collection = PratyayaAnalysisCollection(
        analyses=(make_analysis(),),
    )

    assert str(collection) == "1 analyses"


# ---------------------------------------------------------------------------
# Equality / value-object behavior
# ---------------------------------------------------------------------------


def test_equal_collections_compare_equal():
    first = make_analysis(
        identifier="analysis-1",
        pratyaya="क्त",
    )

    left = PratyayaAnalysisCollection(
        analyses=(first,),
    )
    right = PratyayaAnalysisCollection(
        analyses=(first,),
    )

    assert left == right


def test_different_collections_compare_not_equal():
    left = PratyayaAnalysisCollection(
        analyses=(
            make_analysis(
                identifier="analysis-1",
                pratyaya="क्त",
            ),
        ),
    )

    right = PratyayaAnalysisCollection(
        analyses=(
            make_analysis(
                identifier="analysis-2",
                pratyaya="तव्य",
            ),
        ),
    )

    assert left != right
