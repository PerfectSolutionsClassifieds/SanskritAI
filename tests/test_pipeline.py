from lexicon.dictionary import Dictionary
from pipeline.pipeline import AnalysisPipeline


def test_pipeline_finds_dictionary_meaning():
    pipeline = AnalysisPipeline(Dictionary("data/dictionaries/basic.json"))
    result = pipeline.run("धर्म कर्म।")

    assert result.tokens == ["धर्म", "कर्म", "।"]
    assert result.words[0].meaning == "duty, righteousness, law"
    assert result.words[1].lemma == "कर्मन्"
