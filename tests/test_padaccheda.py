from analysis.padaccheda import split_compound


def test_padaccheda_placeholder_returns_input():
    assert split_compound("धर्मक्षेत्रे") == ["धर्मक्षेत्रे"]
