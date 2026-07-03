from models.word import Word


def test_word_defaults_to_empty_features():
    word = Word(text="धर्म")
    assert word.features == {}
