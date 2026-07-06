"""
SanskritAI
==========

Lexical Layer Integrity Tests

Version:
    v0.3.0 Final
"""

from tests.lexical.sample_lexemes import (
    create_rama,
    create_agni,
    create_gam,
)


def test() -> None:
    """
    Validate integrity of the sample lexical objects.
    """

    lexemes = [
        create_rama(),
        create_agni(),
        create_gam(),
    ]

    seen_ids = set()

    for lexeme in lexemes:

        # -----------------------------------------------------
        # Unique identity
        # -----------------------------------------------------

        assert lexeme.lexeme_id not in seen_ids

        seen_ids.add(lexeme.lexeme_id)

        # -----------------------------------------------------
        # Basic validation
        # -----------------------------------------------------

        assert lexeme.lemma

        assert lexeme.dictionary_count >= 1

        assert len(lexeme.dictionary_entries) == lexeme.dictionary_count

        # -----------------------------------------------------
        # Dictionary consistency
        # -----------------------------------------------------

        for entry in lexeme.dictionary_entries:

            assert entry.headword == lexeme.lemma

            assert entry.sense_count >= 1

        # -----------------------------------------------------
        # Internal index consistency
        # -----------------------------------------------------

        assert len(lexeme.dictionary_sources) == lexeme.dictionary_count

    print(f"Validated {len(lexemes)} Lexeme objects.")
    print("Lexical integrity test PASSED")


if __name__ == "__main__":
    test()
