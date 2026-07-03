from analysis.tokenizer import tokenize


def test_tokenizer_handles_devanagari_and_danda():
    assert tokenize("धर्म कर्म ।") == ["धर्म", "कर्म", "।"]
