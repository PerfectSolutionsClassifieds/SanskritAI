from lexicon.dictionary import Dictionary


def test_dictionary_lookup_sample_entry():
    dictionary = Dictionary("data/dictionaries/basic.json")
    assert dictionary.lookup("धर्म")["lemma"] == "धर्म"
