from input.normalizer import normalize_text


def test_normalizer_spaces_danda():
    assert normalize_text("धर्म  कर्म।") == "धर्म कर्म ।"
