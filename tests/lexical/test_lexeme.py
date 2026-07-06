"""
SanskritAI
==========

Lexeme Unit Tests

Version:
    v0.3.0 Final
"""

from models.enums.dictionary_source import DictionarySource

from tests.lexical.sample_lexemes import create_rama


def test() -> None:
    """
    Validate the Lexeme object.
    """

    rama = create_rama()

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    assert rama.lexeme_id == "LEX-RAMA"

    assert rama.lemma == "राम"

    # ---------------------------------------------------------
    # Language
    # ---------------------------------------------------------

    assert rama.transliteration == "rāma"

    print("Lemma             :", rama.lemma)
    print("Lexeme ID         :", rama.lexeme_id)
    print("Language          :", rama.language.value)
    print("Script            :", rama.script.value)

    # ---------------------------------------------------------
    # Dictionary entries
    # ---------------------------------------------------------

    assert rama.dictionary_count == 1

    assert rama.has_entry(DictionarySource.AMARAKOSHA)

    entry = rama.get_entry(DictionarySource.AMARAKOSHA)

    assert entry is not None

    assert entry.headword == "राम"

    print("Dictionary Count  :", rama.dictionary_count)
    print("Dictionary Source :", entry.source.value)

    # ---------------------------------------------------------
    # Relations
    # ---------------------------------------------------------

    assert rama.relation_count == 0

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    data = rama.to_dict()

    assert data["lemma"] == "राम"

    assert data["lexeme_id"] == "LEX-RAMA"

    assert len(data["dictionary_entries"]) == 1

    # ---------------------------------------------------------
    # Internal index
    # ---------------------------------------------------------

    assert DictionarySource.AMARAKOSHA in rama.dictionary_sources

    print()
    print("Lexeme test PASSED")


if __name__ == "__main__":
    test()
