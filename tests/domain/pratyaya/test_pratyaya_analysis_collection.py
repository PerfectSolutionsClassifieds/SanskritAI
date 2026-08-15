
from SanskritAI.domain.pratyaya.pratyaya_analysis import PratyayaAnalysis
from SanskritAI.domain.pratyaya.pratyaya_analysis_collection import (
    PratyayaAnalysisCollection,
)


def make_analysis(
    identifier: str = "analysis-1",
    pratyaya: str = "क्त",
    confidence: float = 1.0,
) -> PratyayaAnalysis:
    return PratyayaAnalysis(
        identifier=identifier,
        pratyaya=pratyaya,
        confidence=confidence,
    )


def test_empty_collection_has_no_analyses():
    collection = PratyayaAnalysisCollection()

    assert collection.is_empty is True
    assert collection.has_analyses is False


def test_non_empty_collection_has_analyses():
    analysis = make_analysis()

    collection = PratyayaAnalysisCollection(
        analyses=(analysis,),
    )

    assert collection.is_empty is False
    assert collection.has_analyses is True


def test_has_analyses_is_consistent_with_is_empty():
    empty = PratyayaAnalysisCollection()
    non_empty = PratyayaAnalysisCollection(
        analyses=(make_analysis(),),
    )

    assert empty.has_analyses == (not empty.is_empty)
    assert non_empty.has_analyses == (not non_empty.is_empty)


def test_has_analyses_is_read_only_semantic_alias():
    analysis = make_analysis()

    collection = PratyayaAnalysisCollection(
        analyses=(analysis,),
    )

    assert collection.has_analyses is True
    assert collection.count == 1


def test_add_does_not_mutate_original_collection():
    original = PratyayaAnalysisCollection()
    analysis = make_analysis()

    result = original.add(analysis)

    assert original.analyses == ()
    assert original.count == 0
    assert original.is_empty is True
    assert original.has_analyses is False

    assert result.analyses == (analysis,)
    assert result.count == 1
    assert result.is_empty is False
    assert result.has_analyses is True


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
    assert result.is_empty is False
    assert result.has_analyses is True

    assert left.analyses == (first,)
    assert right.analyses == (second,)
