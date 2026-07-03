from lexicon.dictionary import Dictionary
from services.analysis_service import AnalysisService
from services.translation_service import TranslationService


def test_analysis_service_uses_injected_dictionary():
    result = AnalysisService(Dictionary("data/dictionaries/basic.json")).analyze("धर्म")
    assert result.words[0].meaning == "duty, righteousness, law"


def test_translation_service_uses_known_meanings():
    result = AnalysisService(Dictionary("data/dictionaries/basic.json")).analyze("धर्म")
    assert TranslationService().translate(result) == "duty, righteousness, law"
