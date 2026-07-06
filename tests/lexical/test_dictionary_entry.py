"""
SanskritAI
==========

DictionaryEntry Unit Tests

Version:
    v0.3.0 Final
"""

from tests.lexical.sample_lexemes import create_agni


def test() -> None:
    """
    Validate DictionaryEntry construction.
    """

    agni = create_agni()

    assert agni.dictionary_count == 1

    entry = agni.dictionary_entries[0]

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    assert entry.entry_id == "ENTRY-AGNI-AMARA"

    assert entry.headword == "अग्नि"

    # ---------------------------------------------------------
    # Source
    # ---------------------------------------------------------

    print("Dictionary Source :", entry.source.value)

    # ---------------------------------------------------------
    # Senses
    # ---------------------------------------------------------

    assert entry.sense_count == 1

    for sense in entry.senses:

        print("Sense ID         :", sense.sense_id)

        print("Definition       :", sense.definition)

        print("Language         :", sense.language)

        print("Examples         :", sense.example_count)

    print()

    print("DictionaryEntry test PASSED")


if __name__ == "__main__":
    test()
